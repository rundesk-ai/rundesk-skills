# GitHub releases

## Discover the release contract

Read applicable `AGENTS.md`, `CONTRIBUTING.md`, `RELEASING.md`, changelog, version files, release
workflows, and `.github/release.yml`. Determine the required branch, version source, validation,
artifacts, and whether a pushed tag creates the GitHub Release. When automation owns creation,
use it; never also run `gh release create`.

Fetch the release branch and tags, then inspect existing releases:

```sh
git fetch <release-remote> <default-branch> --tags
gh release list --repo <owner/repo> --limit 20
```

Stop if the worktree is dirty, the intended commit is not merged and pushed as required,
validation is incomplete, or the release branch, commit, account, repository, or remote is
uncertain.

## Classify the release branch

Determine branch purpose from repository instructions and deployment workflows, never from its name
alone:

- A live website deployment branch represents the code deployed to a production environment; its
  canonical integration branch is `main` unless repository instructions explicitly name another.
- A product release comes from `main` or an intentional isolated version branch used to build and
  support that product version.

When releasing from a live website deployment branch, treat reconciliation into `main` as part of
release completion. After production verification, fetch both branches, compare the deployed commit
with current `main`, and merge the deployment branch back through a pull request with the
repository's required reviews and checks. Do not merge `main` into the deployment branch and call it
reconciled. Verify the exact deployed commit is reachable from updated `main`; if repository policy
requires squash or rebase, instead prove no deployment-only content remains and record that
exception. Substitute the repository's explicitly named canonical branch for `main` when needed.

Do not report the release as complete while the deployment branch still contains unreconciled work.
If the current authority does not permit the pull request or merge, prepare only what is authorized
and report the back-merge as the remaining release blocker.

Do not apply that automatic back-merge rule to an isolated product-version branch. Follow the
repository's merge-forward or maintenance policy for that release line, and deliberately port only
the changes that belong on `main`.

## Choose an exact version

Inspect every change since the last published release. The highest-impact change sets the bump:

| Bump | Use when the release contains |
|---|---|
| Patch: `v1.4.2` → `v1.4.3` | Compatible fixes, documentation corrections, or internal changes with no new public capability. |
| Minor: `v1.4.2` → `v1.5.0` | Backward-compatible functionality or public deprecation. |
| Major: `v1.4.2` → `v2.0.0` | Any incompatible API, CLI, schema, configuration, data, or behavior change. |

Reset lower components after a minor or major increment. One breaking change makes the release
major; fix count does not determine the bump. For `v0.Y.Z`, use minor for incompatible changes or
new capability and patch for compatible corrections unless the repository is stricter. Use
`v1.0.0` only when the project deliberately declares its public contract stable.

The public tag and GitHub Release title must both match:

```text
^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$
```

Use `v1.4.2`, never a product prefix, missing `v`, shortened version, prerelease, date, or suffix.
Keep repository version files in their required format, such as `1.4.2` without `v`. Confirm the
version is greater than the last release and unused in Git and GitHub.

## Prepare the release commit

Update every required version source, changelog, generated file, and compatibility note. Run the
repository's complete release validation, wait for required CI, inspect the full release range,
and record the exact commit.

Before any push, tag, draft, upload, or publication, present the repository and release branch;
previous release and range; exact tag and compatibility rationale; commit, validation,
automation, and artifacts; and every uncertainty or failed check. A request to publish that exact
repository and version authorizes publication. Otherwise stop before external changes.

## Tag and generate notes

Create an annotated tag on the recorded commit and push only that tag:

```sh
version=1.4.2
tag="v$version"
printf '%s\n' "$tag" | grep -Eq '^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$' || exit 1
release_commit=$(git rev-parse <approved-release-commit>)
git tag -a "$tag" "$release_commit" -m "$tag"
git push <release-remote> "refs/tags/$tag"
```

If repository automation owns the release, confirm it uses GitHub-generated notes, monitor it,
and continue at verification. Otherwise create a draft from the pushed tag:

```sh
gh release create "$tag" --repo <owner/repo> \
  --draft \
  --verify-tag \
  --generate-notes \
  --fail-on-no-commits \
  --title "$tag"
```

Add `--notes-start-tag <previous-tag>` when GitHub would compare the wrong release line. Inspect
the stored draft. Generated notes should cover the correct pull requests, contributors, and
comparison range, honoring `.github/release.yml`. Correct missing breaking changes, migrations,
security instructions, or misleading summaries in a reviewed notes file:

```sh
gh release view "$tag" --repo <owner/repo> \
  --json url,name,tagName,targetCommitish,body,isDraft,isPrerelease,assets
gh release edit "$tag" --repo <owner/repo> --notes-file <reviewed-release-notes.md>
```

Attach required artifacts and checksums before publishing. Never replace an asset with
`--clobber` without explicit approval and proof the release is still a mutable draft.

## Publish, verify, and recover

Publish only after the tag target, draft, notes, and assets match the approved release:

```sh
gh release edit "$tag" --repo <owner/repo> \
  --draft=false \
  --verify-tag \
  --title "$tag"
```

Let GitHub determine `Latest` from semantic order unless repository policy says otherwise. Fetch
the remote tag and prove it resolves to the recorded commit. Read the published release back and
verify its exact tag, title, stable and non-draft state, notes, URL, and assets. With immutable
releases, run `gh release verify "$tag"`; verify local artifacts with
`gh release verify-asset "$tag" <file>`.

After failure, inspect the remote tag, workflow runs, draft, and published release before retrying.
Never delete, move, or recreate a published tag to hide a mistake; correct a published release
with a new patch version. Report success only with the URL, tag, commit, bump rationale, and
verification evidence.
