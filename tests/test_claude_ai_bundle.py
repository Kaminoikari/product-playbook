"""Unit tests for scripts/_adapt_claude_ai_bundle.py.

Covers the two pure adaptation functions the Claude.ai bundle build uses:
adapt_meta for the bundle-root SKILL.md and adapt_lens for the body-only
lens docs under lenses/. Runs against the real repo sources, pure python
only.
"""

import pathlib
import re
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import _adapt_claude_ai_bundle as adapt

META_TEXT = (REPO_ROOT / "skills/product-playbook/SKILL.md").read_text(
    encoding="utf-8"
)
DOC_EXPORT_TEXT = (REPO_ROOT / "skills/document-export/SKILL.md").read_text(
    encoding="utf-8"
)
JTBD_TEXT = (REPO_ROOT / "skills/jtbd/SKILL.md").read_text(encoding="utf-8")


def _frontmatter_description(text):
    match = re.search(r"^description:[ \t]*(.*)$", text, re.MULTILINE)
    assert match is not None, "no description line in frontmatter"
    return match.group(1).strip()


class TestAdaptMeta(unittest.TestCase):
    def test_description_fits_claude_ai_cap(self):
        desc = _frontmatter_description(adapt.adapt_meta(META_TEXT))
        self.assertLessEqual(len(desc), 200)
        self.assertEqual(desc, adapt.SHORT_DESCRIPTION)

    def test_recipes_path_points_at_bundle_folder(self):
        adapted = adapt.adapt_meta(META_TEXT)
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}/references/recipes/", adapted)
        self.assertIn("`recipes/<name>.md`", adapted)
        # the recipe filenames stay
        for recipe in ("full-product-plan.md", "quick-validation.md",
                       "product-revision.md", "feature-extension.md"):
            self.assertIn(recipe, adapted)

    def test_lens_mapping_note_present(self):
        adapted = adapt.adapt_meta(META_TEXT)
        line = next(
            l for l in adapted.splitlines()
            if l.startswith("Available lenses:")
        )
        self.assertTrue(line.endswith(adapt.LENS_MAPPING_NOTE))
        self.assertIn("lenses/<name>.md", line)
        # the lens list stays on the line
        self.assertIn("strategy-kernel", line)
        self.assertIn("document-export", line)

    def test_rejects_text_without_description(self):
        with self.assertRaises(ValueError):
            adapt.adapt_meta("---\nname: x\n---\n\n# Body\n")


class TestAdaptLens(unittest.TestCase):
    def test_frontmatter_stripped(self):
        body = adapt.adapt_lens("jtbd", JTBD_TEXT)
        self.assertFalse(body.startswith("---"))
        self.assertNotIn("\ndescription:", body.split("\n\n")[0])
        self.assertTrue(body.startswith("# "), body[:40])

    def test_document_export_asset_path_rewritten(self):
        body = adapt.adapt_lens("document-export", DOC_EXPORT_TEXT)
        self.assertNotIn(
            "${CLAUDE_PLUGIN_ROOT}/skills/document-export/assets/", body
        )
        self.assertIn("assets/prd-style.css", body)

    def test_other_lens_body_stays_verbatim(self):
        body = adapt.adapt_lens("jtbd", JTBD_TEXT)
        expected = JTBD_TEXT.split("---\n", 2)[2].lstrip("\n")
        self.assertEqual(body, expected)

    def test_rejects_text_without_frontmatter(self):
        with self.assertRaises(ValueError):
            adapt.adapt_lens("jtbd", "# No Frontmatter\n\nbody\n")


if __name__ == "__main__":
    unittest.main()


class TestBundleSweepExclusions(unittest.TestCase):
    BUILD_SCRIPT = (REPO_ROOT / "scripts" / "build-claude-ai-bundle.sh").read_text(
        encoding="utf-8"
    )

    def test_dev_discipline_is_excluded_from_the_lens_sweep(self):
        # dev-discipline governs local coding sessions and references plugin
        # hooks that do not exist on claude.ai; shipping it in the bundle
        # would document machinery the environment cannot run.
        self.assertIn("dev-discipline", self.BUILD_SCRIPT)
