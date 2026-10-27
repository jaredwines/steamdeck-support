# Support coverage matrix

## Purpose

Use this matrix to see what Steam Deck Support (SS) can diagnose, change, and
verify without confusing written guidance with on-device evidence. The linked
runbook remains authoritative when this summary and a procedure differ.

## Rating key

- **Verified** — the recorded procedure produced its expected result on the
  stated SteamOS build.
- **Partial** — only part of the procedure or a read-only check was observed.
- **Reviewed** — commands and upstream guidance were reviewed, but the change
  was not performed on the Deck.
- **Gap** — SS does not yet provide a complete safe path.

## Current coverage

| Area | Diagnose | Repair or configure | Recovery | Evidence | Priority |
| --- | --- | --- | --- | --- | --- |
| SSH access | [Remote access](remote-access.md) | Enable, authenticate, revoke, disable | Preserve a working session and restore `authorized_keys` backup | Partial | High |
| Temporary sudo | [Sudo access](sudo-access.md) | Establish and clear temporary authorization | Clear cached authorization; use local access | Reviewed | High |
| GitHub SSH | [GitHub access](github-access.md) | Create, test, and revoke a dedicated key | Restore intended remote and key access | Partial: authentication and repository read verified | Medium |
| Steam or Proton launch | [Steam and Proton](steam-proton.md) | Reversible Steam-managed checks | Restore launch option and compatibility selection | Reviewed | High |
| Internal storage and microSD | [Storage and microSD](storage-microsd.md) | Steam-managed move/removal and library recovery | Stop writes; restore previous library state | Partial: read-only attribution verified | High |
| Flatpak and Discover | [Flatpak applications](flatpak.md) | Update or repair the identified installation | Preserve app data; reverse only documented changes | Partial: read-only inspection verified | High |
| Wi-Fi and Bluetooth | [Connectivity](connectivity.md) | Reconnect or approved re-pairing | Restore known connection state | Partial: baseline and recovery-state capture verified | High |
| Controls, audio, docks, displays | [Hardware and peripherals](hardware-peripherals.md) | Isolate and reverse one setting or device at a time | Return to built-in hardware and prior settings | Reviewed | Medium |
| Battery, charging, heat, performance | [Power and performance](power-performance.md) | Remove workload or setting causes | Return to stock limits; escalate hardware symptoms | Reviewed | Medium |
| SteamOS updates and boot | [Updates and boot](updates-boot.md) | Steam UI update path and Valve recovery choices | Previous OS, repair, or recovery media | Reviewed | High |
| Saves and personal data | [Save data](save-data.md) | Protect and restore identified data | Independent restore test | Reviewed | High |
| General diagnostics | [Diagnostics](diagnostics.md) | Routes to an owning procedure | Procedure-specific | Verified read-only collection | High |
| Backup readiness | [Backup and restore](backup-and-restore.md) | Create a selected encrypted off-device backup | Representative independent restore | Reviewed | Critical |
| Full-system recovery | [Full-system restore](full-system-restore.md) | Valve recovery workflow | Layered restore with checkpoints | Reviewed, evidence level 1 | Critical |
| Non-Steam artwork | [Non-Steam games](non-steam-games.md) | Install four artwork formats | Timestamped artwork backup | Partial | Medium |

## Promotion rule

Promote an area only after the owning runbook's expected result, functional
check, recovery path, and any required Gaming Mode check have been observed.
Update this matrix and [Compatibility status](compatibility-status.md) in the
same change. A lower evidence rating is not a failure when higher-risk testing
would be artificial or unsafe.

## Verification

Run `bash scripts/validate-repository.sh`. Confirm every link resolves and the
evidence label agrees with the owning runbook before publishing an update.
