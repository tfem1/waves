# Prompts — waves

## 1. Les prompts envoyés (dans l'ordre)

**Prompt 1**
> fesont un project le but sera d avoir une sorte de fastfetch sa dira l'os/distro le kernel et la ram et les composant graphique (ram cpu gpu 1/2 disk carte mere) je veux un design sympas le nom sera waves je veux pouvoir avoir un belle interface minimalist

**Prompt 2**
> FAIS DES THEMES MONOCHROME AUSSI

---

## 2. Prompt complet pour recréer waves d'un coup

> Crée un outil en ligne de commande nommé **waves**, une alternative minimaliste à fastfetch.
>
> **Technique**
> - Un seul fichier Python 3, sans aucune dépendance externe, exécutable (`waves.py`) + un `install.sh` qui l'installe dans `~/.local/bin/waves`.
> - Linux en priorité : lire `/etc/os-release`, `/proc/cpuinfo`, `/proc/meminfo`, `/proc/uptime`, `/sys/block`, `/sys/class/dmi/id`. Utiliser `lspci -mm` pour les GPU s'il existe, sinon fallback via `/sys/bus/pci/devices` (classe 0x03).
>
> **Infos à afficher**
> `user@host`, OS/distro + architecture, kernel, uptime, shell, carte mère (vendeur + modèle, filtrer les valeurs bidon type "To be filled by O.E.M."), CPU (modèle nettoyé, cœurs/threads, fréquence max), GPU 1 et 2, RAM utilisée/totale avec barre et pourcentage, disque 1 et 2 (taille, type NVMe/SSD/HDD, modèle ; ignorer loop/zram/ram), usage de la partition `/` avec barre.
>
> **Design**
> - Logo ASCII à gauche : trois lignes de vagues empilées (`.~~.` / `.~'    '~.` / `~~'    '~~~'`), avec « w a v e s » en dessous. Infos alignées à droite, centrées verticalement.
> - Couleurs truecolor en dégradé : le logo, le titre et les libellés suivent un dégradé ; les valeurs restent en couleur normale ; les détails secondaires en atténué (dim).
> - Barres d'usage fines `━━━━──────` en dégradé, alignées entre elles.
> - Une ligne de 8 points `●` de la palette en bas.
>
> **Thèmes**
> - Dégradés : `ocean` (défaut, cyan → bleu → violet), `sunset`, `mint`, `aurora`.
> - Monochromes (une seule teinte, du clair au foncé, lisibles sur fond sombre) : `mono`, `snow`, `graphite`, `ice`, `abyss`, `matrix`, `ruby`, `rose`, `lavender`, `amber`, `teal`.
>
> **Options CLI**
> `-t/--theme`, `-l/--list-themes` (nom + échantillon de couleur), `--themes` (aperçu de tous), `--mono-themes` (aperçu des monochromes), `--no-logo`, `--no-color`, `--json`, `-V/--version`. Thème par défaut via `WAVES_THEME`. Respecter `NO_COLOR`, `FORCE_COLOR=1` force les couleurs, pas de couleur si la sortie n'est pas un terminal.
>
> Ajoute un README en français avec un exemple de sortie, l'installation, les options et la liste des thèmes.
