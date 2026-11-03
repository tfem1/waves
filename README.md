# 🌊 waves

Un *fetch* système minimaliste et joli, à la fastfetch. Un seul fichier Python, **zéro dépendance**.

```
        .~~.                 user@host
     .~'    '~.      .~'     ────────────────────────
  ~~'          '~~~~'        os      Arch Linux x86_64
                             kernel  Linux 6.18.2
          .~~.               uptime  2h 14m
       .~'    '~.      .~    shell   zsh
    ~~'          '~~~~'      board   ASUS ROG STRIX B650-A
                             cpu     AMD Ryzen 7 7800X3D (8c/16t) @ 5.05 GHz
            .~~.             gpu1    NVIDIA GeForce RTX 4070
         .~'    '~.     .    gpu2    AMD Raphael
      ~~'          '~~~'     ram     9.2 GiB / 31.1 GiB  ━━━━────────── 30%
                             disk1   2.0 TB NVMe · Samsung SSD 990 PRO (nvme0n1)
         w a v e s           disk2   1.0 TB SSD · Crucial MX500 (sda)
```

## Infos affichées
OS / distro · kernel · uptime · shell · carte mère · CPU · GPU (jusqu'à 2) · RAM (avec barre) · disques (jusqu'à 2) · usage de `/`

## Installation
```sh
./install.sh          # installe dans ~/.local/bin/waves
```

## Utilisation
```sh
waves                 # thème ocean par défaut
waves -t sunset       # choisir un thème
waves -l              # lister les thèmes avec leur palette
waves --themes        # aperçu de tous les thèmes
waves --mono-themes   # aperçu des thèmes monochromes
waves --no-logo       # infos seules
waves --no-color
waves --json          # sortie brute en JSON
```
### Thèmes
- **Dégradés** : `ocean` · `sunset` · `mint` · `aurora`
- **Monochromes** (une seule teinte, du clair au foncé) : `mono` · `snow` · `graphite` · `ice` · `abyss` · `matrix` · `ruby` · `rose` · `lavender` · `amber` · `teal`

Thème par défaut via variable d'env : `export WAVES_THEME=aurora`.
Respecte `NO_COLOR`. `FORCE_COLOR=1` force les couleurs (pipe, etc.).

> Nécessite un terminal *truecolor* (Kitty, Alacritty, WezTerm, GNOME Terminal, Konsole…).
> Les noms de GPU utilisent `lspci` (paquet `pciutils`) s'il est présent, sinon un fallback via `/sys`.

Pour l'afficher à chaque ouverture de terminal : ajoute `waves` à la fin de ton `~/.bashrc` / `~/.zshrc`.
