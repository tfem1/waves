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

# 40 themes in four categories: sea, gradient, mono, light.
# ── themes:begin ──
THEMES = {
    # sea — gradients drawn from the ocean
    "surf":      ("sea", [(180, 250, 255), (0, 190, 255), (30, 80, 200)]),
    "ocean":     ("sea", [(0, 210, 255), (58, 123, 213), (120, 80, 220)]),
    "lagoon":    ("sea", [(150, 255, 235), (40, 215, 210), (20, 140, 170)]),
    "reef":      ("sea", [(255, 150, 120), (255, 100, 140), (60, 200, 215)]),
    "deepsea":   ("sea", [(70, 200, 255), (40, 110, 220), (40, 50, 150)]),
    "biolume":   ("sea", [(130, 255, 230), (40, 180, 255), (170, 100, 255)]),
    "seafoam":   ("sea", [(220, 255, 245), (140, 230, 210), (80, 175, 185)]),
    "kelp":      ("sea", [(200, 235, 130), (90, 180, 115), (40, 125, 110)]),
    "storm":     ("sea", [(210, 222, 235), (120, 145, 175), (80, 95, 135)]),
    "arctic":    ("sea", [(235, 250, 255), (150, 215, 245), (90, 150, 225)]),
    "tropic":    ("sea", [(255, 225, 120), (70, 225, 200), (30, 150, 230)]),
    "riptide":   ("sea", [(0, 255, 200), (0, 170, 255), (80, 80, 235)]),
    "maelstrom": ("sea", [(90, 220, 255), (130, 100, 255), (235, 70, 180)]),
    "nautilus":  ("sea", [(255, 215, 170), (235, 150, 100), (170, 90, 80)]),
    "pearl":     ("sea light", [(40, 110, 170), (110, 90, 180), (170, 80, 130)],
                  ((246, 248, 252), (228, 234, 247))),
    "sandbar":   ("sea light", [(20, 120, 140), (200, 110, 40), (180, 70, 70)],
                  ((250, 245, 233), (236, 225, 203))),
    # gradient
    "sunset":    ("gradient", [(255, 175, 90), (255, 95, 109), (190, 70, 160)]),
    "mint":      ("gradient", [(150, 255, 200), (60, 200, 170), (40, 120, 170)]),
    "aurora":    ("gradient", [(130, 255, 160), (60, 200, 255), (200, 110, 255)]),
    "synthwave": ("gradient", [(255, 90, 200), (150, 90, 255), (40, 210, 255)]),
    "dusk":      ("gradient", [(255, 175, 125), (205, 105, 170), (100, 80, 170)]),
    "candy":     ("gradient", [(255, 160, 205), (205, 165, 255), (140, 220, 255)]),
    "ember":     ("gradient", [(255, 220, 120), (255, 125, 60), (205, 45, 65)]),
    "forest":    ("gradient", [(205, 240, 150), (95, 190, 125), (45, 115, 95)]),
    "nebula":    ("gradient", [(255, 125, 225), (150, 95, 255), (70, 185, 255)]),
    "citrus":    ("gradient", [(255, 240, 120), (185, 240, 95), (65, 200, 125)]),
    "vapor":     ("gradient", [(120, 255, 230), (255, 145, 220), (165, 125, 255)]),
    "peach":     ("gradient light", [(200, 90, 90), (210, 120, 60), (150, 90, 160)],
                  ((252, 244, 238), (243, 228, 224))),
    # mono — one hue, light → deep
    "mono":      ("mono", [(230, 230, 230), (160, 160, 160), (100, 100, 100)]),
    "snow":      ("mono", [(255, 255, 255), (235, 235, 240), (200, 200, 210)]),
    "graphite":  ("mono", [(200, 200, 205), (150, 150, 158), (110, 110, 118)]),
    "ice":       ("mono", [(200, 235, 255), (110, 180, 245), (40, 110, 210)]),
    "abyss":     ("mono", [(120, 160, 255), (75, 105, 230), (55, 70, 190)]),
    "matrix":    ("mono", [(180, 255, 180), (60, 220, 90), (20, 140, 50)]),
    "ruby":      ("mono", [(255, 170, 170), (235, 70, 80), (160, 20, 40)]),
    "rose":      ("mono", [(255, 200, 225), (245, 120, 170), (200, 60, 120)]),
    "lavender":  ("mono", [(225, 205, 255), (170, 130, 245), (115, 70, 200)]),
    "amber":     ("mono", [(255, 225, 150), (255, 175, 50), (200, 115, 10)]),
    "teal":      ("mono", [(170, 255, 240), (50, 210, 190), (15, 130, 125)]),
    "paper":     ("mono light", [(30, 34, 42), (70, 76, 90), (110, 116, 130)],
                  ((246, 244, 238), (234, 230, 220))),
}
TAGS = ["sea", "gradient", "mono", "light"]


