#!/usr/bin/env bash
set -euo pipefail
for i in 1 2 3; do
  python3 scripts/mailboard.py --json >/tmp/mailboard-check-$i.json
  echo run-$i-ok
done
