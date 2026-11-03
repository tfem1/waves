#!/usr/bin/env python3
"""waves — a minimal, good-looking system fetch."""
from __future__ import annotations

import argparse
import getpass
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time

__version__ = "0.1.0"

# ───────────────────────────── themes ─────────────────────────────

THEMES = {
    "ocean":  [(0, 210, 255), (58, 123, 213), (120, 80, 220)],
    "sunset": [(255, 175, 90), (255, 95, 109), (190, 70, 160)],
    "mint":   [(150, 255, 200), (60, 200, 170), (40, 120, 170)],
    "aurora": [(130, 255, 160), (60, 200, 255), (200, 110, 255)],
    "mono":   [(230, 230, 230), (160, 160, 160), (100, 100, 100)],
}

LOGO = [
    "      .~~.              ",
    "   .~'    '~.      .~'  ",
    "~~'          '~~~~'     ",
    "                        ",
    "        .~~.            ",
    "     .~'    '~.      .~ ",
    "  ~~'          '~~~~'   ",
    "                        ",
    "          .~~.          ",
    "       .~'    '~.     . ",
    "    ~~'          '~~~'  ",
]

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"


class Painter:
    def __init__(self, theme: str, enabled: bool):
        self.stops = THEMES[theme]
        self.on = enabled

    def lerp(self, t: float):
        t = max(0.0, min(1.0, t))
        seg = t * (len(self.stops) - 1)
        i = min(int(seg), len(self.stops) - 2)
        f = seg - i
        a, b = self.stops[i], self.stops[i + 1]
        return tuple(round(a[k] + (b[k] - a[k]) * f) for k in range(3))

    def fg(self, rgb) -> str:
        return f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" if self.on else ""

    def at(self, t: float, s: str, bold=False) -> str:
        if not self.on:
            return s
        return (BOLD if bold else "") + self.fg(self.lerp(t)) + s + RESET

    def gradient(self, s: str, t0=0.0, t1=1.0, bold=False) -> str:
        if not self.on:
            return s
        n = max(len(s) - 1, 1)
        out = []
        for i, ch in enumerate(s):
            if ch == " ":
                out.append(ch)
                continue
            out.append(self.fg(self.lerp(t0 + (t1 - t0) * i / n)) + ch)
        return (BOLD if bold else "") + "".join(out) + RESET

    def dim(self, s: str) -> str:
        return f"{DIM}{s}{RESET}" if self.on else s


def vlen(s: str) -> int:
    return len(ANSI_RE.sub("", s))


# ───────────────────────────── helpers ─────────────────────────────

def read(path: str, default: str = "") -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    except OSError:
        return default


def run(cmd: list[str]) -> str:
    if not shutil.which(cmd[0]):
        return ""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=2).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def human(n: float, unit="B") -> str:
    for p in ["", "Ki", "Mi", "Gi", "Ti", "Pi"]:
        if abs(n) < 1024 or p == "Pi":
            return f"{n:.1f} {p}{unit}" if p else f"{n:.0f} {unit}"
        n /= 1024
    return f"{n:.1f}"


def human_si(n: float) -> str:
    for p in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if n < 1000 or p == "PB":
            return f"{n:.0f} {p}" if n >= 100 or p == "B" else f"{n:.1f} {p}"
        n /= 1000
    return ""


JUNK = re.compile(
    r"\b(to be filled by o\.e\.m\.|default string|system product name|not applicable|"
    r"none|unknown|o\.e\.m\.|oem)\b", re.I)


def clean(s: str) -> str:
    s = re.sub(r"\((R|TM|tm|r)\)", "", s)
    s = re.sub(r"\b(CPU|Processor|with Radeon Graphics)\b", "", s)
    s = re.sub(r"@.*", "", s)
    s = re.sub(r"\s+\d+-Core\b", "", s)
    return re.sub(r"\s{2,}", " ", s).strip()


# ───────────────────────────── probes ─────────────────────────────

def get_os() -> str:
    if sys.platform == "darwin":
        v = run(["sw_vers", "-productVersion"])
        return f"macOS {v}".strip()
    rel = {}
    for line in read("/etc/os-release").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            rel[k] = v.strip().strip('"')
    name = rel.get("PRETTY_NAME") or rel.get("NAME") or platform.system()
    return f"{name} {platform.machine()}"


def get_kernel() -> str:
    return f"{platform.system()} {platform.release()}"


def get_uptime() -> str:
    raw = read("/proc/uptime").split()
    if not raw:
        return ""
    s = int(float(raw[0]))
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m = s // 60
    parts = [f"{d}d"] * bool(d) + [f"{h}h"] * bool(h) + [f"{m}m"]
    return " ".join(parts)


def get_shell() -> str:
    sh = os.path.basename(os.environ.get("SHELL", ""))
    return sh