def tags_of(name: str) -> list[str]:
    return THEMES[name][0].split()


def stops_of(name: str):
    return THEMES[name][1]
# ── themes:end ──

MONO_THEMES = [n for n in THEMES if "mono" in tags_of(n)]

# Wave logos (waves -i NAME, waves --icons to preview them all)
LOGOS = {
    "wave": [
        "          ⢀⡠⡤⠤⢤⠤⣀",
        "       ⢀⡤⣺⣽⣾⣾⣔⣒⣷⡡⠱⢄",
        "      ⣠⣾⣾⢯⣞⣣⢟⣹⣿⣿⣷⢋⡔⢋⠂⡄",
        "     ⣴⣟⡶⣏⡿⣔⢫⣾⣿⣿⣿⣿⣷⣷⡉⠜⠃",
        "    ⣰⡿⡞⡙⢾⢻⣌⣻⣿⣿⣿⠟⢉⢹⣷⡿⣹⠉⠓",
        "  ⢠⣤⠿⡽⢛⡧⡶⣦⣉⢹⣿⣽⣿⡄⠈⣟⡉⠚⠁⠙",
        "⠠⣴⡿⢷⠟⠍⠩⠞⢧⣭⡻⢦⡿⣿⣿⣷⣄⠈⠉",
        "⠸⢟⣡⠢⢌⠂⢇⣭⢂⢹⡿⣧⣟⢶⢭⠿⣿⣷⣤⣀⡀   ⣀⣤⣤⣤⣠⡄",
        "⠈⢶⢭⣗⣮⢻⣭⢮⢯⣳⣳⣽⣻⣟⢿⢿⣴⣯⢿⣹⣟⢿⡻⣟⠿⣭⣯⡟⠞",
        "  ⠉⠙⠛⠛⠚⠛⠛⠓⠛⠓⠛⠛⠛⠛⠛⠓⠛⠛⠛⠛⠋⠉⠉⠉",
    ],
    "moon": [
        "                       ⣀⣤⣤⣀",
        "                     ⢀⣾⣿⣿⣿⣿⣷",
        "       ⣠⠴⠒⠋⢉⡝⠲⢦⡀     ⠸⣿⣿⣿⣿⣿⣿",
        "    ⢀⡴⠚⢡⣤⣤⣴⣾⣷⣷⣨⢷⣀⡀    ⠹⢿⣿⣿⡿⠋",
        " ⢀⣠⠴⠋  ⠘⣟⡛⡽⡹⣫⣿⣴⣤⠿⣿⡆",
        "⠈⠉⠁⢰⡦⡄ ⣤⠌⣷⣷⣷⢣⠟⠛⠻⣼⣿           ⣠",
        "⢰⣾⣶⣦⢿⣭⣆⡻⣿⣿⣿⣻⣸⡀ ⠃⠿⠷⠂        ⢀⠔⠁",
        "⢸⣿⢿⣿⣎⢿⢿⣿⡿⠛⠛⠳⣿⣧⡀⠰⣿⠂       ⣠⠖⠁⢀⠾",
        " ⠙⢿⣿⣿⣿⠟⠋     ⠙⠿⣦⣄⣀⡀ ⣀⣀⣠⠴⠚⣁⡠⣾⣯⢟",
        " ⠠⣄⣀⣀⡀⠲⡄⠰⠒⠃⡴⣶⣦⡐⢄⣯⣍⡛⠛⠉⢉⡀⢀⣩⠵⠶⠛⡵⢛",
        " ⣤⣾⠛⣟⣹⣦⣒⣢⢿⣾⣧⡸⢙⠿⣶⣷⣬⣊⣳⣿⣽⣟⡟⠛⣋⣒⣓⣒⣪",
        " ⠿⠃ ⠹⠿⠿⠧⠴⠶⠾⡿⠇⠤⠕⠚⠿⠿⠟⠻⠛⠭⠥⠶⠭⠭⠤⠤⠤⠤",
    ],
    "curl": [
        "     ⢀⣀⣤⣤⣤⣀⡀",
        "    ⣰⠟⠉  ⠉⠙⠻⣶⣄",
        "    ⢏ ⠈⠉⠲⣄  ⠈⢻⣦",
        "    ⠈⠂   ⢹⡇   ⠹⣷⡀",
        "⣀⣠⣤⣀⣀⣀⣀⣀⣠⣿⠃    ⠈⠻⣦⣀",
        "   ⠈⠉⠛⠛⠛⠉         ⠉⠉⠒⠒",
    ],
    "swell": [
        "                 ⣠⣴⣶⠾⠿⠿⠯⣷⣄⡀",
        "              ⢀⣼⣾⠛⠁      ⠈⢻⣦",
        "            ⣠⣾⠿⠁   ⢀⣤⣾⣟⣛⣛⣶⣬⣿⣆",
        "          ⢀⣾⠟⠃     ⣾⣿⠟⠉⠉⠉⠉⠛⠿⠟",
        "        ⢀⣴⡟⠋       ⣿⡏⣤",
        "       ⣠⡿⠛         ⠙⣷⡍          ⢀⣀⣀⣤⣤⣤⣀",
        "     ⣠⣼⡏            ⠈⠙⠷⣤⣤⣠⣤⣤⡤⡶⣶⢿⠟⠹⠿⠄⣿⣿⠏ ⣀⣤⡦    ⣀⡄",
        "⢀⣄⣠⣶⣿⠏                  ⠈⠉⠓⠚⠋⠉      ⠈⠛⡛⡻⠿⠿⠙⠓⢒⣺⡿⠋⠁",
        "⠉⠉⠉⠛⠁                                        ⠉⠉⠁",
    ],
    "great": [
        "           ⢀⣀⣀⡀⢤⢰⡒⣌⢩⠳⡤⡄",
        "       ⢀⠠⠒⢉ ⢤ ⣀⡱⡷⠭⡻⢵⣞⢣⠴⡲⣤",
        "     ⢀⠴⠁⡄⡊⠜⡜⣜⣬⣵⣀⣓⢪⣽⡺⣥⣧⠌⡱⠣⢖",
        "    ⠠⢂⠠⢪⢎⡼⠪⠞⠟⢟⣿⣿⣿⣿⣾⣿⡿⡽⡛⢦⠙⡲⣉⠂",
        "   ⠠⢗⡵⢋⡞⡚⡴⣭⣾⣾⡗⣸⣿⣿⣿⣿⣿⠿⠟⡷⣡⣚⢴⠑⠛ ⢀ ⠄⢀⢤⢐⢶⠒⣖⣆⣤⡄",
        "  ⢀⡘⢞⠰⣹⣏⠉⣶⣿⣿⣿⣿⣿⣿⣿⣾⣿⡟   ⠁⠓⠝  ⡪⣐⢤⣫⣿⠝⣺⡱⣛⡷⣜⡬⣲⣄",
        "  ⡎⢸⡎⢒⠌⠿⢬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇     ⡠⣪⡮⣪⢣⣟⣹⢻⣿⣷⣞⣿⣿⣟⣱⡍⣟⠅",
        "⢠⠊⣈⡘⣼⠏⡜⢧⣺⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣅  ⠠⢀⣼⣽⠏⣷⣳⣿⣿⣿⣿⣿⣿⡿⠋⠉⢽⡽⢱⢚⡆",
        "⡾⣽⣶⣾⣫⢿⡬⢝⡌⣿⣿⣿⣿⡽⣿⣿⣿⣿⣿⣿⣦⡦⣹⣿⣾⠽⢺⣾⢇⡝⣿⣿⣿⣿⣿   ⠈⠫⠷⠙⠋   ⡀",
        " ⢩⡿⢿⣟⠑⢳⣯⡟⢚⣻⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣷⣌⣚⣛⣃⣤⡦⡾⣠⣤⣿⣿⣿⣿⡄  ⢀⡀ ⣠⣀⡀⢀⢤⡇",
        "⣴⠖⠈⠛⠫⡠⢄⡔⣄⢮⠞⠋⠉⢿⣿⣾⣻⣿⣿⣷⣿⣿⣿⣿⣿⣷⣹⣚⡳⢃⣶⢄⣘⢿⣿⣿⢞⡓⢧⣞⢫⣵⣎⣽⣩⣶⡇",
        "⣿⣿⡆⠠⣝⣬⡿⡇⣇⢮⢦⡘⣌⠛⢹⢿⣿⣷⣽⣻⢿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣾⣷⣦⣡⠙⣄⠦⠯⣝⣛⡹⣿⣻⢭⣽⡏",
        "⣿⡿⢁⣇⣿⣹⣟⣧⠘⢯⣖⣳⣬⡳⣤⣘⠿⣿⣿⣿⣿⣾⢯⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⡿⢿⣿⣵⢶⡾⣾⠅",
        "⠈⠠⢞⣶⢿⣿⣞⡷⣧⡈⠙⢶⣭⣟⡿⣿⣿⣶⣬⣛⡽⢻⣟⡻⢿⣽⠷⠾⣶⣿⣿⣿⣿⣿⠿⠛⠉⣰⣉⣼⣶⠯⠿⠿⠓⠊",
        "             ⠉⠉⠉⠉⠉⠉⠉⠉⠉ ⠛⠛⠂⠙⠊⠙⠛⠂⠈⠁  ⠐⠉⠁",
    ],
}

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"


