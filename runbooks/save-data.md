# Save data and personal files

## Purpose and status

Use this runbook to identify, protect, and restore game saves or personal data
before repair, prefix replacement, uninstall, or recovery. Locations vary by
game and launcher; no generic path proves a save is protected.

## Quick path

Identify the exact active save source and Cloud state, copy it to encrypted
off-device storage, verify the stored copy, and prove a restore into a new empty
location before risking the original.

## Approval and prerequisites

Inventory may expose private filenames and account paths. Obtain approval before
copying private data, mounting backup storage, creating checksums, restoring, or
changing files. Confirm the exact game App ID, launcher, current prefix, Steam
Cloud state, backup destination, encryption, and available space.

## Identify the source

1. Check the game's current Steam Cloud status and resolve conflicts; do not
   infer Cloud support from library membership.
2. Consult authoritative game or launcher documentation for save locations.
3. For Windows games, distinguish the active Proton prefix from obsolete
   prefixes. Do not choose solely by modification time.
4. Include configuration, screenshots, mods, and launcher data only when the
   owner needs them and their restoration is understood.

Keep raw inventory and manifests in encrypted storage outside SS.

## Protect and prove

1. Close the game, launcher, Steam synchronization, Proton, and Wine processes
   normally before copying.
2. Copy the identified source to an encrypted off-device destination using a
   tool that reports errors and preserves required metadata.
3. Record a manifest and checksum or backup identifier privately.
4. Reconnect the destination and verify the stored copy.
5. Restore into a new empty test directory, never over the original. Compare or
   open representative data and confirm names, permissions, and symlinks.

Follow [Backup and restore](backup-and-restore.md) when the operation risks more
than one game's data or precedes destructive system work.

## Verification and recovery

For an approved real restore, preserve the current destination first, restore
only the intended data, launch the game offline if Cloud conflict is possible,
and verify the expected save. Re-enable synchronization only after choosing the
correct copy. If validation fails, keep originals and both copies unchanged and
stop; do not overwrite the remaining known-good data.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Source identification and independent restore-test procedure reviewed | Ready for use; representative restore remains unverified |
