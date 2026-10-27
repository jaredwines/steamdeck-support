# Steam and Proton launch problems

## Purpose and status

Use this runbook when one or more Steam games fail to launch, regress, or exit
unexpectedly. It covers conservative isolation and Steam-managed recovery. No
repair in this runbook has yet been verified on this Deck.

## Quick path

Determine whether one game, all Windows games, or all Steam games are affected,
record the current launch and compatibility settings, then test one approved,
reversible Steam-managed change at a time.

## Approval and prerequisites

Reading settings and status is diagnostic. Obtain approval before downloading,
verifying files, changing compatibility tools or launch options, deleting data,
or restarting Steam or the Deck. Record the game name and App ID, current
compatibility selection, launch options, affected mode, and when the failure
began. Confirm save and Steam Cloud state before any action involving data.

## Read-only baseline

Determine whether the problem affects one game, all Windows games, or all Steam
games. Check the game's Downloads and Properties pages, available storage, and
current compatibility selection. On the command line, collect only relevant
state:

```bash
cat /etc/os-release
uname -r
df -h / /home
```

Do not infer a safe fix from a different game's App ID or prefix.

## Isolate and repair

1. Undo the most recent game-specific launch-option change with approval, then
   retest.
2. If only one game is affected, review its current Deck compatibility details
   and known game-specific requirements before changing Proton.
3. With approval, verify game files through **Properties > Installed Files**.
   Expect Steam to inspect and possibly replace or download files.
4. For a Windows game, record the current selection before testing one
   Steam-supplied Proton version. Revert immediately if it regresses.
5. For one diagnostic launch, the owner may approve `PROTON_LOG=1 %command%`.
   Remove it afterward and keep the resulting log outside SS; it can expose
   private paths and system details.

Never delete or replace `compatdata/<appid>`, use a third-party Proton build, or
apply a game-specific Internet workaround without separately confirming source,
save coverage, rollback, and approval.

## Verification and recovery

Launch the affected game twice from Gaming Mode, reach a representative menu or
save, test controls and audio, and confirm another known-good Steam game still
works. Restore the recorded launch options and compatibility selection if the
test change fails. Stop before prefix replacement or save deletion.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Conservative Steam and Proton isolation procedure reviewed | Ready for use; repairs remain unverified |