class Painter:
    def __init__(self, theme: str, enabled: bool):
        self.stops = stops_of(theme)
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


# ───────────────────────────── windows probes ─────────────────────────────

IS_WIN = sys.platform == "win32"
WIN_CV = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
ARCH = {"amd64": "x86_64", "x86": "x86", "arm64": "aarch64"}


def reg(path: str, name: str):
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as k:
            return winreg.QueryValueEx(k, name)[0]
    except OSError:
        return None


def reg_subkeys(path: str) -> list[str]:
    import winreg
    out = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as k:
            i = 0
            while True:
                try:
                    out.append(winreg.EnumKey(k, i))
                except OSError:
                    break
                i += 1
    except OSError:
        pass
    return out


def win_run(cmd: list[str], timeout=6) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              creationflags=0x08000000).stdout.strip()  # CREATE_NO_WINDOW
    except (OSError, subprocess.SubprocessError):
        return ""


def win_os() -> str:
    name = reg(WIN_CV, "ProductName") or "Windows"
    try:
        build = int(reg(WIN_CV, "CurrentBuildNumber") or 0)
    except ValueError:
        build = 0
    if build >= 22000:  # Windows 11 still reports "Windows 10" in the registry
        name = name.replace("Windows 10", "Windows 11")
    version = reg(WIN_CV, "DisplayVersion") or reg(WIN_CV, "ReleaseId") or ""
    arch = ARCH.get(platform.machine().lower(), platform.machine())
    return " ".join(x for x in (name, version, arch) if x)


