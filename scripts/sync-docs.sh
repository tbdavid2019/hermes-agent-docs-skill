#!/usr/bin/env bash
# Safely mirror official Hermes Agent documentation into this skill repository.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
UPSTREAM_REPOSITORY="https://github.com/NousResearch/hermes-agent.git"
DOCS_SOURCE="website/docs"
MINIMUM_DOCUMENTS=100
DESTINATION="$REPOSITORY_ROOT/references"
STAGING="$REPOSITORY_ROOT/.references-staging-$$"
BACKUP="$REPOSITORY_ROOT/.references-backup-$$"
REJECTED="$REPOSITORY_ROOT/.references-rejected-$$"
TEMP_ROOT=""

usage() {
    echo "Usage: $0 [--repository URL] [--docs-source PATH] [--minimum-documents N]"
}

fail() {
    echo "Error: $*" >&2
    exit 1
}

cleanup() {
    local status="$?"
    trap - EXIT

    if [ "$status" -ne 0 ] && [ -d "$BACKUP" ]; then
        if [ -d "$DESTINATION" ]; then
            mv "$DESTINATION" "$REJECTED"
        fi
        mv "$BACKUP" "$DESTINATION"
    fi

    [ ! -d "$STAGING" ] || rm -rf -- "$STAGING"
    [ ! -d "$BACKUP" ] || rm -rf -- "$BACKUP"
    [ ! -d "$REJECTED" ] || rm -rf -- "$REJECTED"
    if [ -n "$TEMP_ROOT" ] && [ -d "$TEMP_ROOT" ]; then
        rm -rf -- "$TEMP_ROOT"
    fi
    exit "$status"
}
trap cleanup EXIT

while [ "$#" -gt 0 ]; do
    case "$1" in
        --repository)
            [ "$#" -ge 2 ] || fail "--repository requires a URL or local Git path"
            UPSTREAM_REPOSITORY="$2"
            shift 2
            ;;
        --docs-source)
            [ "$#" -ge 2 ] || fail "--docs-source requires a relative path"
            DOCS_SOURCE="$2"
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
        *)
            fail "unknown argument: $1"
            ;;
    esac
done

case "$MINIMUM_DOCUMENTS" in
    ''|*[!0-9]*) fail "--minimum-documents must be a non-negative integer" ;;
esac
case "$DOCS_SOURCE" in
    /*|..|../*|*/../*|*/..) fail "--docs-source must stay inside the upstream checkout" ;;
esac

TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/hermes-docs-sync.XXXXXX")"
UPSTREAM_CHECKOUT="$TEMP_ROOT/upstream"

echo "Cloning Hermes documentation source..."
git clone --depth 1 --filter=blob:none --sparse \
    "$UPSTREAM_REPOSITORY" "$UPSTREAM_CHECKOUT"
git -C "$UPSTREAM_CHECKOUT" sparse-checkout set "$DOCS_SOURCE"

SOURCE_DIRECTORY="$UPSTREAM_CHECKOUT/$DOCS_SOURCE"
[ -d "$SOURCE_DIRECTORY" ] || fail "upstream docs directory is missing: $DOCS_SOURCE"
SOURCE_COMMIT="$(git -C "$UPSTREAM_CHECKOUT" rev-parse HEAD)"
SYNCED_AT="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"

mkdir "$STAGING"
cp -R "$SOURCE_DIRECTORY/." "$STAGING/"

if find "$STAGING" -type l -print -quit | grep -q .; then
    fail "upstream documentation contains symlinks"
fi

for required_document in \
    "getting-started/installation.md" \
    "integrations/providers.md" \
    "reference/faq.md" \
    "user-guide/configuration.md" \
    "user-guide/messaging/index.md"
do
    [ -f "$STAGING/$required_document" ] \
        || fail "required upstream document is missing: $required_document"
done

DOCUMENT_COUNT="$(
    find "$STAGING" -type f \( -name '*.md' -o -name '*.mdx' \) \
        | wc -l \
        | tr -d ' '
)"
[ "$DOCUMENT_COUNT" -ge "$MINIMUM_DOCUMENTS" ] \
    || fail "upstream document count $DOCUMENT_COUNT is below minimum $MINIMUM_DOCUMENTS"

python3 "$SCRIPT_DIR/generate_index.py" \
    --docs-dir "$STAGING" \
    --output "$STAGING/index.md" \
    --catalog "$STAGING/catalog.md" \
    --source-file "$STAGING/SOURCE.md" \
    --source-repository "$UPSTREAM_REPOSITORY" \
    --source-commit "$SOURCE_COMMIT" \
    --synced-at "$SYNCED_AT"

if [ -d "$DESTINATION" ]; then
    mv "$DESTINATION" "$BACKUP"
fi
mv "$STAGING" "$DESTINATION"

python3 "$SCRIPT_DIR/validate_repository.py" \
    --repository-root "$REPOSITORY_ROOT" \
    --minimum-documents "$MINIMUM_DOCUMENTS"

[ ! -d "$BACKUP" ] || rm -rf -- "$BACKUP"
echo "Sync complete: $DOCUMENT_COUNT upstream documents at $SOURCE_COMMIT"
