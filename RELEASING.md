# Releasing Rundesk Skills

The manifest version labels the catalog Rundesk installs and reports; catalog content, not the
version, decides whether an installed tree changes. A matching Git tag and GitHub Release make that
published state immutable and give maintainers one release ledger.

## Prepare

1. Put every intended catalog change in one pull request against `main`.
2. Update `manifest.json` in that pull request. Use semantic versioning:
   - patch for corrections that preserve the skills and their intended workflows;
   - minor for a new skill or backward-compatible new capability;
   - major only for a deliberately incompatible catalog contract or package change.
3. Run `python3 -m unittest discover -s tests -v` and wait for the `build` workflow.
4. Review the complete manifest, including every skill name and path, before merging.

The manifest bump and content must merge together. Do not publish a tag for an unmerged
commit, and do not reuse or move a published tag.

## Publish

After the pull request is approved and merged, read the version from `manifest.json` and tag
that exact merge commit:

```sh
version=$(python3 -c 'import json; print(json.load(open("manifest.json"))["version"])')
git tag "v$version" <merge-commit>
git push origin "v$version"
```

The `release` workflow refuses a tag that does not exactly match the manifest, reruns the
catalog suite, and creates the GitHub Release with generated notes. Verify the workflow and
release before considering the catalog published:

```sh
gh run list --workflow release.yml --limit 1
gh release view "v$version"
```

Do not tag from a working tree with unmerged catalog changes. Rundesk downloads the repository and
treats its content as authoritative; the manifest version labels that content, and the tag is its
auditable snapshot rather than a second version source.
