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
LEGACY_PACKAGES_WITHOUT_SOURCES = {
    "mysql-patterns",
    "pdf-creation",
    "postgres-patterns",
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
    ),
    "change-proposal.md": (
        "## Problem",
        "## Proposed solution",
        "## Evidence",
        "## Scope and compatibility",
        "## Acceptance criteria",
        "## Verification",
        "## Alternatives considered",
    ),
}
ISSUE_DIGESTS = {
    "bug-report.md": "9b8bb222a68b4c2a592512ee368c17bc8edc8e0750c5f76ba3e4dd65837e5187",
    "change-proposal.md": "71f68d702f29e1cedd6b5a839b8a10df899240f68bd215d734ee77f5286cd379",
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
            "rundesk skills grant ava rundesk-skills/testing-code",
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
        self.assertNotIn("executing-development-tasks", names)
        self.assertIn("maintaining-task-briefs", names)
        self.assertIn("managing-development-work", names)
        self.assertIn("naming-grammar-conventions", names)
        self.assertIn("lead-compliance-gates", names)
        self.assertIn("laravel-stripe-payments", names)
        self.assertIn("researching-topics", names)
        self.assertIn("seo", names)
        self.assertIn("working-as-an-assistant", names)
        self.assertIn("writing-prds", names)
        self.assertIn("writing-technical-docs", names)

    def test_development_management_keeps_proportionate_delivery_boundaries(self):
        page = (
            ROOT / "skills" / "managing-development-work" / "SKILL.md"
        ).read_text(encoding="utf-8")
        description = page.split("---", 2)[1]
        normalized = " ".join(page.split())

        for trigger in (
            "handling a software change from request to an approval-ready outcome",
            "scoping, planning, execution, delegation decisions, scope control, and validation",
        ):
            with self.subTest(routing_trigger=trigger):
                self.assertIn(trigger, description)
        for role_filter in (
            "primary",
            "domain agent",
            "inbound specialist",
            "Do not use",
        ):
            with self.subTest(role_filter=role_filter):
                self.assertNotIn(role_filter, description)

        for required in (
            "Choose the shortest safe path",
            "Use direct work for a localized documentation",
            "Use one implementer for an ordinary code change",
            "Use a read-only discovery specialist",
            "three production files or 150 production lines",
            "Passing tests never authorizes more scope",
            "When implementation reveals a new dependency",
            "do not let sunk effort decide scope",
            "Do not require an issue, project entry, branch, commit, or pull-request draft",
            "Obtain explicit owner approval for that exact pull-request outcome and scope",
            "it never performs GitHub delivery for the primary",
        ):
            with self.subTest(development_boundary=required):
                self.assertIn(required, normalized)
        self.assertIn("Do not grant this orchestration workflow to inbound-only", normalized)

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

    def test_managing_github_keeps_complete_fallback_templates(self):
        package = ROOT / "skills" / "managing-github"
        issues = (package / "references" / "issues.md").read_text(encoding="utf-8")
        pull_requests = (package / "references" / "pull-requests.md").read_text(
            encoding="utf-8"
        )
        issue_templates = (package / "references" / "issue-templates.md").read_text(
            encoding="utf-8"
        )
        pull_request_template = (
            package / "references" / "pull-request-template.md"
        ).read_text(encoding="utf-8")

        self.assertIn("[the fallback issue templates](issue-templates.md)", issues)
        self.assertIn(
            "[fallback pull-request template](pull-request-template.md)",
            pull_requests,
        )
        self.assertIn("scan-friendly review map", pull_requests)
        self.assertIn("normally no more than five steps", pull_requests)
        self.assertIn("Every PR body must identify the filing agent", pull_requests)
        self.assertIn("`Generated with` footer", pull_requests)
        self.assertIn("Reject low-information prose", pull_requests)
        for weak_heading in ("## Need", "## What we need", "## Summary"):
            with self.subTest(weak_heading=weak_heading):
                self.assertNotIn(weak_heading, issue_templates)
                self.assertNotIn(weak_heading, pull_request_template)
        issue_blocks = re.findall(r"```md\n(.*?)\n```", issue_templates, re.DOTALL)
        self.assertEqual(2, len(issue_blocks))
        for block, headings in zip(issue_blocks, ISSUE_HEADINGS.values()):
            with self.subTest(issue_fallback=headings[0]):
                self.assertEqual(
                    headings,
                    tuple(re.findall(r"^## .+$", block, re.MULTILINE)),
                )
        pull_request_block = re.search(
            r"````md\n(.*?)\n````", pull_request_template, re.DOTALL
        )
        self.assertIsNotNone(pull_request_block)
        self.assertEqual(
            (
                "## Problem",
                "## Proposed solution",
                "## Evidence",
                "## Acceptance criteria",
                "## Validation",
                "## Agent",
            ),
            tuple(
                re.findall(
                    r"^## .+$", pull_request_block.group(1), re.MULTILINE
                )
            ),
        )
        self.assertIn("🤖 by <Agent>", pull_request_template)

    def test_managing_github_keeps_external_writes_with_the_responsible_agent(self):
        package = ROOT / "skills" / "managing-github"
        skill = " ".join((package / "SKILL.md").read_text(encoding="utf-8").split())
        sources = " ".join(
            (package / "references" / "sources.md").read_text(encoding="utf-8").split()
        )

        for phrase in (
            "The primary or domain agent responsible for the outcome owns every GitHub write",
            "Never delegate issue or pull-request creation, editing, submission, or follow-up",
            "even when that specialist prepared the implementation or investigation",
            "The specialist returns local artifacts and evidence",
            "re-establishes the account and repository itself",
            "stop at the handback instead of using a GitHub mutation command",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)
        self.assertIn(
            "issue and pull-request writes stay with the primary or domain agent", sources
        )

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
