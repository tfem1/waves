#!/usr/bin/env sh
# Installs waves into ~/.local/bin (or $PREFIX/bin)
set -e
DEST="${PREFIX:-$HOME/.local}/bin"
mkdir -p "$DEST"
install -m 755 "$(dirname "$0")/waves.py" "$DEST/waves"
echo "waves installed to $DEST/waves"
case ":$PATH:" in *":$DEST:"*) ;; *) echo "note: add $DEST to your PATH";; esac
