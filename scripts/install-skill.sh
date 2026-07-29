#!/usr/bin/env bash
# Install, update, or validate an update-capable Hermes documentation skill checkout.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_REPOSITORY="https://github.com/tbdavid2019/hermes-agent-docs-skill.git"
REPOSITORY="$DEFAULT_REPOSITORY"
MINIMUM_DOCUMENTS=100
CHECK_ONLY=false
TARGET_DIR=""

usage() {
    echo "Usage: $0 [--check] [--repository URL] [--minimum-documents N] [TARGET_DIR]"
    echo
    echo "With no TARGET_DIR, validates or updates the checkout containing this script."
}

fail() {
    echo "Error: $*" >&2
    exit 1
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --check)
            CHECK_ONLY=true
            shift
            ;;
        --repository)
            [ "$#" -ge 2 ] || fail "--repository requires a URL or local Git path"
            REPOSITORY="$2"
            shift 2
            ;;
        --minimum-documents)
            [ "$#" -ge 2 ] || fail "--minimum-documents requires a number"
            MINIMUM_DOCUMENTS="$2"
            shift 2
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        -*)
            fail "unknown option: $1"
            ;;
        *)
            [ -z "$TARGET_DIR" ] || fail "only one TARGET_DIR may be supplied"
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

case "$MINIMUM_DOCUMENTS" in
    ''|*[!0-9]*) fail "--minimum-documents must be a non-negative integer" ;;
esac

TARGET_DIR="${TARGET_DIR:-$REPOSITORY_ROOT}"
[ -n "$TARGET_DIR" ] || fail "target directory cannot be empty"
[ "$TARGET_DIR" != "/" ] || fail "refusing to use the filesystem root as TARGET_DIR"
[ "$TARGET_DIR" != "${HOME:-}" ] || fail "refusing to use the home directory as TARGET_DIR"

validate_installation() {
    local target="$1"
    [ -f "$target/SKILL.md" ] || fail "SKILL.md is missing from $target"
    [ -f "$target/scripts/validate_repository.py" ] \
        || fail "repository validator is missing from $target"
    python3 "$target/scripts/validate_repository.py" \
        --repository-root "$target" \
        --minimum-documents "$MINIMUM_DOCUMENTS"
}

if [ "$CHECK_ONLY" = true ]; then
    [ -d "$TARGET_DIR/.git" ] \
        || fail "$TARGET_DIR is not a Git checkout; it cannot receive updates"
    validate_installation "$TARGET_DIR"
    echo "Installation verified: $TARGET_DIR"
    exit 0
fi

if [ ! -e "$TARGET_DIR" ]; then
    mkdir -p "$(dirname "$TARGET_DIR")"
    git clone "$REPOSITORY" "$TARGET_DIR"
    validate_installation "$TARGET_DIR"
    echo "Installation verified: $TARGET_DIR"
    exit 0
fi

if [ ! -d "$TARGET_DIR/.git" ]; then
    if [ -d "$TARGET_DIR" ] \
        && [ -z "$(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -print -quit)" ]; then
        rmdir "$TARGET_DIR"
        git clone "$REPOSITORY" "$TARGET_DIR"
        validate_installation "$TARGET_DIR"
        echo "Installation verified: $TARGET_DIR"
        exit 0
    fi
    fail "$TARGET_DIR exists but is not a Git checkout; refusing to overwrite it"
fi

ORIGIN_URL="$(git -C "$TARGET_DIR" remote get-url origin)"
[ "$ORIGIN_URL" = "$REPOSITORY" ] \
    || fail "origin mismatch for $TARGET_DIR (expected '$REPOSITORY', found '$ORIGIN_URL')"

if ! CURRENT_BRANCH="$(git -C "$TARGET_DIR" symbolic-ref --quiet --short HEAD)"; then
    fail "$TARGET_DIR is in detached HEAD state; switch to a branch before updating"
fi

git -C "$TARGET_DIR" pull --ff-only origin "$CURRENT_BRANCH"
validate_installation "$TARGET_DIR"
echo "Update verified: $TARGET_DIR"