def get_cpu() -> str:
    info = read("/proc/cpuinfo")
    model = ""
    for key in ("model name", "Hardware", "Model", "cpu model"):
        m = re.search(rf"^{key}\s*:\s*(.+)$", info, re.M)
        if m:
            model = m.group(1)
            break
    if not model:
        model = run(["sysctl", "-n", "machdep.cpu.brand_string"]) or platform.processor()
    threads = os.cpu_count() or 0
    cores = len(set(re.findall(r"^core id\s*:\s*(\d+)", info, re.M))) * max(
        len(set(re.findall(r"^physical id\s*:\s*(\d+)", info, re.M))), 1)
    mhz = read("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
    freq = f" @ {int(mhz) / 1e6:.2f} GHz" if mhz.isdigit() else ""
    count = f"{cores}c/{threads}t" if cores and cores != threads else f"{threads}t"
    return f"{clean(model)} ({count}){freq}"


def get_memory():
    mem = {}
    for line in read("/proc/meminfo").splitlines():
        k, _, v = line.partition(":")
        if v.strip():
            mem[k] = int(v.split()[0]) * 1024
    total = mem.get("MemTotal", 0)
    avail = mem.get("MemAvailable", mem.get("MemFree", 0))
    return total - avail, total


def get_gpus(limit=2) -> list[str]:
    gpus = []
    out = run(["lspci", "-mm"])
    for line in out.splitlines():
        f = re.findall(r'"([^"]*)"', line)
        if len(f) >= 3 and re.search(r"VGA|3D|Display", f[0]):
            vendor = re.sub(r"\b(Corporation|Inc\.?|Technologies|\[AMD/ATI\])\b", "", f[1]).strip()
            vendor = vendor.replace("Advanced Micro Devices, ", "AMD").strip(" ,")
            dev = f[2]
            m = re.search(r"\[(.+?)\]", dev)
            gpus.append(f"{vendor} {m.group(1) if m else dev}".strip())
    if not gpus:  # fallback: sysfs PCI ids
        vendors = {"0x10de": "NVIDIA", "0x1002": "AMD", "0x8086": "Intel",
                   "0x1af4": "Virtio", "0x1234": "QEMU", "0x15ad": "VMware"}
        base = "/sys/bus/pci/devices"
        for d in sorted(os.listdir(base)) if os.path.isdir(base) else []:
            if read(f"{base}/{d}/class").startswith("0x03"):
                v = read(f"{base}/{d}/vendor")
                gpus.append(f"{vendors.get(v, v)} GPU [{read(f'{base}/{d}/device')}]")
    if not gpus and sys.platform == "darwin":
        gpus = re.findall(r"Chipset Model:\s*(.+)", run(["system_profiler", "SPDisplaysDataType"]))
    return gpus[:limit]


def get_disks(limit=2) -> list[dict]:
    disks = []
    base = "/sys/block"
    if not os.path.isdir(base):
        return disks
    for name in sorted(os.listdir(base)):
        if re.match(r"(loop|ram|zram|dm-|sr|fd|md)", name):
            continue
        size = int(read(f"{base}/{name}/size", "0") or 0) * 512
        if size <= 0:
            continue
        model = read(f"{base}/{name}/device/model") or name
        if name.startswith("nvme"):
            kind = "NVMe"
        elif name.startswith("vd"):
            kind = "Virtual"
        elif read(f"{base}/{name}/queue/rotational") == "1":
            kind = "HDD"
        else:
            kind = "SSD"
        removable = read(f"{base}/{name}/removable") == "1"
        disks.append({"name": name, "model": model.strip(), "size": size,
                      "type": kind + (" · USB" if removable else "")})
    # Biggest first feels most relevant for a fetch
    disks.sort(key=lambda d: d["size"], reverse=True)
    return disks[:limit]


def get_root_usage():
    try:
        u = shutil.disk_usage("/")
        return u.used, u.total
    except OSError:
        return 0, 0


def get_board() -> str:
    d = "/sys/class/dmi/id"
    vendor = read(f"{d}/board_vendor")
    name = read(f"{d}/board_name")
    if not name or JUNK.search(name):
        name = read(f"{d}/product_name")
    vendor = "" if JUNK.search(vendor) else vendor
    name = "" if JUNK.search(name) else name
    vendor = re.sub(r"\b(Co\.,? ?Ltd\.?|Inc\.?|Corporation|COMPUTER INC\.?)\b", "", vendor, flags=re.I).strip(" ,.")
    return f"{vendor} {name}".strip()


def collect() -> dict:
    used, total = get_memory()
    rused, rtotal = get_root_usage()
    return {
        "user": getpass.getuser(),
        "host": socket.gethostname(),
        "os": get_os(),
        "kernel": get_kernel(),
        "uptime": get_uptime(),
        "shell": get_shell(),
        "board": get_board(),
        "cpu": get_cpu(),
        "gpus": get_gpus(),
        "memory": {"used": used, "total": total},
        "disks": get_disks(),
        "root": {"used": rused, "total": rtotal},
    }


# ───────────────────────────── render ─────────────────────────────

def bar(p: Painter, ratio: float, width=14) -> str:
    ratio = max(0.0, min(1.0, ratio))
    filled = max(round(ratio * width), 1 if ratio > 0 else 0)
    if not p.on:
        return "[" + "#" * filled + "-" * (width - filled) + "]"
    out = "".join(p.fg(p.lerp(i / max(width - 1, 1))) + "━" for i in range(filled))
    return out + RESET + p.dim("─" * (width - filled))


def render(data: dict, p: Painter, show_logo=True) -> str:
    lab_w = 7
    rows: list[str] = []

    def row(label: str, value: str, t: float):
        if value:
            rows.append(f"{p.at(t, label.ljust(lab_w), bold=True)} {value}")

    title = f"{data['user']}@{data['host']}"
    rows.append(p.gradient(title, bold=True))
    rows.append(p.dim("─" * max(len(title), 24)))

    entries = [("os", data["os"]), ("kernel", data["kernel"]),
               ("uptime", data["uptime"]), ("shell", data["shell"]),
               ("board", data["board"]), ("cpu", data["cpu"])]
    for i, g in enumerate(data["gpus"]):
        entries.append((f"gpu{i + 1}" if len(data["gpus"]) > 1 else "gpu", g))

    m = data["memory"]
    if m["total"]:
        r = m["used"] / m["total"]
        entries.append(("ram", f"{human(m['used'])} / {human(m['total'])}  "
                               f"{bar(p, r)} {p.dim(f'{r * 100:.0f}%')}"))
    for i, d in enumerate(data["disks"]):
        lbl = f"disk{i + 1}" if len(data["disks"]) > 1 else "disk"
        model = d["model"] if d["model"] != d["name"] else ""
        entries.append((lbl, f"{human_si(d['size'])} {d['type']}"
                             + (f" {p.dim('·')} {model}" if model else "")
                             + f" {p.dim('(' + d['name'] + ')')}"))
    rt = data["root"]
    if rt["total"]:
        r = rt["used"] / rt["total"]
        entries.append(("root", f"{human(rt['used'])} / {human(rt['total'])}  "
                                f"{bar(p, r)} {p.dim(f'{r * 100:.0f}%')}"))

    n = len(entries)
    for i, (k, v) in enumerate(entries):
        row(k, v, i / max(n - 1, 1))

    rows.append("")
    rows.append("  ".join(p.at(i / 7, "●") for i in range(8)) if p.on else "")

    if not show_logo:
        return "\n".join(rows)

    logo_w = max(len(l) for l in LOGO)
    logo = [p.gradient(l.ljust(logo_w), t0=i / len(LOGO) * 0.4, t1=0.6 + i / len(LOGO) * 0.4)
            for i, l in enumerate(LOGO)]
    logo.append(" " * logo_w)
    logo.append(" " * ((logo_w - 9) // 2) + p.gradient("w a v e s", bold=True) + " " * ((logo_w - 9) // 2 + 1))

    h = max(len(logo), len(rows))
    lpad = (h - len(logo)) // 2
    rpad = (h - len(rows)) // 2
    logo = [" " * logo_w] * lpad + logo + [" " * logo_w] * (h - len(logo) - lpad)
    rows = [""] * rpad + rows + [""] * (h - len(rows) - rpad)
    out = [f"  {l}   {r}".rstrip() for l, r in zip(logo, rows)]
    return "\n" + "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(prog="waves", description="A minimal, good-looking system fetch.")
    ap.add_argument("-t", "--theme", choices=THEMES, default=os.environ.get("WAVES_THEME", "ocean"))
    ap.add_argument("--no-color", action="store_true", help="disable colors")
    ap.add_argument("--no-logo", action="store_true", help="hide the wave logo")
    ap.add_argument("--json", action="store_true", help="print raw data as JSON")
    ap.add_argument("--themes", action="store_true", help="preview every theme")
    ap.add_argument("-V", "--version", action="version", version=f"waves {__version__}")
    a = ap.parse_args()
    if a.theme not in THEMES:
        a.theme = "ocean"

    t0 = time.perf_counter()
    data = collect()
    if a.json:
        print(json.dumps(data, indent=2))
        return
    color = not a.no_color and "NO_COLOR" not in os.environ and sys.stdout.isatty() or os.environ.get("FORCE_COLOR")
    if a.themes:
        for name in THEMES:
            p = Painter(name, bool(color))
            print(f"\n  {p.gradient(name, bold=True)}")
            print(render(data, p, show_logo=not a.no_logo))
        return
    print(render(data, Painter(a.theme, bool(color)), show_logo=not a.no_logo))
    if os.environ.get("WAVES_DEBUG"):
        print(f"  {(time.perf_counter() - t0) * 1000:.1f} ms")


if __name__ == "__main__":
    main()
