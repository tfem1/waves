# Prompts

## 1. The prompts that built waves (verbatim, in order)

1. > fesont un project le but sera d avoir une sorte de fastfetch sa dira l'os/distro le kernel et la ram et les composant graphique (ram cpu gpu 1/2 disk carte mere) je veux un design sympas le nom sera waves je veux pouvoir avoir un belle interface minimalist
2. > FAIS DES THEMES MONOCHROME AUSSI
3. > envoie les prompt
4. > waves.py
5. > fais un onglet en mode waves -c pour color et je peux faire defiler les couleur
6. > ameliore le logo : *(braille wave art)*
7. > je veux que waves souvre quand j open kitty
8. > fish shell
9. > pas mal mais ajoute y quelque chose quand meme plus de themes et plus d option rend le bien mieux fais des themes avec gradience et en themes avec la mere et rend le tout en anglais et ajoute des specificiter

---

## 2. One prompt to rebuild waves

> Build **waves**, a zero-dependency, single-file Python system fetch like fastfetch, for Linux and Windows, in English. Show user@host, OS/distro, kernel, uptime, shell, motherboard, CPU, up to 2 GPUs, RAM with a gradient bar, up to 2 disks and system-drive usage. Draw a braille wave logo on the left with a diagonal truecolor gradient and "w a v e s" under it. Ship 40 themes in 4 categories (sea, gradient, mono, light; each theme = 3 accent colors). Options: `-t`, `-c` (full-screen theme picker with category tabs, random, save to config), `-l`, `--themes [tag]`, `--no-logo`, `--no-color`, `--json`. Respect NO_COLOR / FORCE_COLOR. On Linux read /proc and /sys; on Windows use the registry, the Windows API and `Get-PhysicalDisk`, and enable ANSI + UTF-8 in the console. `install.sh --kitty` adds an autostart block for fish/bash/zsh that only runs in interactive Kitty windows; `install.ps1 -Startup` does the same for PowerShell.