def win_kernel() -> str:
    major = reg(WIN_CV, "CurrentMajorVersionNumber")
    minor = reg(WIN_CV, "CurrentMinorVersionNumber")
    build = reg(WIN_CV, "CurrentBuildNumber")
    ubr = reg(WIN_CV, "UBR")
    if major is None or build is None:
        return f"Windows NT {platform.version()}"
    return f"Windows NT {major}.{minor}.{build}" + (f".{ubr}" if ubr is not None else "")


def win_uptime_seconds() -> int:
    import ctypes
    f = ctypes.windll.kernel32.GetTickCount64
    f.restype = ctypes.c_ulonglong
    return int(f() // 1000)


def win_memory():
    import ctypes

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

    st = MEMORYSTATUSEX()
    st.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st)):
        return 0, 0
    return st.ullTotalPhys - st.ullAvailPhys, st.ullTotalPhys


def win_cpu() -> str:
    key = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
    model = reg(key, "ProcessorNameString") or platform.processor() or "Unknown CPU"
    threads = os.cpu_count() or 0
    mhz = reg(key, "~MHz")
    freq = f" @ {mhz / 1000:.2f} GHz" if isinstance(mhz, int) and mhz > 0 else ""
    return f"{clean(model)} ({threads}t){freq}"


def win_gpus(limit=2) -> list[str]:
    cls = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
    gpus = []
    for sub in reg_subkeys(cls):
        if not sub.isdigit():
            continue
        name = reg(f"{cls}\\{sub}", "DriverDesc")
        if not name or re.search(r"Basic (Display|Render)|Remote|Mirror|Virtual Display|Parsec", name, re.I):
            continue
        name = re.sub(r"\((R|TM)\)", "", name).replace("Advanced Micro Devices, Inc.", "AMD").strip()
        if name not in gpus:
            gpus.append(name)
    return gpus[:limit]


def win_board() -> str:
    b = r"HARDWARE\DESCRIPTION\System\BIOS"
    vendor = reg(b, "BaseBoardManufacturer") or ""
    name = reg(b, "BaseBoardProduct") or ""
    if not name or JUNK.search(name):
        vendor, name = reg(b, "SystemManufacturer") or vendor, reg(b, "SystemProductName") or ""
    vendor = "" if JUNK.search(vendor) else vendor
    name = "" if JUNK.search(name) else name
    vendor = re.sub(r"\b(Co\.,? ?Ltd\.?|Inc\.?|Corporation|COMPUTER INC\.?)\b", "", vendor, flags=re.I).strip(" ,.")
    return f"{vendor} {name}".strip()


