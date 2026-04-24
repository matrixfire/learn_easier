#!/usr/bin/env bash
# save_original.sh — Copy file(s) to originals/ folder, zero LLM tokens.
# Usage:
#   save_original <file>              # save one file
#   save_original <file1> <file2> …   # save multiple files
#   save_original <file> <subfolder>  # save into originals/<subfolder>/

DEST="originals"

if [ $# -eq 0 ]; then
  echo "Usage: save_original <file> [file2 …] [subfolder]"
  echo "  Files are copied to originals/ preserving their name."
  echo "  If last arg has no dot (no extension), it's used as a subfolder."
  exit 1
fi

# If the last argument looks like a subfolder (no dot in basename), peel it off
SUBFOLDER=""
ARGS=("$@")
LAST="${ARGS[-1]}"
BASENAME_LAST=$(basename "$LAST")
if [[ "$BASENAME_LAST" != *.* && ! -f "$LAST" ]]; then
  SUBFOLDER="$LAST"
  unset 'ARGS[-1]'
fi

TARGET_DIR="$DEST"
if [ -n "$SUBFOLDER" ]; then
  TARGET_DIR="$DEST/$SUBFOLDER"
fi

mkdir -p "$TARGET_DIR"

SAVED=0
for f in "${ARGS[@]}"; do
  if [ ! -f "$f" ]; then
    echo "SKIP: $f — not a file"
    continue
  fi
  NAME=$(basename "$f")
  # If a file with same name exists, append timestamp
  if [ -f "$TARGET_DIR/$NAME" ]; then
    STEM="${NAME%.*}"
    EXT="${NAME##*.}"
    TS=$(date +%Y%m%d_%H%M%S)
    DEST_PATH="$TARGET_DIR/${STEM}_${TS}.$EXT"
  else
    DEST_PATH="$TARGET_DIR/$NAME"
  fi
  cp "$f" "$DEST_PATH"
  echo "SAVED: $f → $DEST_PATH"
  SAVED=$((SAVED + 1))
done

echo "Done — $SAVED file(s) saved to $TARGET_DIR/"
