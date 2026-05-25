#!/usr/bin/env bash
# Build a Claude.ai-ready Skill bundle from this repo.
#
# Why this exists: Claude.ai Custom Skills caps uploads at 30MB AND 200
# files in the zip. The GitHub "Download ZIP" is ~70MB and the npm
# tarball is 335 files (mostly i18n/). This script produces a trimmed,
# spec-compliant bundle from the same source files `npm publish` ships.
#
# What it does:
#   1) npm pack (so the file set matches what npm publishes)
#   2) Strip i18n/ — removes ~270 files, gets us under the 200 cap
#   3) Rewrite SKILL.md for Claude.ai (≤200-char description, no broken
#      i18n/ path references)
#   4) Validate: file count ≤200, description ≤200 chars, size ≤30MB
#   5) Re-zip
#
# Output: product-playbook-claude-ai-v<version>.zip in the repo root.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION=$(node -p "require('${REPO_ROOT}/package.json').version")
BUNDLE_NAME="product-playbook-claude-ai-v${VERSION}"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

# 1) Get the npm tarball (same set of files as `npm publish`)
TARBALL=$(cd "$REPO_ROOT" && npm pack --silent --pack-destination "$WORK_DIR")

# 2) Extract — npm tarballs unpack to a "package/" directory
tar -xzf "${WORK_DIR}/${TARBALL}" -C "$WORK_DIR"

# 3) Rename so Claude.ai users see a sensibly-named folder when they unzip
mv "${WORK_DIR}/package" "${WORK_DIR}/product-playbook"

# 4) Strip i18n/ — Claude.ai caps zips at 200 files; with 6 languages we'd
#    be at ~335. The English SKILL.md at the root works multilingually
#    (Claude responds in the user's language regardless).
rm -rf "${WORK_DIR}/product-playbook/i18n"

# 5) Rewrite SKILL.md: shorten description to ≤200 chars and drop the
#    Language Detection block's references to i18n/ paths.
python3 "${REPO_ROOT}/scripts/_trim-skill-for-claude-ai.py" \
  "${WORK_DIR}/product-playbook/SKILL.md"

# 6) Validate against Claude.ai upload constraints
FILE_COUNT=$(find "${WORK_DIR}/product-playbook" -type f | wc -l)
if [ "$FILE_COUNT" -gt 200 ]; then
  echo "ERROR: bundle has $FILE_COUNT files (Claude.ai max is 200)" >&2
  exit 1
fi

DESC_LEN=$(python3 -c "
import re, sys, yaml
text = open('${WORK_DIR}/product-playbook/SKILL.md').read()
fm = re.match(r'---\n(.*?)\n---', text, re.DOTALL).group(1)
print(len(yaml.safe_load(fm)['description']))
")
if [ "$DESC_LEN" -gt 200 ]; then
  echo "ERROR: SKILL.md description is $DESC_LEN chars (Claude.ai max is 200)" >&2
  exit 1
fi

# 7) Zip it back up
(cd "$WORK_DIR" && zip -rq "${BUNDLE_NAME}.zip" product-playbook)

OUTPUT="${REPO_ROOT}/${BUNDLE_NAME}.zip"
mv "${WORK_DIR}/${BUNDLE_NAME}.zip" "$OUTPUT"

SIZE_BYTES=$(stat -c%s "$OUTPUT" 2>/dev/null || stat -f%z "$OUTPUT")
SIZE_MB=$(python3 -c "print(f'{${SIZE_BYTES}/1024/1024:.2f}')")
if python3 -c "import sys; sys.exit(0 if ${SIZE_BYTES} <= 30*1024*1024 else 1)"; then
  echo "Created: ${OUTPUT}"
  echo "  size:   ${SIZE_MB} MB  (cap 30MB)"
  echo "  files:  ${FILE_COUNT}  (cap 200)"
  echo "  descr:  ${DESC_LEN} chars  (cap 200)"
else
  echo "ERROR: bundle is ${SIZE_MB} MB (Claude.ai max is 30 MB)" >&2
  exit 1
fi