def win_processes() -> dict:
    """pid -> (parent pid, exe name), from a Toolhelp snapshot."""
    import ctypes
    from ctypes import wintypes

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.c_size_t),
                    ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", ctypes.c_long),
                    ("dwFlags", wintypes.DWORD), ("szExeFile", ctypes.c_wchar * 260)]

    k32 = ctypes.windll.kernel32
    k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    snap = k32.CreateToolhelp32Snapshot(0x2, 0)  # TH32CS_SNAPPROCESS
    procs = {}
    if not snap or snap == wintypes.HANDLE(-1).value:
        return procs
    e = PROCESSENTRY32W()
    e.dwSize = ctypes.sizeof(PROCESSENTRY32W)
    ok = k32.Process32FirstW(snap, ctypes.byref(e))
    while ok:
        procs[e.th32ProcessID] = (e.th32ParentProcessID, e.szExeFile.lower())
        ok = k32.Process32NextW(snap, ctypes.byref(e))
    k32.CloseHandle(snap)
    return procs


WIN_SHELLS = {"pwsh.exe": "PowerShell 7", "powershell.exe": "Windows PowerShell", "cmd.exe": "cmd",
              "nu.exe": "nushell", "bash.exe": "bash", "zsh.exe": "zsh", "fish.exe": "fish",
              "elvish.exe": "elvish", "xonsh.exe": "xonsh"}


def win_shell() -> str:
    try:
        procs = win_processes()
    except Exception:
        return ""
    chain, pid = [], os.getpid()
    for _ in range(8):
        if pid not in procs:
            break
        pid, exe = procs[pid][0], procs.get(procs[pid][0], (0, ""))[1]
        chain.append(exe)
    chain = [e for e in chain if e and not re.match(r"(python\w*|py|pythonw?|waves)\.exe$", e)]
    # waves.cmd is run by a cmd.exe shim: skip it when another shell sits above it
    if len(chain) > 1 and chain[0] == "cmd.exe" and chain[1] in WIN_SHELLS:
        chain = chain[1:]
    shell = WIN_SHELLS.get(chain[0], chain[0].removesuffix(".exe")) if chain else ""
    if os.environ.get("WT_SESSION"):
        shell += " · Windows Terminal"
    return shell


def win_disks(limit=2) -> list[dict]:
    ps = ("Get-PhysicalDisk | Select-Object FriendlyName,Size,MediaType,BusType,DeviceId "
          "| ConvertTo-Json -Compress")
    out = win_run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps])
    disks = []
    try:
        items = json.loads(out) if out else []
    except ValueError:
        items = []
    if isinstance(items, dict):
        items = [items]
    media = {"3": "HDD", "4": "SSD", "5": "SCM", "hdd": "HDD", "ssd": "SSD", "scm": "SCM"}
    for d in items:
        bus = str(d.get("BusType", "")).lower()
        kind = "NVMe" if bus in ("17", "nvme") else media.get(str(d.get("MediaType", "")).lower(), "Disk")
        if bus in ("7", "usb"):
            kind += " · USB"
        size = int(d.get("Size") or 0)
        if size > 0:
            disks.append({"name": f"disk {d.get('DeviceId', len(disks))}",
                          "model": (d.get("FriendlyName") or "").strip(), "size": size, "type": kind})
    if not disks:  # fallback: fixed drives
        import ctypes
        import string
        mask = ctypes.windll.kernel32.GetLogicalDrives()
        for i, letter in enumerate(string.ascii_uppercase):
            root = f"{letter}:\\"
            if mask >> i & 1 and ctypes.windll.kernel32.GetDriveTypeW(root) == 3:  # DRIVE_FIXED
                try:
                    disks.append({"name": f"{letter}:", "model": "", "size": shutil.disk_usage(root).total,
                                  "type": "Drive"})
                except OSError:
                    pass
    disks.sort(key=lambda d: d["size"], reverse=True)
    return disks[:limit]


def win_console() -> bool:
    """Turn on ANSI colors and UTF-8 in the Windows console. Returns True if colors work."""
    import ctypes
    k32 = ctypes.windll.kernel32
    k32.SetConsoleOutputCP(65001)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    handle = k32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
    mode = ctypes.c_ulong()
    if not k32.GetConsoleMode(handle, ctypes.byref(mode)):
        return False
    return bool(k32.SetConsoleMode(handle, mode.value | 0x0004))  # ENABLE_VIRTUAL_TERMINAL_PROCESSING


