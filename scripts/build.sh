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
  printf '\nVersion: %s (https://github.com/%s/releases/tag/%s). Newest version: https://github.com/%s/releases/latest\n' "$tag" "$repo" "$tag" "$repo"
  tail -n +2 "$src"
} > "dist/$asset"

# Same content as .txt for people who do not know .md files. The fixed name
# serves the "latest" link; the versioned name keeps the version in downloads.
cp "dist/$asset" dist/no-tech-scribe.txt
cp "dist/$asset" "dist/no-tech-scribe-$tag.txt"

(cd dist && shasum -a 256 "no-tech-scribe-$tag.txt" no-tech-scribe.txt "$asset" > SHA256SUMS)

echo "built dist/ for $tag"
cat dist/SHA256SUMS
