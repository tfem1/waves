# 🌊 waves

Un *fetch* système minimaliste et joli, à la fastfetch. Un seul fichier Python, **zéro dépendance**.

```
            ⢀⡠⡤⠤⢤⠤⣀                user@host
         ⢀⡤⣺⣽⣾⣾⣔⣒⣷⡡⠱⢄              ────────────────────────
        ⣠⣾⣾⢯⣞⣣⢟⣹⣿⣿⣷⢋⡔⢋⠂⡄           os      Arch Linux x86_64
       ⣴⣟⡶⣏⡿⣔⢫⣾⣿⣿⣿⣿⣷⣷⡉⠜⠃           kernel  Linux 6.18.2
      ⣰⡿⡞⡙⢾⢻⣌⣻⣿⣿⣿⠟⢉⢹⣷⡿⣹⠉⠓          board   ASUS ROG STRIX B650-A
    ⢠⣤⠿⡽⢛⡧⡶⣦⣉⢹⣿⣽⣿⡄⠈⣟⡉⠚⠁⠙           cpu     AMD Ryzen 7 7800X3D (8c/16t)
  ⠠⣴⡿⢷⠟⠍⠩⠞⢧⣭⡻⢦⡿⣿⣿⣷⣄⠈⠉              gpu     NVIDIA GeForce RTX 4070
  ⠸⢟⣡⠢⢌⠂⢇⣭⢂⢹⡿⣧⣟⢶⢭⠿⣿⣷⣤⣀⡀   ⣀⣤⣤⣤⣠⡄   ram     9.2 GiB / 31.1 GiB    ━━━━────────── 30%
  ⠈⢶⢭⣗⣮⢻⣭⢮⢯⣳⣳⣽⣻⣟⢿⢿⣴⣯⢿⣹⣟⢿⡻⣟⠿⣭⣯⡟⠞    disk1   2.0 TB NVMe · Samsung SSD 990 PRO
    ⠉⠙⠛⠛⠚⠛⠛⠓⠛⠓⠛⠛⠛⠛⠛⠓⠛⠛⠛⠛⠋⠉⠉⠉       disk2   1.0 TB SSD · Crucial MX500
            w a v e s
```

![aperçu](preview.png)

## Infos affichées
OS / distro · kernel · uptime · shell · carte mère · CPU · GPU (jusqu'à 2) · RAM (avec barre) · disques (jusqu'à 2) · usage de `/`

## Installation
```sh
./install.sh          # installe dans ~/.local/bin/waves
```

## Utilisation
```sh
waves                 # thème ocean par défaut
waves -c              # sélecteur de couleurs interactif
waves -t sunset       # choisir un thème
waves -l              # lister les thèmes avec leur palette
waves --themes        # aperçu de tous les thèmes
waves --mono-themes   # aperçu des thèmes monochromes
waves --no-logo       # infos seules
waves --no-color
waves --json          # sortie brute en JSON
```
### Sélecteur de couleurs (`waves -c`)
Écran interactif avec aperçu en direct :

| Touche | Action |
|---|---|
| `←` `→` (ou `h` `l`, `↑` `↓`) | faire défiler les thèmes |
| `Tab` / `Shift+Tab` | changer d'onglet : tous · dégradés · mono |
| `Entrée` | sauvegarder comme thème par défaut |
| `q` / `Échap` | quitter |

Le thème est enregistré dans `~/.config/waves/config` (marqué d'une `*` dans le sélecteur).
Priorité : `-t` > `WAVES_THEME` > config > `ocean`.

### Thèmes
- **Dégradés** : `ocean` · `sunset` · `mint` · `aurora`
- **Monochromes** (une seule teinte, du clair au foncé) : `mono` · `snow` · `graphite` · `ice` · `abyss` · `matrix` · `ruby` · `rose` · `lavender` · `amber` · `teal`

Thème par défaut aussi possible via variable d'env : `export WAVES_THEME=aurora`.
Respecte `NO_COLOR`. `FORCE_COLOR=1` force les couleurs (pipe, etc.).

> Nécessite un terminal *truecolor* (Kitty, Alacritty, WezTerm, GNOME Terminal, Konsole…).
> Les noms de GPU utilisent `lspci` (paquet `pciutils`) s'il est présent, sinon un fallback via `/sys`.

## Lancer waves à l'ouverture de Kitty
```sh
./install.sh --kitty            # fish, bash et zsh détectés automatiquement
./install.sh --uninstall-kitty  # pour retirer
```
waves ne s'affiche que dans une fenêtre Kitty interactive (`$KITTY_WINDOW_ID`) : pas dans les autres terminaux, ni en SSH, ni dans les scripts.
Avec fish, le message d'accueil (`fish_greeting`) est désactivé dans Kitty pour laisser la place à waves.

Bloc ajouté à `~/.config/fish/config.fish` :
```fish
# >>> waves (kitty) >>>
if status is-interactive; and set -q KITTY_WINDOW_ID; and test -x "$HOME/.local/bin/waves"
    set -g fish_greeting
    "$HOME/.local/bin/waves"
end
# <<< waves (kitty) <<<
```
