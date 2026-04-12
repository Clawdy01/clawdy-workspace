#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <input-image> <output-dir>" >&2
  exit 2
fi

INPUT="$1"
OUTDIR="$2"
mkdir -p "$OUTDIR"
BASE="$(basename "$INPUT")"
NAME="${BASE%.*}"
MASK_PNG="$OUTDIR/${NAME}.mask.png"
CUTOUT_PNG="$OUTDIR/${NAME}.cutout.png"

. /home/clawdy/.openclaw/workspace/.venv-photo/bin/activate
python - <<'PY' "$INPUT" "$CUTOUT_PNG" "$MASK_PNG"
from rembg import remove
from PIL import Image
import io, sys
src, cutout_path, mask_path = sys.argv[1], sys.argv[2], sys.argv[3]
with open(src, 'rb') as f:
    out = remove(f.read())
img = Image.open(io.BytesIO(out)).convert('RGBA')
img.save(cutout_path)
img.getchannel('A').save(mask_path)
print(cutout_path)
print(mask_path)
PY

echo "Cutout: $CUTOUT_PNG"
echo "Mask:   $MASK_PNG"
