#!/usr/bin/env bash
set -euo pipefail
cd /home/clawdy/.openclaw/workspace
python3 /usr/lib/python3.12/py_compile.py scripts/mail-dispatch.py scripts/command-dispatch.py
python3 scripts/mail-dispatch.py catalog --json > tmp/mail-dispatch-catalog-check.json
python3 scripts/command-dispatch.py --json-help > tmp/command-dispatch-help-check.json
grep -q '"thread-now"' tmp/mail-dispatch-catalog-check.json
grep -q '"thread-review"' tmp/mail-dispatch-catalog-check.json
grep -q '"/mail-thread-now"' tmp/command-dispatch-help-check.json
grep -q '"/mail-thread-review"' tmp/command-dispatch-help-check.json
python3 scripts/command-dispatch.py /mail-thread-now --json -n 1 > tmp/mail-thread-now-check.json
python3 scripts/command-dispatch.py /mail-thread-review --json -n 1 > tmp/mail-thread-review-check.json
