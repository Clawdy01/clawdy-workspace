#!/usr/bin/env bash
set -Eeuo pipefail
DEFAULT_OUTDIR="/home/clawdy/.openclaw/workspace/browser-automation/out-desktop"
DEFAULT_URL="https://example.com"
KEEP_SCREENSHOTS_DEFAULT="${OPENCLAW_DESKTOP_KEEP_SCREENSHOTS:-8}"
OUTDIR=""
URL=""
DISPLAY_NAME="${OPENCLAW_DESKTOP_DISPLAY:-:99}"

START_TS="$(date +%s)"
CHECKED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
XVFB_PID=""
OB_PID=""
CH_PID=""
STARTED_XVFB=0
STARTED_OPENBOX=0
WINDOW_COUNT=0
SCREENSHOT_BASENAME="desktop"
SCREENSHOT_PATH="$OUTDIR/desktop.png"
NUMBERED_SCREENSHOT_PATH=""
CHROMIUM_BIN=""
SUCCESS=0
ERROR_MESSAGE=""
METADATA_WRITTEN=0
KEEP_SCREENSHOTS="$KEEP_SCREENSHOTS_DEFAULT"
PRUNED_SCREENSHOT_COUNT=0
LOCK_FILE="${OPENCLAW_DESKTOP_LOCK_FILE:-/tmp/openclaw-desktop-probe.lock}"
LOCK_TIMEOUT="${OPENCLAW_DESKTOP_LOCK_TIMEOUT:-120}"
LOCK_FD=""

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --keep-screenshots)
        shift
        if [[ $# -eq 0 ]]; then
          fail "--keep-screenshots vereist een getal"
        fi
        KEEP_SCREENSHOTS="$1"
        ;;
      --keep-screenshots=*)
        KEEP_SCREENSHOTS="${1#*=}"
        ;;
      --help|-h)
        cat <<'EOF'
Gebruik: desktop_probe.sh [--keep-screenshots N] [OUTDIR] [URL]

- bewaart altijd desktop.png als laatste snapshot
- bewaart daarnaast maximaal N genummerde desktop_XXX.png screenshots
EOF
        exit 0
        ;;
      *)
        if [[ -z "$OUTDIR" ]]; then
          OUTDIR="$1"
        elif [[ -z "$URL" ]]; then
          URL="$1"
        else
          fail "desktop_probe.sh accepteert hooguit één OUTDIR en één URL"
        fi
        ;;
    esac
    shift
  done

  OUTDIR="${OUTDIR:-$DEFAULT_OUTDIR}"
  URL="${URL:-$DEFAULT_URL}"

  if ! [[ "$KEEP_SCREENSHOTS" =~ ^[0-9]+$ ]]; then
    fail "--keep-screenshots moet een niet-negatief geheel getal zijn"
  fi

  mkdir -p "$OUTDIR"
}

prune_old_screenshots() {
  local keep="$1"
  local remove_list=""
  if [[ "$keep" -eq 0 ]]; then
    remove_list="$(find "$OUTDIR" -maxdepth 1 -type f -name 'desktop_[0-9][0-9][0-9].png' | sort || true)"
  else
    remove_list="$(find "$OUTDIR" -maxdepth 1 -type f -name 'desktop_[0-9][0-9][0-9].png' | sort | head -n -"$keep" || true)"
  fi
  if [[ -z "$remove_list" ]]; then
    PRUNED_SCREENSHOT_COUNT=0
    return
  fi
  PRUNED_SCREENSHOT_COUNT="$(printf '%s\n' "$remove_list" | sed '/^$/d' | wc -l | tr -d ' ')"
  while IFS= read -r old_path; do
    [[ -z "$old_path" ]] && continue
    rm -f "$old_path"
  done <<< "$remove_list"
}

parse_args "$@"
SCREENSHOT_PATH="$OUTDIR/desktop.png"

if ! [[ "$LOCK_TIMEOUT" =~ ^[0-9]+$ ]]; then
  echo "OPENCLAW_DESKTOP_LOCK_TIMEOUT moet een niet-negatief geheel getal zijn" >&2
  exit 1
fi

cleanup() {
  if [[ -n "$LOCK_FD" ]]; then
    flock -u "$LOCK_FD" 2>/dev/null || true
    eval "exec ${LOCK_FD}>&-" || true
  fi
  if [[ -n "$CH_PID" ]]; then
    kill "$CH_PID" 2>/dev/null || true
  fi
  if [[ -n "$OB_PID" && "$STARTED_OPENBOX" -eq 1 ]]; then
    kill "$OB_PID" 2>/dev/null || true
  fi
  if [[ -n "$XVFB_PID" && "$STARTED_XVFB" -eq 1 ]]; then
    kill "$XVFB_PID" 2>/dev/null || true
  fi
}

json_escape() {
  python3 -c 'import json, sys; print(json.dumps(sys.argv[1]))' "$1"
}

json_bool() {
  if [[ "${1:-0}" -eq 1 ]]; then
    printf 'true'
  else
    printf 'false'
  fi
}

