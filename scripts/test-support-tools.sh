#!/usr/bin/env bash

set -euo pipefail

repository_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repository_root"

profiles=(system storage steam flatpak network bluetooth audio input all)
for profile in "${profiles[@]}"; do
  output=$(bash scripts/collect-diagnostics.sh --dry-run "$profile")
  [[ "$output" == *'SS read-only diagnostic collection'* ]]
  if printf '%s\n' "$output" | grep -Eq '^\$ (sudo|rm|mv|cp|install|chmod|chown|mount|umount|reboot|shutdown|systemctl (enable|disable|start|stop|restart)|flatpak (update|repair|uninstall))([[:space:]]|$)'; then
    printf 'collector dry-run contains a mutating command in profile %s\n' "$profile" >&2
    exit 1
  fi
done

summary=$(bash scripts/collect-diagnostics.sh --dry-run all | python3 -B scripts/summarize-diagnostics.py)
[[ "$summary" == *'Profiles: all, system, storage, steam, flatpak, network, bluetooth, audio, input'* ]]
[[ "$summary" == *'Command sections: 26'* ]]
[[ "$summary" == *'Unavailable or non-zero commands: 0'* ]]

if bash scripts/collect-diagnostics.sh unknown >/dev/null 2>&1; then
  printf 'collector accepted an unknown profile\n' >&2
  exit 1
fi

sanitized=$(python3 -B scripts/sanitize-diagnostics.py tests/fixtures/diagnostics-sensitive.txt)
for marker in '<ip-address>' '<ip-address-v6>' '<mac-address>' '<uuid>' '/home/<user>' '<redacted>'; do
  [[ "$sanitized" == *"$marker"* ]] || {
    printf 'sanitizer did not produce marker: %s\n' "$marker" >&2
    exit 1
  }
done
for secret in '192.0.2.10' 'fe80::1' '02:00:5e:10:00:00' 'Example Network With Spaces'; do
  [[ "$sanitized" != *"$secret"* ]] || {
    printf 'sanitizer retained fixture value: %s\n' "$secret" >&2
    exit 1
  }
done

token_input=$(printf '%s%s\n' 'ghp_' '12345678901234567890')
sanitized_token=$(printf '%s' "$token_input" | python3 -B scripts/sanitize-diagnostics.py)
[[ "$sanitized_token" == '<token>' ]] || {
  printf 'sanitizer did not redact a constructed token fixture\n' >&2
  exit 1
}

printf 'Support-tool tests passed.\n'
