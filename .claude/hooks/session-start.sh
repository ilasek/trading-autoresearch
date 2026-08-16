#!/bin/bash
# SessionStart hook for trading-autoresearch.
#
# Two jobs:
#   1. Provision .venv so the engine tests and run_experiment.py work immediately.
#   2. Guard research integrity: warn loudly if this session is starting from a
#      stale base or if a previous session's work never landed on main.
#
# Job 2 exists because of the 2026-08-16 protocol issue: the nightly routine
# pushed to per-run branches for four nights, so each session ran blind to the
# others, 19 trials never reached main, and every deflated-Sharpe bar computed in
# those sessions was understated. See the protocol issue entry in
# experiments/journal.md.
#
# This hook never exits non-zero on a policy problem — it prints a warning into
# the session context and lets the agent decide. A hard failure here would strand
# every session, including ones opened to fix the problem.

set -uo pipefail

# Web/remote sessions only; local dev keeps its own environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || echo .)}" || exit 0

# ---------------------------------------------------------------- dependencies
# Keyed on the requirements hash so a cached container skips reinstalling.
REQ_HASH="$(sha256sum requirements.txt 2>/dev/null | cut -d' ' -f1)"
STAMP=".venv/.requirements-sha256"

if [ ! -x .venv/bin/python ]; then
  echo "[session-start] creating .venv"
  python3 -m venv .venv || echo "[session-start] WARNING: venv creation failed"
fi

if [ -x .venv/bin/python ]; then
  if [ ! -f "$STAMP" ] || [ "$(cat "$STAMP" 2>/dev/null)" != "$REQ_HASH" ]; then
    echo "[session-start] installing requirements"
    if .venv/bin/pip install -q -r requirements.txt; then
      echo "$REQ_HASH" > "$STAMP"
    else
      echo "[session-start] WARNING: pip install failed — tests may not run"
    fi
  else
    echo "[session-start] requirements already satisfied"
  fi
fi

echo 'export PATH="'"$PWD"'/.venv/bin:$PATH"' >> "${CLAUDE_ENV_FILE:-/dev/null}" 2>/dev/null || true

# ----------------------------------------------------------- integrity guard
git fetch origin --prune --quiet 2>/dev/null || {
  echo "[session-start] NOTE: git fetch failed; skipping integrity check"
  exit 0
}

WARN=""

HEAD_SHA="$(git rev-parse HEAD 2>/dev/null)"
MAIN_SHA="$(git rev-parse origin/main 2>/dev/null)"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"

# Behind origin/main: this session cannot see the latest recorded trials.
if [ -n "$HEAD_SHA" ] && [ -n "$MAIN_SHA" ] && [ "$HEAD_SHA" != "$MAIN_SHA" ]; then
  if git merge-base --is-ancestor "$HEAD_SHA" "$MAIN_SHA" 2>/dev/null; then
    BEHIND="$(git rev-list --count "$HEAD_SHA..$MAIN_SHA" 2>/dev/null)"
    WARN="${WARN}  - HEAD is ${BEHIND} commit(s) BEHIND origin/main (on '${BRANCH}').
    Run: git checkout main && git reset --hard origin/main
"
  fi
fi

# Unmerged non-archive branches: a previous session's work never landed.
STRAY="$(git branch -r --no-merged origin/main 2>/dev/null \
         | sed 's/^[ *]*//' \
         | grep -v -E '^origin/(HEAD|archive/)' || true)"

if [ -n "$STRAY" ]; then
  WARN="${WARN}  - Remote branches hold commits absent from origin/main:
$(echo "$STRAY" | sed 's/^/      /')
    A prior session's trials may never have reached main. Do NOT run new
    experiments until this is resolved — a split trial history silently
    understates the deflated-Sharpe bar for every later trial.
"
fi

if [ -n "$WARN" ]; then
  cat <<BANNER

================================================================================
RESEARCH INTEGRITY WARNING — read before running any experiment
================================================================================
${WARN}
Precedent: on 2026-08-12..15 the nightly routine pushed to per-run branches.
Four sessions each ran blind to the others, 19 trials never reached main, and
residual momentum was independently re-tested four times across three nights.
Every DSR recorded in those sessions was scored against an understated bar.

If you cannot resolve this, append a '## Protocol issue' entry to
experiments/journal.md describing what you found, commit, push, and stop.
================================================================================

BANNER
else
  echo "[session-start] integrity check OK — on main, level with origin/main, no stray branches"
fi

exit 0
