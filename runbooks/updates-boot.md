# SteamOS updates and boot problems

## Purpose and status

Use this runbook when a stable SteamOS update fails or the Deck does not reach
normal Gaming Mode. Prefer the least destructive official recovery option. The
complete procedure has not been verified on this Deck.

## Quick path

Record the exact update or boot state, stabilize power and storage, consult
Valve's current choices, and select the least destructive approved path. Never
wipe without a proven backup and immediate explicit approval.

## Approval and prerequisites

Recording the displayed state is diagnostic. Installing updates, restarting,
using rollback or repair, preparing recovery media, factory resetting, and
re-imaging require approval appropriate to their impact. A factory reset or
re-image is destructive and additionally requires the backup acceptance test
and explicit approval immediately before execution.

## Update failure while SteamOS boots

1. Record the exact message, stable/beta channel, power source, free space, and
   whether normal Gaming Mode still works.
2. Do not repeatedly retry on low storage or unstable power.
3. Review Valve's current support instructions before acting; labels and button
   sequences can change.
4. With approval, resolve the identified prerequisite and retry through Steam's
   interface. Do not switch channels as a generic repair.

## Boot failure

1. Record the last known-good state and exact screen or behavior. Avoid repeated
   forced shutdowns of a responsive system.
2. Disconnect optional peripherals and storage without removing a device that
   contains an active operating system or required recovery data.
3. Review the current Valve recovery choices in
   [Full-system restore](full-system-restore.md): previous OS, repair, factory
   reset, or full re-image.
4. Choose the least destructive option that matches the observed failure. Stop
   if labels, target disks, backup state, or expected results differ.

## Verification and recovery

After an approved update or recovery, verify controls, display, audio, Wi-Fi,
charging, sleep/wake, storage, a Steam game, and Gaming Mode. Record the build
and any lost or restored state. If the official flow fails or the storage target
is unclear, stop and contact Steam Support rather than improvising partitions
or recovery-shell commands.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Least-destructive routing and Valve recovery boundary reviewed | Ready for use; update and boot repairs remain unverified |
