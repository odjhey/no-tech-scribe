# Releasing

`src/no-tech-scribe.md` is the payload: the instructions a harness reads. Each release publishes it as a versioned asset with a link that never changes.

## Cut a release

```sh
git tag v1.2.0
git push origin v1.2.0
```

The [Release workflow](.github/workflows/release.yml) first runs the rule ID check against earlier tags (see [README](README.md#edit-the-rules)). Then it builds the same content three times: `no-tech-scribe-<tag>.txt` (version in the file name, so downloads and local copies show it), `no-tech-scribe.txt` (fixed name for the latest link) and `no-tech-scribe.md`, plus `SHA256SUMS`. Then it publishes the GitHub release with the links in its notes. It fails if the release already exists. To change published content, tag a new version.

A tag with a suffix, such as `v1.2.0-rc.1`, becomes a prerelease. Use it to run evals before colleagues see the change. A prerelease never becomes the "latest" link.

## Links

| Use | Link |
| --- | --- |
| Pin one version (evals, reproducible sessions) | `https://github.com/odjhey/no-tech-scribe/releases/download/<tag>/no-tech-scribe-<tag>.txt` |
| Always the newest stable version | `https://github.com/odjhey/no-tech-scribe/releases/latest/download/no-tech-scribe.txt` |

The build adds a version line under the title, so a transcript shows which version the harness loaded:

```
# no-tech-scribe

Version: v1.2.0 (https://github.com/odjhey/no-tech-scribe/releases/tag/v1.2.0). Newest version: https://github.com/odjhey/no-tech-scribe/releases/latest
```

## Check locally

```sh
scripts/check-ids.py      # compares rule IDs with every released tag
scripts/build.sh v1.2.0   # writes the three copies and SHA256SUMS to dist/
```

## One-time repository settings

- The repository must be public. Otherwise, harnesses cannot fetch the assets without credentials.
- Turn on **Settings → General → Releases → Enable release immutability**. GitHub then locks each published release's assets and tag.
