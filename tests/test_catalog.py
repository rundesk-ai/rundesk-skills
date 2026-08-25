"""The published catalog is internally complete and contains guidance only."""

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ALLOWED = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CATALOG_GUIDE_URL = "https://github.com/rundesk-ai/rundesk-cli/blob/main/docs/catalogs.md"
FORBIDDEN_PACKAGE_FILES = {"README.md", "CHANGELOG.md", "rundesk.json"}
ALLOWED_PACKAGE_ROOTS = {"SKILL.md", "LICENSE.txt", "references", "assets"}
LEGACY_PACKAGES_WITHOUT_SOURCES = {"pdf-creation"}
MOVED_DEVELOPMENT_SKILLS = {
    "database-design",
    "debugging-code",
    "executing-development-tasks",
    "frontend-design",
    "inertia-patterns",
    "laravel-patterns",
    "managing-github",
    "mysql-patterns",
    "postgres-patterns",
    "python-patterns",
    "reviewing-code",
    "sqlite-patterns",
    "testing-code",
    "vue-patterns",
    "writing-technical-docs",
}
AGENT_HEADINGS = (
    "# AGENTS",
    "## Purpose",
    "## Before you work",
    "## Repository layout",
    "## Package and artifact contract",
    "## Safety and approval gates",
    "## Delegation",
    "## Architecture and conventions",
    "## Documentation duties",
    "## Build, test, and run",
    "## Pull requests and releases",
    "## Definition of done",
)
PR_HEADINGS = (
    "## Problem",
    "## Proposed solution",
    "## Evidence",
    "## Scope and compatibility",
    "## Risks and safeguards",
    "## Acceptance criteria",
    "## Validation",
    "## Repository gates",
    "## Release",
    "## Manual user path",
    "## Agent",
)
PR_CHECKLIST_ANCHORS = (
    "- Skills changed:",
    "- [ ] `python3 -m unittest discover -s tests -v`",
    "- [ ] Required GitHub checks pass for the exact head commit.",
    "- [ ] The diff contains no credential, customer identifier, private-project language, owner-specific path, generated filler, or unrelated artifact.",
    "- [ ] `README.md`, `manifest.json`, `tests/test_catalog.py`, and `skills/` agree.",
    "🤖 by <Agent>",
)
README_HEADINGS = (
    "## Skills",
    "## Install",
    "## Requirements",
    "## Repository layout",
    "## Development",
    "## Creating a skill catalog",
    "## Contributing",
    "## Releases",
    "## License",
)
ISSUE_HEADINGS = {
    "bug-report.md": (
        "## Problem",
        "## Reproduction",
        "## Expected behavior",
        "## Evidence",
        "## Acceptance criteria",
        "## Environment",
        "## Scope and privacy",
        "## Agent",
    ),
    "change-proposal.md": (
        "## Problem",
        "## Proposed solution",
        "## Evidence",
        "## Scope and compatibility",
        "## Acceptance criteria",
        "## Verification",
        "## Alternatives considered",
        "## Agent",
    ),
}
ISSUE_DIGESTS = {
    "bug-report.md": "6e8eadbdaf3198c29ed33edf6b3abaf7374cfca5adb05d46c85daedeb1281276",
    "change-proposal.md": "82c13fe89d21778e23de6c9a7ae7e918960cf78d4b2cccd69041e9160e97fdbd",
}


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
        self.assertEqual(
            README_HEADINGS,
            tuple(re.findall(r"^## .+$", readme, re.MULTILINE)),
        )
        for required in (
            CATALOG_GUIDE_URL,
            ".github/ISSUE_TEMPLATE/bug-report.md",
            ".github/ISSUE_TEMPLATE/change-proposal.md",
            ".github/pull_request_template.md",
            "rundesk skills install https://github.com/rundesk-ai/rundesk-skills --confirm",
            "rundesk skills grant ava rundesk-skills/writing-plans",
            "rundesk-team-development/testing-code",
            "rundesk-team-development/using-python",
            "rundesk/managing-github",
            "rundesk skills update rundesk-skills --confirm",
        ):
            with self.subTest(readme_contract=required):
                self.assertIn(required, readme)
        self.assertNotIn("<agent>", readme)

    def test_general_catalog_contains_required_specialties(self):
        names = {entry["name"] for entry in self.manifest["skills"]}
        self.assertIn("pdf-creation", names)
        self.assertIn("performance-engineering", names)
        self.assertIn("creating-design-assets", names)
        self.assertIn("conversion-landing-pages", names)
        self.assertIn("ecommerce-storefronts", names)
        self.assertIn("maintaining-task-briefs", names)
        self.assertIn("naming-grammar-conventions", names)
        self.assertIn("lead-compliance-gates", names)
        self.assertIn("laravel-stripe-payments", names)
        self.assertIn("researching-topics", names)
        self.assertIn("seo", names)
        self.assertIn("working-as-an-assistant", names)
        self.assertIn("writing-prds", names)
        self.assertEqual(set(), names & MOVED_DEVELOPMENT_SKILLS)

    def test_every_entry_is_a_complete_named_skill(self):
        missing_sources = set()
        for entry in self.manifest["skills"]:
            with self.subTest(skill=entry["name"]):
                self.assertRegex(entry["name"], ALLOWED)
                package = ROOT / entry["path"]
                self.assertEqual(entry["name"], package.name)
                self.assertEqual(Path("skills") / entry["name"], Path(entry["path"]))
                self.assertLessEqual(
                    {path.name for path in package.iterdir()},
                    ALLOWED_PACKAGE_ROOTS,
                )
                page = (package / "SKILL.md").read_text(encoding="utf-8")
                sections = page.split("---", 2)
                self.assertEqual(3, len(sections), "SKILL.md needs YAML frontmatter")
                frontmatter = [
                    line for line in sections[1].strip().splitlines() if line.strip()
                ]
                keys = [line.partition(":")[0] for line in frontmatter]
                self.assertEqual(["name", "description"], keys)
                self.assertEqual(f"name: {entry['name']}", frontmatter[0])
                description = frontmatter[1].partition(":")[2].strip()
                self.assertTrue(description)
                self.assertLessEqual(len(description), 1024)
                self.assertLessEqual(len(page.splitlines()), 500)

                sources = package / "references" / "sources.md"
                if not sources.is_file():
                    missing_sources.add(entry["name"])
                for forbidden in FORBIDDEN_PACKAGE_FILES:
                    self.assertFalse((package / forbidden).exists())
                self.assertFalse((package / "scripts").exists())
                self.assertFalse((package / "agents").exists())
                for artifact in package.rglob("*"):
                    if artifact.is_file():
                        self.assertEqual(
                            0,
                            artifact.stat().st_mode & 0o111,
                            f"{artifact.relative_to(ROOT)} must not be executable",
                        )
        self.assertEqual(LEGACY_PACKAGES_WITHOUT_SOURCES, missing_sources)

    def test_catalog_contains_no_integration_commands(self):
        self.assertEqual([], list((ROOT / "skills").glob("*/scripts/**")))

    def test_repository_guides_and_templates_follow_the_shared_contract(self):
        agents = (ROOT / "AGENTS.md").read_bytes()
        self.assertEqual(agents, (ROOT / "CLAUDE.md").read_bytes())
        self.assertIn(
            CATALOG_GUIDE_URL.encode(),
            agents,
        )
        self.assertEqual(
            AGENT_HEADINGS,
            tuple(re.findall(r"^#{1,2} .+$", agents.decode("utf-8"), re.MULTILINE)),
        )

        pull_request = ROOT / ".github" / "pull_request_template.md"
        self.assertTrue(pull_request.is_file())
        pull_request_text = pull_request.read_text(encoding="utf-8")
        self.assertEqual(
            PR_HEADINGS,
            tuple(re.findall(r"^## .+$", pull_request_text, re.MULTILINE)),
        )
        for anchor in PR_CHECKLIST_ANCHORS:
            with self.subTest(pull_request_anchor=anchor):
                self.assertIn(anchor, pull_request_text)

        issue_root = ROOT / ".github" / "ISSUE_TEMPLATE"
        self.assertEqual(
            {"bug-report.md", "change-proposal.md", "config.yml"},
            {path.name for path in issue_root.iterdir() if path.is_file()},
        )
        self.assertEqual(
            b"blank_issues_enabled: false\n",
            (issue_root / "config.yml").read_bytes(),
        )
        for filename, expected in ISSUE_HEADINGS.items():
            with self.subTest(issue_template=filename):
                issue = issue_root / filename
                self.assertTrue(issue.is_file())
                issue_bytes = issue.read_bytes()
                self.assertEqual(
                    ISSUE_DIGESTS[filename],
                    hashlib.sha256(issue_bytes).hexdigest(),
                )
                self.assertIn("🤖 by <Agent>", issue_bytes.decode("utf-8"))
                self.assertEqual(
                    expected,
                    tuple(re.findall(r"^## .+$", issue_bytes.decode("utf-8"), re.MULTILINE)),
                )

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