next_screenshot_path() {
  local existing next
  existing="$(find "$OUTDIR" -maxdepth 1 -type f -name 'desktop_*.png' | sed 's#.*/desktop_\([0-9][0-9][0-9]\)\.png#\1#' | sort | tail -n 1)"
  if [[ -z "$existing" ]]; then
    next=0
  else
    next=$((10#$existing + 1))
  fi
  printf '%s/desktop_%03d.png' "$OUTDIR" "$next"
}

write_metadata() {
  if [[ "$METADATA_WRITTEN" -eq 1 ]]; then
    return
  fi
  local end_ts duration latest_window_list
  end_ts="$(date +%s)"
  duration=$((end_ts - START_TS))
  latest_window_list=""
  if [[ -f "$OUTDIR/windows.txt" ]]; then
    latest_window_list="$(python3 - <<'PY' "$OUTDIR/windows.txt"
from pathlib import Path
import sys
path = Path(sys.argv[1])
try:
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
except Exception:
    lines = []
print('\n'.join(lines[:10]))
PY
)"
    WINDOW_COUNT="$(python3 - <<'PY' "$OUTDIR/windows.txt"
from pathlib import Path
import sys
path = Path(sys.argv[1])
try:
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
except Exception:
    lines = []
print(len(lines))
PY
)"
  fi

  cat > "$OUTDIR/metadata.json" <<EOF
{
  "checkedAt": $(json_escape "$CHECKED_AT"),
  "url": $(json_escape "$URL"),
  "display": $(json_escape "$DISPLAY_NAME"),
  "success": $(json_bool "$SUCCESS"),
  "error": $(json_escape "$ERROR_MESSAGE"),
  "durationSeconds": $duration,
  "startedXvfb": $(json_bool "$STARTED_XVFB"),
  "startedOpenbox": $(json_bool "$STARTED_OPENBOX"),
  "chromiumBin": $(json_escape "$CHROMIUM_BIN"),
  "windowCount": $WINDOW_COUNT,
  "screenshotPath": $(json_escape "${SCREENSHOT_PATH#$OUTDIR/}"),
  "numberedScreenshotPath": $(json_escape "${NUMBERED_SCREENSHOT_PATH#$OUTDIR/}"),
  "keepScreenshots": $KEEP_SCREENSHOTS,
  "prunedScreenshotCount": $PRUNED_SCREENSHOT_COUNT,
  "windowsPreview": $(json_escape "$latest_window_list")
}
EOF
  METADATA_WRITTEN=1
}

wait_for_display() {
  local attempts="${1:-15}"
  local sleep_seconds="${2:-1}"
  local idx
  for ((idx=0; idx<attempts; idx++)); do
    if xdpyinfo -display "$DISPLAY_NAME" >/dev/null 2>&1; then
      return 0
    fi
    sleep "$sleep_seconds"
  done
  return 1
}

fail() {
  ERROR_MESSAGE="${1:-onbekende fout}"
  SUCCESS=0
  write_metadata
  exit 1
}

handle_error() {
  local lineno="${1:-unknown}"
  local exit_code="${2:-1}"
  local cmd="${3:-$BASH_COMMAND}"
  if [[ -z "$ERROR_MESSAGE" ]]; then
    ERROR_MESSAGE="desktop probe faalde op regel ${lineno}: ${cmd} (exit ${exit_code})"
  fi
  SUCCESS=0
  write_metadata
  exit "$exit_code"
}

trap cleanup EXIT
trap 'handle_error "$LINENO" "$?" "$BASH_COMMAND"' ERR

exec {LOCK_FD}>"$LOCK_FILE"
if ! flock -w "$LOCK_TIMEOUT" "$LOCK_FD"; then
  fail "desktop probe lock bleef bezet: $LOCK_FILE"
fi

export DISPLAY="$DISPLAY_NAME"
if ! xdpyinfo -display "$DISPLAY_NAME" >/dev/null 2>&1; then
  Xvfb "$DISPLAY_NAME" -screen 0 1440x1200x24 >/tmp/desktop_probe_xvfb.log 2>&1 &
  XVFB_PID=$!
  STARTED_XVFB=1
  if ! wait_for_display 15 1; then
    fail "X display ${DISPLAY_NAME} kwam niet beschikbaar na Xvfb-start; zie /tmp/desktop_probe_xvfb.log"
  fi
fi

if ! wmctrl -m >/dev/null 2>&1; then
  openbox >/tmp/desktop_probe_openbox.log 2>&1 &
  OB_PID=$!
  STARTED_OPENBOX=1
  sleep 1
fi

if ! xdpyinfo -display "$DISPLAY_NAME" >/dev/null 2>&1; then
  fail "X display ${DISPLAY_NAME} is niet bereikbaar vlak voor desktop capture"
fi

if command -v chromium-browser >/dev/null 2>&1; then
  CHROMIUM_BIN="chromium-browser"
elif command -v chromium >/dev/null 2>&1; then
  CHROMIUM_BIN="chromium"
else
  ERROR_MESSAGE='geen chromium-browser/chromium gevonden'
  write_metadata
  exit 1
fi

"$CHROMIUM_BIN" --no-sandbox --disable-dev-shm-usage "$URL" >/tmp/desktop_probe_chromium.log 2>&1 &
CH_PID=$!
sleep 4
wmctrl -l > "$OUTDIR/windows.txt" 2>"$OUTDIR/wmctrl-stderr.log" || true
xdotool search --name 'Chromium' windowactivate --sync key ctrl+l type --delay 15 "$URL" key Return 2>"$OUTDIR/xdotool-stderr.log" || true
sleep 3
NUMBERED_SCREENSHOT_PATH="$(next_screenshot_path)"
scrot "$NUMBERED_SCREENSHOT_PATH"
cp "$NUMBERED_SCREENSHOT_PATH" "$SCREENSHOT_PATH"
prune_old_screenshots "$KEEP_SCREENSHOTS"
SUCCESS=1
write_metadata

echo "$OUTDIR"
