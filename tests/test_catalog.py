"""The published catalog is internally complete and contains guidance only."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ALLOWED = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CatalogContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    def test_manifest_names_a_versioned_catalog(self):
        self.assertEqual(1, self.manifest["schema"])
        self.assertRegex(self.manifest["name"], ALLOWED)
        self.assertRegex(self.manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertTrue(self.manifest["description"].strip())
        self.assertGreaterEqual(len(self.manifest["skills"]), 1)
        self.assertFalse((ROOT / "catalog.json").exists())

    def test_manifest_declares_every_skill_directory_once(self):
        declared = self.manifest["skills"]
        names = [entry["name"] for entry in declared]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(
            sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir()),
            sorted(names),
        )

    def test_readme_lists_exactly_the_declared_skills(self):
        """A catalog that ships a skill its README never mentions is a catalog nobody trusts."""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"(?m)^- `([a-z0-9-]+)`", readme))
        declared = {entry["name"] for entry in self.manifest["skills"]}
        self.assertEqual(declared, listed, "README.md and manifest.json disagree")

    def test_general_catalog_contains_required_specialties(self):
        names = {entry["name"] for entry in self.manifest["skills"]}
        self.assertIn("pdf-creation", names)
        self.assertIn("researching-topics", names)
        self.assertIn("seo", names)

    def test_every_entry_is_a_complete_named_skill(self):
        for entry in self.manifest["skills"]:
            with self.subTest(skill=entry["name"]):
                package = ROOT / entry["path"]
                self.assertEqual(entry["name"], package.name)
                page = (package / "SKILL.md").read_text(encoding="utf-8")
                self.assertRegex(page, rf"(?m)^name: {re.escape(entry['name'])}$")
                self.assertRegex(page, r"(?m)^description: .+\S$")

    def test_catalog_contains_no_integration_commands(self):
        self.assertEqual([], list((ROOT / "skills").glob("*/scripts/**")))

    def test_release_process_ties_tags_to_the_manifest_version(self):
        guide = (ROOT / "RELEASING.md").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("manifest.json", guide)
        self.assertIn('tags:', workflow)
        self.assertIn('does not match manifest', workflow)
        self.assertIn('gh release create', workflow)


if __name__ == "__main__":
    unittest.main()
