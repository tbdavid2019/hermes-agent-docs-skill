#!/bin/bash
set -e

# Configuration
REPO_URL="https://github.com/NousResearch/hermes-agent.git"
TEMP_DIR=".tmp_repo"
DOCS_SOURCE="website/docs"
DEST_DIR="references"

echo "🔄 Syncing Hermes Agent documentation..."

# Clean up
rm -rf "$TEMP_DIR"
mkdir -p "$DEST_DIR"

# Clone sparse or shallow
git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$TEMP_DIR"
cd "$TEMP_DIR"
git sparse-checkout set "$DOCS_SOURCE"
cd ..

# Copy files
echo "📂 Copying files to $DEST_DIR..."
cp -R "$TEMP_DIR/$DOCS_SOURCE/"* "$DEST_DIR/"

# Clean up
rm -rf "$TEMP_DIR"

echo "✅ Sync complete!"
