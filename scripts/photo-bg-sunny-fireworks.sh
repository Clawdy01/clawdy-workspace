#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <input-image> <output-image>" >&2
  exit 2
fi

INPUT="$1"
OUTPUT="$2"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

MASK_SCRIPT="/home/clawdy/.openclaw/workspace/scripts/photo-mask-bg-edit.sh"
"$MASK_SCRIPT" "$INPUT" "$WORKDIR" >/dev/null
BASE="$(basename "$INPUT")"
NAME="${BASE%.*}"
MASK="$WORKDIR/${NAME}.mask.png"
INV_MASK="$WORKDIR/${NAME}.mask.invert.png"
BG_ONLY="$WORKDIR/${NAME}.bg.jpg"
SUN_BG="$WORKDIR/${NAME}.bg.sun.jpg"
FW="$WORKDIR/fireworks.png"

# invert mask: white = editable background, black = protected subject
convert "$MASK" -negate "$INV_MASK"

# create a sunnier/bluer background version using imagemagick, then apply only to background via mask
convert "$INPUT" \
  -modulate 112,110,100 \
  -fill 'rgba(255,220,140,0.12)' -draw 'rectangle 0,0 10000,900' \
  -fill 'rgba(80,150,255,0.16)' -draw 'rectangle 0,0 10000,650' \
  -brightness-contrast 8x10 \
  "$SUN_BG"

convert "$INPUT" "$SUN_BG" "$INV_MASK" -compose over -composite "$BG_ONLY"

# make transparent fireworks overlay
convert -size 1536x1024 xc:none \
  -stroke 'rgba(255,90,90,0.85)' -strokewidth 3 \
  -draw 'line 1160,170 1195,170 line 1160,170 1125,170 line 1160,170 1160,135 line 1160,170 1160,205 line 1160,170 1185,145 line 1160,170 1135,145 line 1160,170 1185,195 line 1160,170 1135,195' \
  -stroke 'rgba(80,210,255,0.85)' -strokewidth 3 \
  -draw 'line 1030,125 1060,125 line 1030,125 1000,125 line 1030,125 1030,95 line 1030,125 1030,155 line 1030,125 1052,103 line 1030,125 1008,103 line 1030,125 1052,147 line 1030,125 1008,147' \
  -stroke 'rgba(255,220,90,0.82)' -strokewidth 3 \
  -draw 'line 1330,260 1362,260 line 1330,260 1298,260 line 1330,260 1330,228 line 1330,260 1330,292 line 1330,260 1353,237 line 1330,260 1307,237 line 1330,260 1353,283 line 1330,260 1307,283' \
  -blur 0x0.6 "$FW"

# place fireworks only on sky/background, keep subject protected
convert "$FW" "$INV_MASK" -compose CopyOpacity -composite "$FW"
convert "$BG_ONLY" "$FW" -compose over -composite "$OUTPUT"

echo "$OUTPUT"
