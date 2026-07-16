#!/usr/bin/env bash
# Build a Claude.ai-ready custom skill bundle from this repo.
#
# Claude.ai Custom Skills caps uploads at 30MB, 200 files, and a 200-char
# frontmatter description. This script assembles ONE skill folder straight
# from the lens-architecture sources:
#
#   product-playbook/
#     SKILL.md          adapted meta-skill (scripts/_adapt_claude_ai_bundle.py)
#     lenses/<name>.md  one body-only doc per lens skill
#     recipes/<name>.md copied from references/recipes/
#     assets/<file>     copied from skills/document-export/assets/
#
# Output: product-playbook-claude-ai-v<version>.zip in the repo root.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION=$(node -p "require('${REPO_ROOT}/package.json').version")
BUNDLE_NAME="product-playbook-claude-ai-v${VERSION}"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

BUNDLE_DIR="${WORK_DIR}/product-playbook"
mkdir -p "${BUNDLE_DIR}/lenses" "${BUNDLE_DIR}/recipes" "${BUNDLE_DIR}/assets"

# 1) Adapt the meta-skill and every lens body via the python module.
REPO_ROOT="$REPO_ROOT" BUNDLE_DIR="$BUNDLE_DIR" python3 - <<'PY'
import os
import pathlib
import sys

repo_root = pathlib.Path(os.environ["REPO_ROOT"])
bundle_dir = pathlib.Path(os.environ["BUNDLE_DIR"])
sys.path.insert(0, str(repo_root / "scripts"))

import _adapt_claude_ai_bundle as adapt

skills_dir = repo_root / "skills"

meta_text = (skills_dir / "product-playbook" / "SKILL.md").read_text(
    encoding="utf-8"
)
(bundle_dir / "SKILL.md").write_text(
    adapt.adapt_meta(meta_text), encoding="utf-8"
)

# dev-discipline governs local coding sessions and leans on plugin hooks
# that do not exist on claude.ai, so it stays out of the bundle.
NON_LENS_SKILLS = {"product-playbook", "dev-discipline"}

lens_count = 0
for lens_dir in sorted(skills_dir.iterdir()):
    skill_md = lens_dir / "SKILL.md"
    if lens_dir.name in NON_LENS_SKILLS or not skill_md.is_file():
        continue
    body = adapt.adapt_lens(
        lens_dir.name, skill_md.read_text(encoding="utf-8")
    )
    (bundle_dir / "lenses" / f"{lens_dir.name}.md").write_text(
        body, encoding="utf-8"
    )
    lens_count += 1

print(f"Adapted meta-skill SKILL.md and {lens_count} lens bodies")
PY

# 2) Copy recipe docs and export assets verbatim.
cp "${REPO_ROOT}/references/recipes/"*.md "${BUNDLE_DIR}/recipes/"
cp "${REPO_ROOT}/skills/document-export/assets/"* "${BUNDLE_DIR}/assets/"

# 3) Validate against Claude.ai upload constraints.
FILE_COUNT=$(find "$BUNDLE_DIR" -type f | wc -l | tr -d '[:space:]')
if [ "$FILE_COUNT" -gt 200 ]; then
  echo "ERROR: bundle has $FILE_COUNT files (Claude.ai max is 200)" >&2
  exit 1
fi

DESC_LEN=$(python3 - "${BUNDLE_DIR}/SKILL.md" <<'PY'
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
match = re.search(r"^description:[ \t]*(.*)$", text, re.MULTILINE)
if match is None:
    print("ERROR: adapted SKILL.md has no description line", file=sys.stderr)
    sys.exit(1)
print(len(match.group(1).strip()))
PY
)
if [ "$DESC_LEN" -gt 200 ]; then
  echo "ERROR: SKILL.md description is $DESC_LEN chars (Claude.ai max is 200)" >&2
  exit 1
fi

# 4) Zip and move to the repo root.
(cd "$WORK_DIR" && zip -rq "${BUNDLE_NAME}.zip" product-playbook)
OUTPUT="${REPO_ROOT}/${BUNDLE_NAME}.zip"
mv "${WORK_DIR}/${BUNDLE_NAME}.zip" "$OUTPUT"

SIZE_BYTES=$(stat -c%s "$OUTPUT" 2>/dev/null || stat -f%z "$OUTPUT")
SIZE_MB=$(python3 -c "print(f'{${SIZE_BYTES}/1024/1024:.2f}')")
if [ "$SIZE_BYTES" -gt $((30 * 1024 * 1024)) ]; then
  echo "ERROR: bundle is ${SIZE_MB} MB (Claude.ai max is 30 MB)" >&2
  exit 1
fi

echo "Created: ${OUTPUT}"
echo "  size:   ${SIZE_MB} MB  (cap 30MB)"
echo "  files:  ${FILE_COUNT}  (cap 200)"
echo "  descr:  ${DESC_LEN} chars  (cap 200)"
