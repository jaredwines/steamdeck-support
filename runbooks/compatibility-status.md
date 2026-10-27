# Compatibility status

## Purpose

This dashboard summarizes the strongest recorded evidence for version-sensitive
SS procedures. It must remain conservative: a documentation review is not
on-device compatibility, and one verified sub-step does not verify a complete
workflow.

## Current evidence

| Area | Strongest evidence | SteamOS version/build | Last review | Remaining verification |
| --- | --- | --- | --- | --- |
| Remote access | Existing key-authenticated connection verified | 3.9.5 / 20261023.100 | 2026-10-26 | Enablement, new-key installation, revocation, and shutdown |
| Sudo access | Documentation review | Not tested | 2026-10-26 | Complete temporary authorization and clearing lifecycle |
| GitHub access | Existing dedicated key authenticated and read-only `origin` access succeeded | 3.9.5 / 20261023.100 | 2026-10-26 | Key creation, clone, and revocation lifecycle |
| Diagnostic profiles | All eight read-only profiles completed; 26 command sections available | 3.9.5 / 20261023.100 | 2026-10-26 | Sanitized output review during real symptom cases; no repair claim |
| Storage, Flatpak, and connectivity baselines | Focused read-only attribution, application inspection, and connection-state queries completed | 3.9.5 / 20261023.100 | 2026-10-26 | Actual failure classification, approved repair, rollback, and functional verification |
| Common issue repairs | Commands and upstream documentation reviewed | Not tested | 2026-10-26 | At least one complete case in each high-frequency category |
| Backup and restore | Procedure reviewed | Not tested | 2026-10-26 | Encrypted copy, remount verification, and independent representative restore |
| Recovery media | Valve documentation reviewed | Not tested | 2026-10-26 | Write, validate, boot to recovery desktop, and return to Gaming Mode |
| Full re-image and layered restore | Evidence level 1 documentation review | Not tested | 2026-10-26 | Levels 2 through 4 when independently justified and approved |
| Non-Steam shortcuts and artwork | Stored IDs and eight installed files verified | 3.9.5 / 20261023.100 | 2026-10-26 | Steam restart and visual four-format Gaming Mode check |

## Evidence ladder

1. **Reviewed** — procedure and authoritative documentation checked.
2. **Observed read-only** — relevant state inspected on the Deck.
3. **Changed and verified** — approved change and functional result observed.
4. **Recovery verified** — rollback or representative restoration demonstrated.
5. **End-to-end accepted** — complete workflow and owner acceptance recorded.

Use the lowest level that accurately describes the full claimed scope. Do not
perform a risky action solely to raise an evidence level.

## Freshness rule

Review version-sensitive entries after a major SteamOS release, an upstream
procedure change, or any observed contradiction. `scripts/check-compatibility-status.py`
flags dates older than 180 days as review candidates; age alone does not erase
valid evidence, and a newer date must reflect a real review.

## Verification

Compare this dashboard with the compatibility record in every owning runbook,
then run `bash scripts/validate-repository.sh`.
