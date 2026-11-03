# Prompts

## 1. The prompts that built waves and tsunami (verbatim, in order)

1. > fesont un project le but sera d avoir une sorte de fastfetch sa dira l'os/distro le kernel et la ram et les composant graphique (ram cpu gpu 1/2 disk carte mere) je veux un design sympas le nom sera waves je veux pouvoir avoir un belle interface minimalist
2. > FAIS DES THEMES MONOCHROME AUSSI
3. > envoie les prompt
4. > waves.py
5. > fais un onglet en mode waves -c pour color et je peux faire defiler les couleur
6. > ameliore le logo fais plutot un tsunami : *(braille tsunami art)*
7. > je veux que waves souvre quand j open kitty
8. > fish shell
9. > creer mon propre terminal je veux quelque chose de sobre et vraiment tres minimalist mais avec de belle custom un peux comme waves du genre on va l appeler tsunami et je veux quil yest des commande tsunami -c ect jai confiance en toi!
10. > pas mal mais ajoute y quelque chose quand meme plus de themes et plus d option rend le bien mieux fais des themes avec gradience et en themes avec la mere et rend le tout en anglais et ajoute des specificiter

---

## 2. One prompt to rebuild both projects

> Build two companion Linux tools in English, sharing one table of 40 themes (categories: sea, gradient, mono, light; each theme = 3 accent colors, light themes also get a background pair).
>
> **waves** — a zero-dependency, single-file Python system fetch like fastfetch. Show user@host, OS/distro, kernel, uptime, shell, motherboard, CPU, up to 2 GPUs, RAM with a gradient bar, up to 2 disks and `/` usage. Draw a braille tsunami logo on the left with a diagonal truecolor gradient and "w a v e s" under it. Options: `-t`, `-c` (full-screen theme picker with category tabs, random, save to config), `-l`, `--themes [tag]`, `--no-logo`, `--no-color`, `--json`. Respect NO_COLOR / FORCE_COLOR. Inside the tsunami terminal, follow the window theme. `install.sh --kitty` adds an autostart block for fish/bash/zsh that only runs in interactive Kitty or tsunami windows.
>
> **tsunami** — a quiet, minimalist GTK3 + VTE terminal (Python, PyGObject, pycairo). No scrollbar, menus or tabs. Gradient backgrounds drawn behind VTE (`set_clear_background(False)`): linear with angle, radial glow, or solid, with intensity and opacity. Build a full 16-color palette per theme. Live config reload for every window. CLI: `-c` theme picker, `-f` font picker, `-s` settings menu, `-l [tag]`, `-t` (also random, random:tag, auto day/night), `--font`, `--set`, `--get`, `--export kitty|alacritty|foot|ghostty`, `--reset`, `--config`, `-e`. Window features: wave/flash visual bell, toasts, scrollback search, focus dimming, copy on select, new window in the same directory, per-window theme cycling and random, opacity and background cycling, zoom, fullscreen, ctrl+click links. Ship an installer with an SVG icon and a .desktop entry.
