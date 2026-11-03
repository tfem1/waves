#!/usr/bin/env sh
# waves installer for Linux (Windows: install.ps1)
# Installs waves into ~/.local/bin (or $PREFIX/bin).
#   ./install.sh                     install the waves command
#   ./install.sh --kitty             + show waves when Kitty opens
#   ./install.sh --uninstall-kitty   remove the autostart
set -e
DEST="${PREFIX:-$HOME/.local}/bin"
MARK="# >>> waves (kitty) >>>"
END="# <<< waves (kitty) <<<"

add_block() {  # $1 = fichier rc, $2 = contenu
    [ -f "$1" ] || { mkdir -p "$(dirname "$1")"; : > "$1"; }
    if grep -qF "$MARK" "$1"; then
        sed -i.bak "/$MARK/,/$END/d" "$1" && rm -f "$1.bak"   # refresh the block
        echo "  updated : $1"
    else
        echo "  added   : $1"
    fi
    printf '\n%s\n%s\n%s\n' "$MARK" "$2" "$END" >> "$1"
}

remove_block() {
    [ -f "$1" ] && grep -qF "$MARK" "$1" || return 0
    sed -i.bak "/$MARK/,/$END/d" "$1" && rm -f "$1.bak"
    echo "  removed : $1"
}

FISH_RC="${XDG_CONFIG_HOME:-$HOME/.config}/fish/config.fish"

case "$1" in
    --uninstall-kitty)
        remove_block "$HOME/.bashrc"; remove_block "$HOME/.zshrc"; remove_block "$FISH_RC"
        exit 0 ;;
esac

mkdir -p "$DEST"
install -m 755 "$(dirname "$0")/waves.py" "$DEST/waves"
echo "waves installed to $DEST/waves"
case ":$PATH:" in *":$DEST:"*) ;; *) echo "note: add $DEST to your PATH";; esac

if [ "$1" = "--kitty" ]; then
    echo "autostart in Kitty:"
    SH_BLOCK="if [ -n \"\$KITTY_WINDOW_ID\" ] && [[ \$- == *i* ]] && [ -x \"$DEST/waves\" ]; then
    \"$DEST/waves\"
fi"
    FISH_BLOCK="if status is-interactive; and set -q KITTY_WINDOW_ID; and test -x \"$DEST/waves\"
    set -g fish_greeting  # waves replaces the fish greeting
    \"$DEST/waves\"
end"
    found=0
    if [ -f "$HOME/.bashrc" ] || [ "$(basename "${SHELL:-}")" = bash ]; then add_block "$HOME/.bashrc" "$SH_BLOCK"; found=1; fi
    if [ -f "$HOME/.zshrc" ]  || [ "$(basename "${SHELL:-}")" = zsh ];  then add_block "$HOME/.zshrc"  "$SH_BLOCK"; found=1; fi
    if [ -f "$FISH_RC" ]      || [ "$(basename "${SHELL:-}")" = fish ]; then add_block "$FISH_RC" "$FISH_BLOCK"; found=1; fi
    [ "$found" = 1 ] || echo "  no shell found (bash/zsh/fish)"
    echo "open a new Kitty window to see waves 🌊"
fi
