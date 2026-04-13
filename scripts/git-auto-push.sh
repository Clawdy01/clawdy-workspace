#!/usr/bin/env bash
set -euo pipefail

REPO="/home/clawdy/.openclaw/workspace"
LOCK="/tmp/clawdy-git-auto-push.lock"
SSH_KEY="/home/clawdy/.ssh/id_ed25519_github_clawdy"
python3 - <<'PY'
from scripts.workspace_secrets import materialize_github_ssh_key
materialize_github_ssh_key('/home/clawdy/.ssh/id_ed25519_github_clawdy')
PY
BRANCH="$(git -C "$REPO" branch --show-current)"
SSH_CMD="ssh -i $SSH_KEY -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"

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

UPSTREAM="$(git -C "$REPO" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
REMOTE_BRANCH_EXISTS="$(GIT_SSH_COMMAND="$SSH_CMD" git -C "$REPO" ls-remote --heads origin "$BRANCH" 2>/dev/null || true)"

if [[ -n "$UPSTREAM" ]]; then
  AHEAD="$(git -C "$REPO" rev-list --left-right --count "$UPSTREAM...HEAD" 2>/dev/null | awk '{print $2}' || echo 0)"
else
  AHEAD="$(git -C "$REPO" rev-list --count HEAD 2>/dev/null || echo 0)"
fi

if [[ "${AHEAD:-0}" == "0" ]] && [[ -n "$UPSTREAM" ]] && [[ -z "$(git -C "$REPO" status --porcelain)" ]]; then
  echo "NO_CHANGES"
  exit 0
fi

if [[ -z "$REMOTE_BRANCH_EXISTS" ]]; then
  GIT_SSH_COMMAND="$SSH_CMD" git -C "$REPO" push -u origin "$BRANCH" >/dev/null
else
  GIT_SSH_COMMAND="$SSH_CMD" git -C "$REPO" push origin "$BRANCH" >/dev/null
  if [[ "$UPSTREAM" != "origin/$BRANCH" ]]; then
    git -C "$REPO" branch --set-upstream-to="origin/$BRANCH" "$BRANCH" >/dev/null 2>&1 || true
  fi
fi

echo "PUSHED"
