---
name: publishing-github-releases
description: Use this skill when asked to choose a release version, prepare or publish a GitHub Release, create or verify its tag, generate GitHub release notes, attach artifacts, or recover a partial release. It supplies a guarded SemVer workflow that classifies the complete shipped change, requires exact vMAJOR.MINOR.PATCH tags and titles, publishes from a verified commit through repository automation or a reviewed draft, and proves the stored release. Do not use it for ordinary commits, pull requests, or deployments without a GitHub Release.
---

# Publish GitHub releases

Treat a release as an external, potentially immutable publication. Read the repository's release
contract first; its required branch, version source, validation, artifacts, and automation override
the fallbacks here.

## Establish the release contract

Read every applicable `AGENTS.md`, `CONTRIBUTING.md`, `RELEASING.md`, changelog, version file,
release workflow, and `.github/release.yml`. Determine whether pushing a tag already creates the
GitHub Release. If it does, use that workflow and never also run `gh release create`.

Confirm the repository, active GitHub account, default branch, worktree, remotes, tags, and existing
releases:

```sh
gh auth status --active
gh repo view --json nameWithOwner,url,defaultBranchRef
git remote -v
git branch --show-current
git status --short --branch
git fetch <release-remote> <default-branch> --tags
gh release list --repo <owner/repo> --limit 20
```

Do not silently switch GitHub accounts, repositories, remotes, or release branches. Stop if the
worktree is dirty, the release commit is not merged and pushed as required, validation is incomplete,
or the target repository or active account is uncertain.

## Choose the version from the complete change

Classify every change since the last published release. The highest-impact change determines the
bump:

| Bump | Use when the release contains |
|---|---|
| Patch: `v1.4.2` → `v1.4.3` | Backward-compatible bug or security fixes, documentation corrections, or internal changes with no new public capability. |
| Minor: `v1.4.2` → `v1.5.0` | Backward-compatible functionality, a public deprecation, or a substantial compatible capability. |
| Major: `v1.4.2` → `v2.0.0` | Any incompatible API, CLI, schema, configuration, data, or behavior change that requires consumers to adapt. |

Reset lower components to zero when incrementing minor or major. One breaking change makes the whole
release major; several fixes do not become minor merely by count. Use repository labels and commit
messages as evidence, not as substitutes for inspecting the actual compatibility impact.

For `v0.Y.Z`, the public API is not yet stable under SemVer. Use minor for incompatible changes or
new capability and patch for compatible corrections unless the repository declares a stricter
policy. Use `v1.0.0` when the project deliberately declares its public contract stable.

The public release identity must match this exact regular expression:

```text
^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$
```

Use that exact value for both the Git tag and GitHub Release title: `v1.4.2`, never
`release-v1.4.2`, `product-v1.4.2`, `1.4.2`, `v1.4`, or `v1.4.2-final`. This workflow publishes
stable releases only; do not invent an alpha, beta, release-candidate, date, or build suffix.

Keep repository version files in their required format. A manifest that stores `1.4.2` remains
`1.4.2`; the public tag and release title add the `v`.

Confirm the proposed version is greater than the last release and unused in both Git and GitHub.

## Prepare one exact commit

Update every repository-owned version source, changelog, generated metadata, and compatibility note
required by the release contract. Run its complete prescribed validation and wait for required CI.
Confirm the release range contains only intended work and record the exact commit to publish.

Before any push, tag, draft, asset upload, or publication, present:

- repository and release branch;
- previous release and complete change range;
- proposed exact tag, bump class, and compatibility reason;
- release commit, validation, automation path, and artifacts; and
- any uncertainty, failing check, or missing permission.

A direct request to publish the exact repository and version can supply approval. Otherwise, stop
before the external actions and ask. Approval to prepare a release is not approval to publish it.

## Tag the approved commit

Create an annotated exact-version tag on the recorded commit and push only that tag:

```sh
version=1.4.2
tag="v$version"
printf '%s\n' "$tag" | grep -Eq '^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$' || exit 1
release_commit=$(git rev-parse <approved-release-commit>)
git tag -a "$tag" "$release_commit" -m "$tag"
git push <release-remote> "refs/tags/$tag"
```

If a repository workflow owns release creation, confirm it requests GitHub-generated notes, monitor
it, and then continue at verification. Surface a workflow that violates the repository's release
contract instead of bypassing it.

## Generate and review the GitHub Release

Without repository automation, create a draft from the already-pushed tag. `--verify-tag` prevents
GitHub from silently tagging the default branch, and `--fail-on-no-commits` prevents a duplicate
release when a previous release exists. Add `--notes-start-tag <previous-tag>` when the repository
has multiple release lines or GitHub would choose the wrong comparison:

```sh
gh release create "$tag" --repo <owner/repo> \
  --draft \
  --verify-tag \
  --generate-notes \
  --fail-on-no-commits \
  --title "$tag"
```

Inspect the stored draft. GitHub-generated notes should cover the merged pull requests,
contributors, and full comparison from the correct previous tag. Honor `.github/release.yml` label
categories and exclusions. Use the generated body as the base; correct missing breaking changes,
migrations, security instructions, or misleading summaries in a reviewed notes file when needed:

```sh
gh release view "$tag" --repo <owner/repo> \
  --json url,name,tagName,targetCommitish,body,isDraft,isPrerelease,assets
gh release edit "$tag" --repo <owner/repo> --notes-file <reviewed-release-notes.md>
```

Attach repository-required artifacts and checksums to the draft before publishing. Never use
`--clobber` to replace an asset without explicit approval and proof that the release is still a
mutable draft.

Publish only after the draft, tag target, notes, and assets match the approved release:

```sh
gh release edit "$tag" --repo <owner/repo> \
  --draft=false \
  --verify-tag \
  --title "$tag"
```

Let GitHub determine `Latest` from semantic version order unless the repository explicitly defines
another policy. Do not mark an older maintenance release latest by accident.

## Prove publication

Fetch the remote tag and confirm it resolves to the recorded release commit. Read the published
release back from GitHub and verify its exact title, tag, non-draft state, stable state, notes, URL,
and assets. When immutable releases are enabled, also run `gh release verify "$tag"`; verify local
assets with `gh release verify-asset "$tag" <file>`.

If any command fails, inspect the remote tag, workflow runs, and existing draft or release before
retrying. Never delete, move, or recreate a published tag to hide a mistake. Correct a published
release with a new patch version. Report success only with the release URL, exact tag, commit,
version rationale, and verification evidence.
