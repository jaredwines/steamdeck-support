# Symptom triage

## Purpose and status

Use this page to reach the smallest relevant SS procedure. It authorizes no
change. Begin with read-only evidence, change one variable at a time, and stop
when the target, consequence, approval, or recovery path is unclear.

## Thirty-second route

| Symptom | Start here | Safe first check |
| --- | --- | --- |
| Cannot reach the Deck remotely | [Remote access](remote-access.md) | Confirm the Deck is awake and inspect `systemctl is-active sshd` locally |
| A command needs administrator access | [Sudo access](sudo-access.md) | Stop and obtain approval before any sudo check |
| A Steam or Proton game fails | [Steam and Proton](steam-proton.md) | Determine whether one game or all Steam games are affected |
| Storage is full or microSD is missing | [Storage and microSD](storage-microsd.md) | Compare Steam Storage with `df -h` and `lsblk` |
| Discover or a Flatpak app fails | [Flatpak applications](flatpak.md) | Identify the exact application ID and user/system installation |
| Wi-Fi or Bluetooth fails | [Connectivity](connectivity.md) | Determine whether other devices or only the Deck are affected |
| Controls, audio, dock, or display fails | [Hardware and peripherals](hardware-peripherals.md) | Disconnect optional hardware and test the built-in path when safe |
| Battery, charging, heat, or speed is abnormal | [Power and performance](power-performance.md) | Record power source, workload, charge state, and whether the symptom persists idle |
| An update failed or SteamOS will not boot | [Updates and boot](updates-boot.md) | Record the exact screen and avoid repeated force-off cycles |
| Saves or personal files are at risk | [Save data](save-data.md) | Stop writes and identify whether Steam Cloud actually covers the game |
| A wipe or major recovery is proposed | [Full-system restore](full-system-restore.md) | Do not wipe; first pass the backup acceptance test |
| The symptom is still unclear | [Diagnostics](diagnostics.md) | Collect only relevant read-only baseline data |

## Isolation sequence

1. Record the original symptom and when it began.
2. Decide whether it affects one game or app, Gaming Mode, Desktop Mode, or the
   entire Deck.
3. Note the current SteamOS build without installing an update.
4. Remove one optional peripheral or close one optional application at a time.
5. Route to the owning runbook as soon as the scope narrows.
6. Obtain approval before the first change and retest the original symptom
   immediately afterward.

Do not switch update channels, delete caches or prefixes, format storage,
disable read-only protection, paste Internet commands, or use sudo as generic
troubleshooting.

## Approval and privacy

Read-only checks still can expose local addresses, device names, application
history, and account-related paths. Review output locally and sanitize it before
sharing. Configuration changes, software installation, restarts, repairs,
forgetting devices or networks, and destructive actions require owner approval.

## Verification

Success means the symptom reached one owning runbook without an unsafe or
unexplained step. After an approved repair, use that runbook's functional and
Gaming Mode checks and record the result under the verification standard.
