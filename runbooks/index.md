# Steam Deck Support Runbooks

## Start here

This is the required entry point for remote command-line support of a Steam
Deck running SteamOS. The expected target is `deck@192.168.1.67`, but verify
the device, network address, and SSH host key before treating it as the Deck.

Use only the runbook that matches the task. Do not use a procedure when its
prerequisites, authorization, verification, or recovery path are unclear.

## Update the SS

SS means **Steam Deck Support**: this repository and its documentation. After
verified, reusable support work, follow the [Support session](support-session.md)
runbook to update the SS when its guidance needs to change.

## Safety rules

- Obtain the owner's explicit approval before using `sudo` or making a
  destructive, security-sensitive, system-wide, or difficult-to-reverse
  change.
- Never request, record, display, or share passwords, private SSH keys,
  tokens, or host-key material.
- Prefer reversible user-level changes. Do not disable SteamOS read-only
  protection unless the task explicitly requires it and includes a recovery
  plan.
- Preserve normal Steam and Gaming Mode operation. After significant work,
  verify Gaming Mode before handoff.
- A SteamOS update may overwrite custom configuration; record that risk where
  it applies.

## Fast path

Use this only when the Deck and its host key have already been verified and a
valid SSH key is configured:

```bash
ssh -i <private-key-path> deck@192.168.1.67
whoami
```

`whoami` must return `deck`. If the task requires `sudo`, obtain the owner's
explicit approval before checking access with `sudo -l`, then follow
[Sudo access](sudo-access.md). When approved sudo work is complete, run
`sudo -k` to clear temporary authorization and then `exit`.

## Choose a task

If the cause is not yet known, start with [Symptom triage](triage.md). For a
coverage overview, see the [Support coverage matrix](coverage-matrix.md) and
[Compatibility status](compatibility-status.md). The
[SS readiness scorecard](readiness-scorecard.md) shows which 10/10 acceptance
gates have passed and which still require evidence or approval.

### Something is broken

Start with [Symptom triage](triage.md), then follow the single focused runbook
it selects. Collect read-only evidence before approving a change.

### Configure something

Use [Remote access](remote-access.md), [Sudo access](sudo-access.md),
[GitHub access](github-access.md), or [Non-Steam games](non-steam-games.md).
Record the current state and recovery path before changing it.

### Back up or recover the Deck

Start with [Save data](save-data.md) or
[Backup and restore readiness](backup-and-restore.md). A full wipe additionally
requires [Full-system restore](full-system-restore.md), a passed backup gate,
and explicit approval immediately before erasure.

| Task | Runbook |
| --- | --- |
| Set up, verify, or disable SSH access | [Remote access](remote-access.md) |
| Use or configure temporary shared sudo access | [Sudo access](sudo-access.md) |
| Use Git or restore GitHub SSH access on the Deck | [GitHub access](github-access.md) |
| Prepare and prove backups before destructive work | [Backup and restore readiness](backup-and-restore.md) |
| Plan or recover from a full internal-drive wipe | [Full-system restore](full-system-restore.md) |
| Plan, perform, document, and hand off support work | [Support session](support-session.md) |
| Collect safe diagnostics or resolve common access failures | [Diagnostics](diagnostics.md) |
| Triage storage, applications, games, input, audio, or networking | [Common issues](common-issues.md) |
| Resolve a Steam or Proton launch problem | [Steam and Proton](steam-proton.md) |
| Investigate internal storage or microSD | [Storage and microSD](storage-microsd.md) |
| Diagnose a Flatpak or Discover application | [Flatpak applications](flatpak.md) |
| Diagnose Wi-Fi or Bluetooth | [Connectivity](connectivity.md) |
| Diagnose controls, audio, docks, or displays | [Hardware and peripherals](hardware-peripherals.md) |
| Diagnose battery, charging, heat, or performance | [Power and performance](power-performance.md) |
| Handle SteamOS updates or boot trouble | [Updates and boot](updates-boot.md) |
| Protect or restore saves and personal data | [Save data](save-data.md) |
| Add a non-Steam game, launcher, or artwork | [Non-Steam games](non-steam-games.md) |
| Record compatibility evidence or review a procedure | [Verification standard](verification.md) |
| Prepare a private support-session record | [Session record template](support-session-record-template.md) |

## Evidence snapshot

This snapshot prevents documentation review from being mistaken for Deck
compatibility. Detailed evidence remains in each owning runbook.

| Area | Strongest recorded evidence as of 2026-10-26 |
| --- | --- |
| Remote access | Key-authenticated SSH reached the expected `deck` account on SteamOS 3.9.5 build 20261023.100 with strict known-host checking; setup, revocation, and shutdown were not repeated. |
| Sudo access | Procedure is available; no dated on-device compatibility entry is recorded. |
| GitHub access | Existing dedicated-key authentication and read-only `origin` access passed on SteamOS 3.9.5 build 20261023.100; creation and revocation were not repeated. |
| Backup and restore readiness | Documentation and read-only inventory review only; no backup/restore acceptance test is recorded. |
| Full-system restore | Evidence level 1 documentation review only; media boot, re-image, and restored layers remain unverified. |
| Common issues | Read-only storage attribution, Flatpak inspection, and connection-state capture completed on SteamOS 3.9.5 build 20261023.100; repairs remain unverified. |
| Diagnostic collector | All eight read-only profiles completed on SteamOS 3.9.5 build 20261023.100; 26 command sections were available. This verifies collection, not repairs. |
| Non-Steam shortcuts and artwork | Stored Battle.net and WowUp shortcut IDs were read on-device; all eight installed artwork files matched SS byte for byte. Steam restart and visual Gaming Mode checks remain pending. |
| Tabletop acceptance | A fresh independent review scored all 20 scenarios at 200/200 after remediation, with no critical failure; this does not replace on-device repair evidence. |

## Before handoff

- [ ] Commands run, files changed, checks performed, and unresolved risks are recorded.
- [ ] Required verification passed; Gaming Mode was checked after significant work.
- [ ] Temporary sudo authorization was cleared, if used.
- [ ] Remote access was reviewed or disabled when it is no longer needed.
- [ ] Verified reusable knowledge was added to the applicable runbook.
- [ ] SteamOS build, procedure result, and any deviations were recorded.
