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
  .github/workflows/validate.yml
  AGENTS.md
  README.md
  codex/AGENTS.md
  codex/README.md
  runbooks/README.md
  runbooks/backup-and-restore.md
  runbooks/common-issues.md
  runbooks/compatibility-status.md
  runbooks/connectivity.md
  runbooks/coverage-matrix.md
  runbooks/diagnostics.md
  runbooks/flatpak.md
  runbooks/full-system-restore.md
  runbooks/github-access.md
  runbooks/hardware-peripherals.md
  runbooks/index.md
  runbooks/non-steam-games.md
  runbooks/power-performance.md
  runbooks/readiness-scorecard.md
  runbooks/remote-access.md
  runbooks/save-data.md
  runbooks/scenario-catalog.md
  runbooks/steam-proton.md
  runbooks/storage-microsd.md
  runbooks/sudo-access.md
  runbooks/support-session-record-template.md
  runbooks/support-session.md
  runbooks/triage.md
  runbooks/updates-boot.md
  runbooks/verification.md
  scripts/check-compatibility-status.py
  scripts/check-runbook-structure.py
  scripts/check-scenario-coverage.py
  scripts/collect-diagnostics.sh
  scripts/list-non-steam-shortcuts.py
  scripts/sanitize-diagnostics.py
  scripts/summarize-diagnostics.py
  scripts/test-support-tools.sh
  scripts/validate-artwork.py
  scripts/validate-markdown-links.py
  scripts/validate-repository.sh
  steam/README.md
  steam/add-non-steam-game-and-artwork-guide.md
  steam/artworks/README.md
  tests/fixtures/diagnostics-sensitive.txt
)

for required_file in "${required_files[@]}"; do
  [[ -f "$required_file" ]] || fail "missing required file: $required_file"
done

if ! cmp -s AGENTS.md codex/AGENTS.md; then
  fail 'codex/AGENTS.md is not an exact backup of AGENTS.md'
fi

retired_root='/home/deck/Documents/'
retired_root+='codex-steamdeck-support'
if grep -RIl --exclude-dir=.git --exclude=AGENTS.md "$retired_root" . | grep -q .; then
  fail 'repository contains the retired project path'
fi

if grep -RIEIl --exclude-dir=.git \
  'BEGIN ([A-Z0-9]+ )?PRIVATE KEY|github_pat_[A-Za-z0-9_]+|gh[opurs]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}' \
  . | grep -q .; then
  fail 'repository contains text matching a common secret pattern'
fi

python3 -B scripts/check-runbook-structure.py ||
  fail 'runbook structure validation failed'

python3 -B scripts/check-compatibility-status.py ||
  fail 'compatibility status validation failed'

python3 -B scripts/check-scenario-coverage.py ||
  fail 'scenario coverage validation failed'

python3 -B scripts/validate-markdown-links.py ||
  fail 'Markdown link validation failed'

python3 -B scripts/validate-artwork.py ||
  fail 'artwork content validation failed'

python3 -B scripts/list-non-steam-shortcuts.py --self-test ||
  fail 'non-Steam shortcut inspector self-test failed'

bash scripts/test-support-tools.sh ||
  fail 'support-tool tests failed'

git diff --check ||
  fail 'working-tree whitespace validation failed'

git diff --cached --check ||
  fail 'staged whitespace validation failed'

for shell_script in scripts/*.sh; do
  bash -n "$shell_script" || fail "$shell_script has invalid shell syntax"
done

for python_script in scripts/*.py; do
  python3 -B -c 'import ast, pathlib, sys; ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"), filename=sys.argv[1])' "$python_script" ||
    fail "$python_script has invalid Python syntax"
done

if ((failures > 0)); then
  printf '%d validation check(s) failed.\n' "$failures" >&2
  exit 1
fi

printf 'SS repository validation passed.\n'
