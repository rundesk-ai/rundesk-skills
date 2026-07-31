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
        cls.manifest = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))

    def test_manifest_names_a_versioned_catalog(self):
        self.assertEqual(1, self.manifest["manifest"])
        self.assertRegex(self.manifest["name"], ALLOWED)
        self.assertRegex(self.manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertTrue(self.manifest["description"].strip())

    def test_manifest_declares_every_skill_directory_once(self):
        declared = self.manifest["skills"]
        names = [entry["name"] for entry in declared]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(
            sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir()),
            sorted(names),
        )

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


if __name__ == "__main__":
    unittest.main()
