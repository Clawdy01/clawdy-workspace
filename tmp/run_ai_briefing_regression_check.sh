#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-regression-check.py
python3 scripts/ai-briefing-status.py --summary-file tmp/ai-briefing-invalid-bron-with-urls-sample.txt --json > /tmp/ai-invalid.json
python3 scripts/ai-briefing-regression-check.py
python3 - <<'PY'
import json
from pathlib import Path
j=json.loads(Path('/tmp/ai-invalid.json').read_text())
print('MULTI', j['items_with_multiple_sources_count'], j['first3_items_with_multiple_sources_count'])
print('TEXT', j['text'])
PY
