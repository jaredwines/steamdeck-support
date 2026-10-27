# Storage and microSD

## Purpose and status

Use this runbook for low storage, missing Steam libraries, or removable-storage
problems. It prioritizes identification and preservation over cleanup. No repair
in this runbook has yet been verified on this Deck.

## Quick path

Compare Steam Storage with filesystems, devices, mounts, and top-level usage;
identify the owner of data before moving or deleting it, and never format an
uncertain device.

## Approval and prerequisites

The baseline is read-only. Obtain approval before moving or uninstalling games,
mounting or repairing filesystems, changing Steam libraries, or formatting any
device. Formatting and deletion require a proven backup and recovery plan.
Record which library is affected and close software using removable storage
before physically removing it.

## Read-only baseline

Compare **Steam > Settings > Storage** with:

```bash
df -h / /home
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
findmnt --real --output SOURCE,TARGET,FSTYPE,OPTIONS
```

Review labels and models locally because they may identify private devices. A
device visible to `lsblk` but absent from Steam is different from a device not
detected at all. Do not format a device merely because Steam offers to do so.

## Low-space path

1. Identify whether games, Desktop files, application data, or another category
   owns the space. Steam Storage covers Steam-managed categories; for a local
   read-only summary of non-Steam usage, use:

   ```bash
   du -x -h --max-depth=1 /home/deck 2>/dev/null | sort -h
   du -x -h --max-depth=1 ~/.local ~/.var 2>/dev/null | sort -h
   ```

   These commands may take time and directory names can be private. Review them
   locally. A large category narrows the investigation but does not authorize
   deleting it.
2. Prefer Steam's Storage interface for moving or uninstalling Steam games.
3. Before deleting anything outside Steam, identify its owner, size, backup,
   and recovery source.
4. Do not delete shader caches, `compatdata`, Flatpak data, logs, or unknown
   directories as generic cleanup.

## Missing-microSD path

1. Close games and applications using the card, then reseat it once.
2. Recheck Steam Storage, `lsblk`, and `findmnt`.
3. If the filesystem reports errors, the card disconnects repeatedly, or the
   device is absent, stop writes and preserve evidence.
4. Add an existing library through Steam only after the expected filesystem and
   content have been identified. Do not create a new library over uncertain data.

## Verification and recovery

Confirm free space or library visibility in both Steam and the read-only tools.
Launch a game from each changed library in Gaming Mode. If a move or library
change fails, stop before deleting the source. Filesystem repair needs a
device-specific backup, recovery plan, and separate approval.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | 3.9.5 / 20261023.100 | Read-only filesystem baseline and non-Steam `du` attribution | Passed: baseline collector and both bounded attribution commands completed; moves, cleanup, filesystem repair, and microSD recovery remain unverified |