# ───────────────────────────── collect ─────────────────────────────

def format_uptime(s: int) -> str:
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m = s // 60
    return " ".join([f"{d}d"] * bool(d) + [f"{h}h"] * bool(h) + [f"{m}m"])


def collect() -> dict:
    if IS_WIN:
        drive = os.environ.get("SystemDrive", "C:")
        try:
            u = shutil.disk_usage(drive + "\\")
            root = {"used": u.used, "total": u.total, "label": drive}
        except OSError:
            root = {"used": 0, "total": 0, "label": drive}
        used, total = win_memory()
        return {
            "user": getpass.getuser(),
            "host": socket.gethostname(),
            "os": win_os(),
            "kernel": win_kernel(),
            "uptime": format_uptime(win_uptime_seconds()),
            "shell": win_shell(),
            "board": win_board(),
            "cpu": win_cpu(),
            "gpus": win_gpus(),
            "memory": {"used": used, "total": total},
            "disks": win_disks(),
            "root": root,
        }
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
        "root": {"used": rused, "total": rtotal, "label": "root"},
    }


# ───────────────────────────── render ─────────────────────────────

def bar(p: Painter, ratio: float, width=14) -> str:
    ratio = max(0.0, min(1.0, ratio))
    filled = max(round(ratio * width), 1 if ratio > 0 else 0)
    if not p.on:
        return "[" + "#" * filled + "-" * (width - filled) + "]"
    out = "".join(p.fg(p.lerp(i / max(width - 1, 1))) + "━" for i in range(filled))
    return out + RESET + p.dim("─" * (width - filled))


def paint_logo_line(p: Painter, line: str, row: int, rows: int) -> str:
    """Diagonal gradient: light crest at the top-left, deep water at the bottom-right."""
    if not p.on:
        return line
    w = max(len(line) - 1, 1)
    out = []
    for col, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        t = 0.65 * row / max(rows - 1, 1) + 0.35 * col / w
        out.append(p.fg(p.lerp(t)) + ch)
    return "".join(out) + RESET


