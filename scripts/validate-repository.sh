#!/usr/bin/env bash

set -euo pipefail

repository_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repository_root"

failures=0

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  failures=$((failures + 1))
}

required_files=(
  AGENTS.md
  codex/AGENTS.md
  README.md
  runbooks/index.md
  runbooks/verification.md
)

for required_file in "${required_files[@]}"; do
  [[ -f "$required_file" ]] || fail "missing required file: $required_file"
done

if ! cmp -s AGENTS.md codex/AGENTS.md; then
  fail 'codex/AGENTS.md is not an exact backup of AGENTS.md'
fi

while IFS=$'\t' read -r source_file target; do
  case "$target" in
    http://*|https://*|mailto:*|'#'*) continue ;;
  esac

  target=${target%%#*}
  [[ -n "$target" ]] || continue
  resolved_target=$(dirname -- "$source_file")/$target
  [[ -e "$resolved_target" ]] || fail "$source_file links to missing $target"
done < <(
  find . -type f -name '*.md' -not -path './.git/*' -exec \
    perl -ne 'while (/\[[^]]*\]\(([^)]+)\)/g) { print "$ARGV\t$1\n" }' {} +
)

check_image() {
  local path=$1
  local dimensions=$2
  local color_type=$3
  local description

  if [[ ! -f "$path" ]]; then
    fail "missing artwork: $path"
    return
  fi

  description=$(file --brief -- "$path")
  [[ "$description" == *"PNG image data, $dimensions,"* ]] ||
    fail "$path does not have dimensions $dimensions"
  [[ "$description" == *"8-bit/color $color_type,"* ]] ||
    fail "$path is not reported as $color_type"
}

for artwork_set in battle.net wowup-curseforge; do
  artwork_root=steam/artworks/$artwork_set
  check_image "$artwork_root/wide-cover.png" '920 x 430' 'RGB'
  check_image "$artwork_root/portrait-cover.png" '600 x 900' 'RGB'
  check_image "$artwork_root/hero-background.png" '1920 x 620' 'RGB'
  check_image "$artwork_root/title-logo.png" '1200 x 300' 'RGBA'
done

if ! bash -n scripts/validate-repository.sh; then
  fail 'scripts/validate-repository.sh has invalid shell syntax'
fi

if ((failures > 0)); then
  printf '%d validation check(s) failed.\n' "$failures" >&2
  exit 1
fi

printf 'SS repository validation passed.\n'
