#!/usr/bin/env bash
# Build a Claude.ai-ready Skill bundle from this repo.
#
# Why this exists: Claude.ai Custom Skills upload limit is 30MB, but the
# GitHub "Download ZIP" is ~70MB because of demo GIFs in assets/. The bundle
# strips everything that is not part of the skill itself.
#
# Single source of truth: this script runs `npm pack` and re-packages the
# result, so the bundle contents == what `npm publish` ships. Maintaining
# the file list happens in package.json "files" only.
#
# Output: product-playbook-claude-ai-v<version>.zip in the repo root.

set -euo pipefail

VERSION=$(node -p "require('./package.json').version")
BUNDLE_NAME="product-playbook-claude-ai-v${VERSION}"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

# 1) Get the npm tarball (same set of files as `npm publish`)
TARBALL=$(npm pack --silent --pack-destination "$WORK_DIR")

# 2) Extract — npm tarballs unpack to a "package/" directory
tar -xzf "${WORK_DIR}/${TARBALL}" -C "$WORK_DIR"

# 3) Rename "package/" -> "product-playbook/" so Claude.ai users get a
#    sensibly-named folder when they unzip
mv "${WORK_DIR}/package" "${WORK_DIR}/product-playbook"

# 4) Zip it back up
(cd "$WORK_DIR" && zip -rq "${BUNDLE_NAME}.zip" product-playbook)

# 5) Move to repo root
OUTPUT="${PWD}/${BUNDLE_NAME}.zip"
mv "${WORK_DIR}/${BUNDLE_NAME}.zip" "$OUTPUT"

SIZE=$(du -h "$OUTPUT" | cut -f1)
echo "Created: ${OUTPUT} (${SIZE})"
