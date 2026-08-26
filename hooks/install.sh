#!/usr/bin/env bash
set -euo pipefail

# Wires git to the tracked hooks/ directory and makes sure gitleaks is present.
# Plain bash + git + curl: it never invokes the project's own toolchain, so it
# works the same in a Node, Python, Go, Rust or JVM repo. Idempotent and safe to
# re-run, so it is fine to call from a bootstrap script or an install hook.

# Hooks do nothing in CI, and a CI install step would run this on every job.
if [ -n "${CI:-}" ]; then
  exit 0
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# ---------------------------------------------------------------------------
# Guard 1 - never hijack another hook manager.
# husky and lefthook claim a repo by setting core.hooksPath themselves. Pointing
# it at hooks/ would silently stop their lint/test hooks running, with no error.
# ---------------------------------------------------------------------------
current="$(git config --get core.hooksPath || true)"
if [ -n "$current" ]; then
  case "$current" in
    /*) current_abs="$current" ;;
    *)  current_abs="$REPO_ROOT/$current" ;;
  esac
  if [ "$current_abs" != "$REPO_ROOT/hooks" ] && [ "${HOOKS_FORCE:-0}" != "1" ]; then
    echo "[hooks] REFUSING: core.hooksPath is already set to '$current'."
    echo "[hooks] Another hook manager (husky, lefthook, ...) owns this repo's hooks."
    echo "[hooks] Repointing it would silently stop those hooks from running."
    echo "[hooks] Add the gitleaks scan to that setup instead, or force with:"
    echo "[hooks]   HOOKS_FORCE=1 ./hooks/install.sh"
    exit 1
  fi
fi

# ---------------------------------------------------------------------------
# Guard 2 - core.hooksPath makes git ignore .git/hooks entirely. Anything real
# in there stops running, silently, so say so rather than let it go unnoticed.
# ---------------------------------------------------------------------------
# NOT `git rev-parse --git-path hooks` - that honours core.hooksPath, so once this
# script has run once it would report our own hooks/ back to us. --git-common-dir
# gives the real .git (and is worktree-correct, where hooks live in the common dir).
git_hooks_dir="$(git rev-parse --git-common-dir)/hooks"
shadowed="$(ls -A "$git_hooks_dir" 2>/dev/null | grep -v '\.sample$' || true)"
if [ -n "$shadowed" ]; then
  echo "[hooks] WARNING: these will stop running once core.hooksPath points at hooks/:"
  echo "$shadowed" | sed "s|^|[hooks]   $git_hooks_dir/|"
  echo "[hooks] Move anything still needed into $REPO_ROOT/hooks/."
fi

# Skip-if-missing: not every repo using this script has all five hooks, and under
# `set -e` a chmod on an absent file would abort before core.hooksPath is set.
for h in pre-commit pre-merge-commit pre-push post-commit post-checkout; do
  if [ -f "hooks/$h" ]; then chmod +x "hooks/$h"; fi
done
git config core.hooksPath hooks
echo "[hooks] git now runs $REPO_ROOT/hooks (core.hooksPath)."

# ---------------------------------------------------------------------------
# gitleaks. The pre-commit hook fails closed without it, so install it here
# rather than letting the developer discover a blocked commit later.
# ~/.local/bin is already on the hooks' PATH, so no hook change is needed.
# ---------------------------------------------------------------------------
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

if command -v gitleaks >/dev/null 2>&1; then
  echo "[hooks] gitleaks $(gitleaks version) present - secret scanning active."
  exit 0
fi

echo "[hooks] gitleaks not found - installing it..."

if command -v brew >/dev/null 2>&1 && brew install gitleaks; then
  echo "[hooks] gitleaks installed via brew."
  exit 0
fi

# Fall back to the release tarball, the same source the gitleaks CI Action uses.
case "$(uname -s)" in
  Darwin) os=darwin ;;
  Linux)  os=linux ;;
  *) os="" ;;
esac
case "$(uname -m)" in
  arm64|aarch64) arch=arm64 ;;
  x86_64|amd64)  arch=x64 ;;
  *) arch="" ;;
esac

# Never fail a bootstrap over this - warn and let the hook's own message guide them.
if [ -z "$os" ] || [ -z "$arch" ]; then
  echo "[hooks] WARNING: unsupported platform $(uname -s)/$(uname -m)."
  echo "[hooks] Install gitleaks manually: https://github.com/gitleaks/gitleaks#installing"
  exit 0
fi

ver="$(curl -sSf https://api.github.com/repos/gitleaks/gitleaks/releases/latest 2>/dev/null \
       | sed -n 's/.*"tag_name": *"v\([^"]*\)".*/\1/p' | head -1)" || ver=""
if [ -z "$ver" ]; then
  echo "[hooks] WARNING: could not reach the GitHub releases API."
  echo "[hooks] Install gitleaks manually: https://github.com/gitleaks/gitleaks#installing"
  exit 0
fi

mkdir -p "$HOME/.local/bin"
url="https://github.com/gitleaks/gitleaks/releases/download/v${ver}/gitleaks_${ver}_${os}_${arch}.tar.gz"
if curl -sSfL "$url" | tar -xz -C "$HOME/.local/bin" gitleaks 2>/dev/null; then
  chmod +x "$HOME/.local/bin/gitleaks"
  echo "[hooks] gitleaks $ver installed to ~/.local/bin."
else
  echo "[hooks] WARNING: download failed ($url)."
  echo "[hooks] Install gitleaks manually: https://github.com/gitleaks/gitleaks#installing"
fi

exit 0
