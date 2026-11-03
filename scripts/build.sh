#!/bin/sh
# Build the release assets for one version into dist/.
# Usage: scripts/build.sh v1.2.3
set -eu

tag="${1:?usage: scripts/build.sh <tag, e.g. v1.2.3>}"
repo="${GITHUB_REPOSITORY:-odjhey/no-tech-scribe}"
src="src/no-tech-scribe.md"
asset="no-tech-scribe.md"

if ! printf '%s\n' "$tag" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$'; then
  echo "error: '$tag' is not a version tag like v1.2.3 or v1.2.3-rc.1" >&2
  exit 1
fi

cd "$(dirname "$0")/.."

if ! head -n 1 "$src" | grep -q '^# '; then
  echo "error: $src must start with a '# ' title line" >&2
  exit 1
fi

rm -rf dist
mkdir dist

# Keep the title, then add a plain version line so transcripts show what was loaded.
{
  head -n 1 "$src"
  printf '\nVersion: %s (https://github.com/%s/releases/tag/%s)\n' "$tag" "$repo" "$tag"
  tail -n +2 "$src"
} > "dist/$asset"

(cd dist && shasum -a 256 "$asset" > SHA256SUMS)

echo "built dist/$asset for $tag"
cat dist/SHA256SUMS
