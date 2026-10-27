# Backup and restore readiness

## Purpose and status

Use this runbook before a destructive Steam Deck operation to inventory data,
create encrypted off-device copies, and prove that representative data can be
restored. It is the required backup gate for [Full-system restore](full-system-restore.md).

This procedure defines acceptance evidence without prescribing one backup
product. Backup tools, filesystems, applications, and save locations vary; stop
when the selected tool cannot preserve or restore the metadata the data needs.
The procedure has been reviewed locally but not completed on this Deck.

## Quick path

Inventory every irreplaceable source, copy it to an identified encrypted
off-device destination, verify the stored copy after reconnecting it, and prove
a representative restore into a new location. Do not approve destructive work
until every applicable acceptance item passes.

## Approval and prerequisites

Inventory commands below are read-only. Obtain the owner's approval before
mounting backup storage, copying private data, creating archives or checksums,
or performing a restore test. Confirm the intended Deck, backup destination,
available space, encryption method, and access to protected credentials.

Keep the completed worksheet, manifests, logs, account data, recovery codes,
tokens, private keys, and raw diagnostics in encrypted storage outside Steam
Deck Support (SS). Never use the recovery-media USB as a backup destination.

## Inventory

When the Deck boots, these read-only commands help establish the baseline:

```bash
cat /etc/os-release
uname -r
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
df -h / /home
flatpak list --app --columns=application,origin
find ~/.var/app -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort
find ~/Applications -mindepth 1 -maxdepth 2 -printf '%P\n' | sort
git -C /home/deck/steamdeck-support log -1 --format='%H %cI %s'
git -C /home/deck/steamdeck-support remote -v
```

Missing paths are valid findings; do not create them. Review output locally
because names and labels may be private. Check Steam Cloud in Steam for each
important game rather than assuming library membership means Cloud support.

Assess personal directories, browser and application profiles, Flatpak data
under `~/.var/app`, Steam `userdata`, each important game's documented save
locations, non-Steam prefixes, launcher data, and intentional configuration.
Treat Steam `compatdata` individually: it can contain irreplaceable saves even
when downloaded game files do not need backup.

Inventory every internal-drive operating system, partition, and boot
customization. For another operating system, separately record its data,
reinstall method, license or activation recovery, and encryption-recovery
material in protected storage. A SteamOS backup does not protect another
operating system or its bootloader.

## Private worksheet

Use `not applicable`, `unknown`, or `not recoverable` instead of blanks:

```text
Inventory review date/person:
Deck model and storage size:
SteamOS channel, version/build, and kernel:
Internal partitions, operating systems, boot customizations, and accepted losses:
Internal storage used/free; microSD and external-storage contents:
Steam account recovery verified:
Games with Cloud confirmed; non-Cloud saves:
Non-Steam games, launchers, prefixes, and saves:
Flatpak/Discover applications and sources:
Personal files and application-data paths:
Intentional customizations and owning SS runbook:
Required SSH/GitHub public-key fingerprints:
Backup tool/version, destination, date, encryption, and source manifest:
Backup result, archive ID or checksum, and exclusions:
Independent restore-test destination, sample, result, and date:
Known exclusions and accepted losses:
Owner acceptance record:
```

## Create and prove the backup

1. **Classify.** Mark every item as Steam Cloud, reproducible download,
   backed-up local data, intentionally excluded, or not recoverable. Confirm
   Cloud status per game and resolve conflicts before copying.
2. **Protect credentials.** Keep account recovery codes, disk-recovery
   material, passwords, tokens, and private keys only in the owner's protected
   credential storage, never in SS or an unencrypted manifest.
3. **Copy.** Use a documented tool that reports errors, preserves required
   metadata, and writes to an encrypted off-device destination. Record its
   version, exact source manifest, destination, times, result, exclusions, and
   an archive identifier or checksum. Check the resolved destination and free
   space first; do not use an unresolved device, mount, or placeholder.
4. **Retest the stored copy.** Reconnect or remount the destination, then run
   the checksum or backup-tool verification so the check does not rely only on
   cached data.
5. **Restore-test.** Decrypt the backup and restore representative items into
   a new empty test directory, never over originals. On another device when
   practical, open or compare a personal file, a non-Cloud save, and each
   important application-data format. Confirm required ownership, permissions,
   filenames, and symlinks.
6. **Add resilience.** Keep irreplaceable data in two verified copies on
   separate destinations, with at least one disconnected from the Deck during
   the destructive operation.

After a wipe, restore selected data instead of the entire old home directory;
this avoids reintroducing stale caches, permissions, and obsolete settings.

## Backup acceptance test

- [ ] The destination is outside the Deck, identified, encrypted, and decryptable on another device.
- [ ] The copy completed without unexplained errors and has a plausible size.
- [ ] Verification passes after reconnecting or remounting the destination.
- [ ] The manifest accounts for every internal operating system, partition, important source, and exclusion.
- [ ] Irreplaceable data has two verified copies on separate destinations, with one disconnected during destructive work.
- [ ] A restore into a new empty location succeeds for a personal file, non-Cloud save, and applicable application data.
- [ ] Required ownership, permissions, filenames, and symlinks survive the restore test where applicable.
- [ ] The recorded SS commit is accessible from another device.
- [ ] The owner accepts every exclusion and unrecoverable item.

Do not approve a destructive operation when any applicable item fails or is
unknown. Record why a genuinely inapplicable item does not apply.

## Verification and recovery

Retain the actual backups after deleting only the temporary restore-test copy.
Record the tool and version, manifest, destination, encryption confirmation,
verification result, restore-test samples, exclusions, and owner acceptance.
If verification or restoration fails, preserve the source data, stop the
destructive plan, correct the backup method, and repeat the complete acceptance
test. Do not treat a second untested copy as recovery.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Procedure and read-only inventory commands reviewed locally | Ready for use; backup and restore test remain unverified |