def render(data: dict, p: Painter, show_logo=True, icon: str = "wave") -> str:
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
        entries.append(("ram", f"{human(m['used']) + ' / ' + human(m['total']):<21} "
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
        entries.append((rt.get("label", "root"), f"{human(rt['used']) + ' / ' + human(rt['total']):<21} "
                                f"{bar(p, r)} {p.dim(f'{r * 100:.0f}%')}"))

    n = len(entries)
    for i, (k, v) in enumerate(entries):
        row(k, v, i / max(n - 1, 1))

    rows.append("")
    rows.append("  ".join(p.at(i / 7, "●") for i in range(8)) if p.on else "")

    if not show_logo:
        return "\n".join(rows)

    art = LOGOS.get(icon, LOGOS["wave"])
    logo_w = max(max(len(l) for l in art), 9)
    logo = [paint_logo_line(p, l.ljust(logo_w), i, len(art)) for i, l in enumerate(art)]
    logo.append(" " * logo_w)
    left = (logo_w - 9) // 2
    logo.append(" " * left + p.gradient("w a v e s", bold=True) + " " * (logo_w - 9 - left))

    h = max(len(logo), len(rows))
    lpad = (h - len(logo)) // 2
    rpad = (h - len(rows)) // 2
    logo = [" " * logo_w] * lpad + logo + [" " * logo_w] * (h - len(logo) - lpad)
    rows = [""] * rpad + rows + [""] * (h - len(rows) - rpad)
    out = [f"  {l}   {r}".rstrip() for l, r in zip(logo, rows)]
    return "\n" + "\n".join(out) + "\n"


# ───────────────────────────── config ─────────────────────────────

def config_path() -> str:
    if IS_WIN:
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return os.path.join(base, "waves", "config")


def load_config() -> dict:
    cfg = {}
    for line in read(config_path()).splitlines():
        k, _, v = line.partition("=")
        if k.strip():
            cfg[k.strip()] = v.strip()
    return cfg


def load_theme() -> str:
    t = load_config().get("theme", "")
    return t if t in THEMES else ""


def load_icon() -> str:
    i = load_config().get("icon", "")
    return i if i in LOGOS else ""


def save_config(**values) -> None:
    cfg = load_config()
    cfg.update(values)
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(f"{k}={v}\n" for k, v in cfg.items())


# ───────────────────────────── color picker (waves -c) ─────────────────────────────

TABS = [("all", list(THEMES))] + [(tg, [n for n in THEMES if tg in tags_of(n)]) for tg in TAGS]


WIN_KEYS = {"H": "up", "P": "down", "K": "left", "M": "right", "\x0f": "btab"}


def read_key(fd: int) -> str:
    if IS_WIN:
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):  # arrows and special keys come as two characters
            return WIN_KEYS.get(msvcrt.getwch(), "")
        return {"\t": "tab", "\r": "enter", "\x1b": "quit", "q": "quit", "\x03": "quit", "r": "r", "i": "i",
                "l": "right", "h": "left", "k": "up", "j": "down"}.get(ch, "")
    b = os.read(fd, 8)
    keys = {b"\x1b[C": "right", b"\x1b[D": "left", b"\x1b[A": "up", b"\x1b[B": "down",
            b"\x1bOC": "right", b"\x1bOD": "left", b"\x1bOA": "up", b"\x1bOB": "down",
            b"\t": "tab", b"\x1b[Z": "btab", b"\r": "enter", b"\n": "enter",
            b"\x1b": "quit", b"q": "quit", b"\x03": "quit",
            b"l": "right", b"h": "left", b"k": "up", b"j": "down", b"r": "r", b"i": "i"}
    return keys.get(b, "")


def picker_frame(data: dict, tab: int, idx: int, saved: str, msg: str, icon: str = "wave") -> str:
    themes = TABS[tab][1]
    name = themes[idx]
    p = Painter(name, True)
    cols = shutil.get_terminal_size((100, 30)).columns

    # category tabs
    tabs = []
    for i, (label, _) in enumerate(TABS):
        tabs.append(p.at(0.2, f" {label} ", bold=True) if i == tab else p.dim(f" {label} "))
    head = f"  {p.gradient('waves', bold=True)} {p.dim('·')} {p.dim('themes')}     " + p.dim("│").join(tabs)

    # theme strip, scrolling around the selection
    chips = []
    for i, t in enumerate(themes):
        tp = Painter(t, True)
        dot = tp.at(0.0, "●") + tp.at(0.5, "●") + tp.at(1.0, "●")
        star = "*" if t == saved else ""
        label = tp.gradient(f"{t}{star}", bold=True) if i == idx else p.dim(f"{t}{star}")
        chips.append((f"{dot} {label}", i == idx))
    budget = cols - 8
    lo = hi = idx
    width = vlen(chips[idx][0])
    while True:
        grew = False
        if hi + 1 < len(chips) and width + vlen(chips[hi + 1][0]) + 4 <= budget:
            hi += 1; width += vlen(chips[hi][0]) + 4; grew = True
        if lo - 1 >= 0 and width + vlen(chips[lo - 1][0]) + 4 <= budget:
            lo -= 1; width += vlen(chips[lo][0]) + 4; grew = True
        if not grew:
            break
    strip = "    ".join(c for c, _ in chips[lo:hi + 1])
    left = p.dim("‹ ") if lo > 0 else "  "
    right = p.dim(" ›") if hi < len(chips) - 1 else ""
    pos = p.dim(f"{idx + 1}/{len(themes)}")

    body = render(data, p, icon=icon)
    keys = p.dim(f"←/→ theme   tab category   i logo ({icon})   r random   enter save   q quit")
    note = ("  " + p.at(0.0, msg, bold=True)) if msg else ""
    return "\n".join([
        "", head, "",
        f"  {left}{strip}{right}   {pos}",
        body,
        f"  {keys}{note}",
    ])


def color_picker(data: dict, start: str, icon: str = "wave") -> None:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        sys.exit("waves -c: needs an interactive terminal")
    if not IS_WIN:
        import termios
        import tty

    saved = load_theme()
    tab = 0
    idx = TABS[0][1].index(start) if start in TABS[0][1] else 0
    msg = ""
    fd = sys.stdin.fileno()
    old = None if IS_WIN else termios.tcgetattr(fd)
    out = sys.stdout
    out.write("\x1b[?1049h\x1b[?25l")  # alternate screen, hidden cursor
    try:
        if not IS_WIN:
            tty.setraw(fd)
        while True:
            frame = picker_frame(data, tab, idx, saved, msg, icon)
            out.write("\x1b[H\x1b[2J" + frame.replace("\n", "\r\n"))
            out.flush()
            msg = ""
            k = read_key(fd)
            themes = TABS[tab][1]
            if k in ("right", "down"):
                idx = (idx + 1) % len(themes)
            elif k in ("left", "up"):
                idx = (idx - 1) % len(themes)
            elif k in ("tab", "btab"):
                current = themes[idx]
                tab = (tab + (1 if k == "tab" else -1)) % len(TABS)
                new = TABS[tab][1]
                idx = new.index(current) if current in new else 0
            elif k == "i":
                names = list(LOGOS)
                icon = names[(names.index(icon) + 1) % len(names)] if icon in names else names[0]
            elif k == "r":
                import random
                idx = random.randrange(len(themes))
            elif k == "enter":
                saved = themes[idx]
                try:
                    save_config(theme=saved, icon=icon)
                    msg = f"✓ saved {saved} · {icon}"
                except OSError as e:
                    msg = f"error: {e}"
            elif k == "quit":
                break
    finally:
        if old is not None:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        out.write("\x1b[?25h\x1b[?1049l")
        out.flush()
    if saved:
        print(f"  default theme: {Painter(saved, True).gradient(saved, bold=True)}")


def main() -> None:
    ap = argparse.ArgumentParser(prog="waves", description="A minimal, good-looking system fetch.")
    ap.add_argument("-t", "--theme", choices=THEMES,
                    default=os.environ.get("WAVES_THEME") or load_theme() or "ocean")
    ap.add_argument("-c", "--color", action="store_true",
                    help="interactive theme picker (scroll through colors, enter to save)")
    ap.add_argument("--no-color", action="store_true", help="disable colors")
    ap.add_argument("-i", "--icon", choices=list(LOGOS), metavar="LOGO",
                    help=f"wave logo, saved as the default: {', '.join(LOGOS)}")
    ap.add_argument("--icons", action="store_true", help="preview every logo")
    ap.add_argument("--no-logo", action="store_true", help="hide the wave logo")
    ap.add_argument("--json", action="store_true", help="print raw data as JSON")
    ap.add_argument("--themes", nargs="?", const="all", metavar="TAG",
                    help="preview every theme (or only: sea, gradient, mono, light)")
    ap.add_argument("--mono-themes", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("-l", "--list-themes", action="store_true", help="list themes by category")
    ap.add_argument("-V", "--version", action="version", version=f"waves {__version__}")
    a = ap.parse_args()
    icon_note = ""
    if a.icon:  # an explicit -i becomes the new default
        if a.icon != load_icon():
            try:
                save_config(icon=a.icon)
                icon_note = a.icon
            except OSError:
                pass
    else:
        a.icon = os.environ.get("WAVES_ICON") if os.environ.get("WAVES_ICON") in LOGOS else (load_icon() or "wave")
    if a.theme not in THEMES:
        a.theme = "ocean"

    vt_ok = win_console() if IS_WIN else True
    t0 = time.perf_counter()
    data = collect()
    if a.json:
        print(json.dumps(data, indent=2))
        return
    if a.color:
        color_picker(data, a.theme, a.icon)
        return
    color = not a.no_color and (bool(os.environ.get("FORCE_COLOR"))
                                or ("NO_COLOR" not in os.environ and sys.stdout.isatty() and vt_ok))
    if a.list_themes:
        p = Painter("ocean", bool(color))
        for tg in TAGS[:3]:
            names = [n for n in THEMES if tg in tags_of(n)]
            print(f"\n  {BOLD if color else ''}{tg}{RESET if color else ''} {p.dim(str(len(names)))}")
            for name in names:
                sw = "".join(Painter(name, bool(color)).at(i / 11, "█") for i in range(12))
                light = p.dim("light") if "light" in tags_of(name) else ""
                print(f"  {name:<10} {sw}  {light}")
        print()
        return
    if a.mono_themes:
        a.themes = "mono"
    if a.themes:
        if a.themes != "all" and a.themes not in TAGS:
            sys.exit(f"waves: tags are {', '.join(TAGS)}")
        for name in [n for n in THEMES if a.themes == "all" or a.themes in tags_of(n)]:
            p = Painter(name, bool(color))
            print(f"\n  {p.gradient(name, bold=True)}")
            print(render(data, p, show_logo=not a.no_logo, icon=a.icon))
        return
    if a.icons:
        p = Painter(a.theme, bool(color))
        for name in LOGOS:
            print(f"\n  {p.gradient(name, bold=True)}  {p.dim('waves -i ' + name)}")
            print(render(data, p, icon=name))
        return
    p = Painter(a.theme, bool(color))
    print(render(data, p, show_logo=not a.no_logo, icon=a.icon))
    if icon_note:
        print(f"  {p.dim('default logo:')} {p.gradient(icon_note, bold=True)}\n")
    if os.environ.get("WAVES_DEBUG"):
        print(f"  {(time.perf_counter() - t0) * 1000:.1f} ms")


if __name__ == "__main__":
    main()
