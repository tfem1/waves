#!/usr/bin/env sh
# waves installer for Linux (Windows: install.ps1)
# Installs waves into ~/.local/bin (or $PREFIX/bin).
#   ./install.sh                     install the waves command
#   ./install.sh --kitty             + show waves when Kitty opens
#   ./install.sh --uninstall-kitty   remove the autostart
#   ./install.sh --uninstall         remove waves and the autostart
# One-liner (downloads waves.py from GitHub):
#   curl -fsSL https://raw.githubusercontent.com/tfem1/waves/main/install.sh | sh
#   curl -fsSL https://raw.githubusercontent.com/tfem1/waves/main/install.sh | sh -s -- --kitty
set -e
DEST="${PREFIX:-$HOME/.local}/bin"
SRC_URL="${WAVES_SRC:-https://raw.githubusercontent.com/tfem1/waves/main/waves.py}"
MARK="# >>> waves (kitty) >>>"
END="# <<< waves (kitty) <<<"

add_block() {  # $1 = rc file, $2 = block content
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
    --uninstall-kitty|--uninstall)
        remove_block "$HOME/.bashrc"; remove_block "$HOME/.zshrc"; remove_block "$FISH_RC"
        if [ "$1" = "--uninstall" ]; then
            rm -f "$DEST/waves"
            echo "waves uninstalled (config kept in ~/.config/waves)"
        fi
        exit 0 ;;
esac

command -v python3 >/dev/null 2>&1 || echo "warning: python3 was not found, waves needs it"

# use waves.py next to this script (git clone), or download it (curl | sh)
HERE="$(cd "$(dirname "$0")" 2>/dev/null && pwd || true)"
mkdir -p "$DEST"
if [ -n "$HERE" ] && [ -f "$HERE/waves.py" ]; then
    install -m 755 "$HERE/waves.py" "$DEST/waves"
else
    echo "downloading waves…"
    TMP="$(mktemp)"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$SRC_URL" -o "$TMP"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$TMP" "$SRC_URL"
    else
        echo "error: curl or wget is needed to download waves"; rm -f "$TMP"; exit 1
    fi
    head -1 "$TMP" | grep -q python || { echo "error: download failed"; rm -f "$TMP"; exit 1; }
    install -m 755 "$TMP" "$DEST/waves"
    rm -f "$TMP"
fi
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
