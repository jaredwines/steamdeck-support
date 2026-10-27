#!/usr/bin/env bash

set -u

usage() {
  cat <<'EOF'
Usage: scripts/collect-diagnostics.sh [--dry-run] PROFILE

Read-only profiles:
  system      SteamOS, kernel, failed services
  storage     Filesystem, block-device, and mount summary
  steam       Steam-relevant system and storage state
  flatpak     Application and transaction summary
  network     Network manager, interface, and radio state
  bluetooth   Bluetooth radio and service state
  audio       PipeWire/WirePlumber service and route summary
  input       Input device summary
  all         Run every profile

Options:
  --list      List profiles
  --dry-run   Print commands without running them
  --help      Show this help

The collector makes no changes and uploads nothing. Output can contain local
addresses, device names, application history, and identifiers. Review it
locally and sanitize it before sharing:

  bash scripts/collect-diagnostics.sh PROFILE |
    python3 -B scripts/sanitize-diagnostics.py

For a compact summary that includes no collected values:

  bash scripts/collect-diagnostics.sh PROFILE |
    python3 -B scripts/summarize-diagnostics.py
EOF
}

dry_run=false
case "${1:-}" in
  --help|-h) usage; exit 0 ;;
  --list) usage | sed -n '/Read-only profiles:/,/Options:/p' | sed '$d'; exit 0 ;;
  --dry-run) dry_run=true; shift ;;
esac

profile=${1:-}
if [[ -z "$profile" || $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

run() {
  local label=$1
  shift
  printf '\n## %s\n' "$label"
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  if [[ "$dry_run" == true ]]; then
    return
  fi
  if ! "$@" 2>&1; then
    printf '[command unavailable or returned a non-zero status]\n'
  fi
}

system_profile() {
  run 'SteamOS release' cat /etc/os-release
  run 'Kernel' uname -r
  run 'System failures' systemctl --failed --no-pager
  run 'User-service failures' systemctl --user --failed --no-pager
}

storage_profile() {
  run 'Filesystem use' df -h / /home
  run 'Block devices' lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
  run 'Real mounts' findmnt --real --output SOURCE,TARGET,FSTYPE,OPTIONS
}

steam_profile() {
  run 'SteamOS release' cat /etc/os-release
  run 'Kernel' uname -r
  run 'Steam storage filesystems' df -h / /home
  run 'User-service failures' systemctl --user --failed --no-pager
}

flatpak_profile() {
  run 'Flatpak applications' flatpak list --app --columns=application,origin,version,installation
  run 'User Flatpak history' flatpak history --user --columns=time,change,application,installation
  run 'System Flatpak history' flatpak history --system --columns=time,change,application,installation
}

network_profile() {
  run 'NetworkManager state' nmcli general status
  run 'Network devices' nmcli device status
  run 'Interface addresses' ip -br addr
  run 'Radio blocks' rfkill list
}

bluetooth_profile() {
  run 'Bluetooth radio blocks' rfkill list bluetooth
  run 'Bluetooth service' systemctl is-active bluetooth
  run 'User-service failures' systemctl --user --failed --no-pager
}

audio_profile() {
  run 'PipeWire service' systemctl --user is-active pipewire
  run 'WirePlumber service' systemctl --user is-active wireplumber
  run 'Audio routes and devices' wpctl status
}

input_profile() {
  run 'Input device names' awk -F= '/^N: Name=/{print $2}' /proc/bus/input/devices
  run 'User-service failures' systemctl --user --failed --no-pager
}

run_profile() {
  case "$1" in
    system) system_profile ;;
    storage) storage_profile ;;
    steam) steam_profile ;;
    flatpak) flatpak_profile ;;
    network) network_profile ;;
    bluetooth) bluetooth_profile ;;
    audio) audio_profile ;;
    input) input_profile ;;
    *) printf 'Unknown profile: %s\n' "$1" >&2; exit 2 ;;
  esac
}

printf '# SS read-only diagnostic collection\n'
printf '# Profile: %s\n' "$profile"
printf '# Review and sanitize output before sharing. No data is uploaded.\n'

if [[ "$profile" == all ]]; then
  for selected_profile in system storage steam flatpak network bluetooth audio input; do
    printf '\n# Profile: %s\n' "$selected_profile"
    run_profile "$selected_profile"
  done
else
  run_profile "$profile"
fi
