#!/usr/bin/env bash
set -euo pipefail

REPO="/home/clawdy/.openclaw/workspace"
LOCK="/tmp/clawdy-git-auto-push.lock"
SSH_KEY="/home/clawdy/.ssh/id_ed25519_github_clawdy"
BRANCH="$(git -C "$REPO" branch --show-current)"

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "BUSY"
  exit 0
fi

if [[ -z "$BRANCH" ]]; then
  echo "ERROR: no branch"
  exit 1
fi

if [[ ! -f "$SSH_KEY" ]]; then
  echo "ERROR: missing ssh key"
  exit 1
fi

if [[ -n "$(git -C "$REPO" status --porcelain)" ]]; then
  git -C "$REPO" add -A
  if [[ -n "$(git -C "$REPO" diff --cached --name-only)" ]]; then
    TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"
    git -C "$REPO" commit -m "Auto-push workspace update $TS" >/dev/null
  fi
fi

if [[ -z "$(git -C "$REPO" rev-list --left-right --count "origin/$BRANCH...HEAD" 2>/dev/null || true)" ]]; then
  git -C "$REPO" remote -v >/dev/null
fi

AHEAD="$(git -C "$REPO" rev-list --left-right --count "origin/$BRANCH...HEAD" 2>/dev/null | awk '{print $2}' || echo 0)"
if [[ "${AHEAD:-0}" == "0" ]] && [[ -z "$(git -C "$REPO" status --porcelain)" ]]; then
  echo "NO_CHANGES"
  exit 0
fi

GIT_SSH_COMMAND="ssh -i $SSH_KEY -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new" \
  git -C "$REPO" push origin "$BRANCH" >/dev/null

echo "PUSHED"
