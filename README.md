# 🌊 waves

A minimal, good-looking system fetch, in the spirit of fastfetch. One Python file, **zero dependencies**, for **Linux and Windows**.

![preview](preview.png)

## What it shows
OS / distro · kernel · uptime · shell · motherboard · CPU · GPU (up to 2) · RAM (with a bar) · disks (up to 2) · `/` usage

## Install
### Linux
```sh
./install.sh            # installs ~/.local/bin/waves
./install.sh --kitty    # also show waves whenever Kitty opens
```

### Windows
Needs Python 3 (`winget install Python.Python.3.12`). In PowerShell, from the waves folder:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1            # adds the waves command
powershell -ExecutionPolicy Bypass -File install.ps1 -Startup   # also show waves when PowerShell opens
powershell -ExecutionPolicy Bypass -File install.ps1 -Uninstall
```
On Windows, waves reads the registry and the Windows API (and `Get-PhysicalDisk` for NVMe / SSD / HDD), detects PowerShell 7, Windows PowerShell, cmd or nushell, and stores its config in `%APPDATA%\waves`.
Use **Windows Terminal** with a font that has braille glyphs (Cascadia Mono, JetBrains Mono) for the logo.

## Usage
```sh
waves                   # default theme
waves -c                # interactive theme picker
waves -t reef           # pick a theme
waves -l                # list themes by category
waves --themes sea      # preview a category (sea, gradient, mono, light) or all
waves --no-logo
waves --no-color
waves --json            # raw data
```

### Theme picker (`waves -c`)
| Key | Action |
|---|---|
| `←` `→` | browse themes |
| `Tab` / `Shift+Tab` | switch category: all · sea · gradient · mono · light |
| `r` | random theme |
| `Enter` | save as default (`~/.config/waves/config`) |
| `q` / `Esc` | quit |

Priority: `-t` > `WAVES_THEME` > saved config > `ocean`.

### Themes (40)
- **sea** — `tsunami` `ocean` `lagoon` `reef` `deepsea` `biolume` `seafoam` `kelp` `storm` `arctic` `tropic` `riptide` `maelstrom` `nautilus` `pearl` `sandbar`
- **gradient** — `sunset` `mint` `aurora` `synthwave` `dusk` `candy` `ember` `forest` `nebula` `citrus` `vapor` `peach`
- **mono** — `mono` `snow` `graphite` `ice` `abyss` `matrix` `ruby` `rose` `lavender` `amber` `teal` `paper`
- **light** (for light terminals) — `pearl` `sandbar` `peach` `paper`

Respects `NO_COLOR`; `FORCE_COLOR=1` forces colors. Needs a truecolor terminal and a font with braille glyphs (JetBrains Mono, Nerd Fonts, DejaVu, Fira Code…). GPU names use `lspci` (`pciutils`) when available.

## Autostart in Kitty
```sh
./install.sh --kitty            # fish, bash and zsh are detected
./install.sh --uninstall-kitty  # remove it
```
waves only shows up in interactive Kitty windows (`$KITTY_WINDOW_ID`): not in other terminals, over SSH, or in scripts. With fish, the greeting is turned off in those windows.

Block added to `~/.config/fish/config.fish`:
```fish
# >>> waves (kitty) >>>
if status is-interactive; and set -q KITTY_WINDOW_ID; and test -x "$HOME/.local/bin/waves"
    set -g fish_greeting
    "$HOME/.local/bin/waves"
end
# <<< waves (kitty) <<<
```
