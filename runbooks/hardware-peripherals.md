# Controls, audio, docks, and displays

## Purpose and status

Use this runbook to isolate built-in controls, controller layouts, audio output,
docks, and external displays. It favors built-in hardware and one-variable
tests. No repair in this runbook has yet been verified on this Deck.

## Quick path

Test the built-in path first, disconnect optional hardware safely, and restore
one recorded layout, output, cable, or display variable at a time before
escalating a persistent hardware-level failure.

## Approval and prerequisites

Steam input tests and observation are diagnostic. Obtain approval before
changing layouts or display settings, forgetting devices, updating firmware,
or restarting the Deck. Record connected hardware and the previous working
state. Never force-disconnect storage through a dock while it is in use.

## Controls

1. Use **Steam > Settings > Controller > Test Controller Inputs**.
2. If built-in input fails there, test after safely disconnecting optional
   controllers and docks. Persistent failure warrants Steam Support rather than
   game-specific remapping.
3. If only one game fails, record its current layout. With approval, test one
   Valve template or known layout, then restore the original if ineffective.

## Audio

1. Record the selected output and whether the problem affects built-in speakers,
   headphones, Bluetooth, HDMI, or one application.
2. Disconnect optional audio paths and retest built-in speakers.
3. Select the intended output through SteamOS with approval. Do not replace
   system audio configuration as generic troubleshooting.

## Docks and displays

1. Safely close software using docked storage, then reduce to power, one known
   cable, and one display.
2. Test the Deck display and charging independently of the dock.
3. Add the display, USB devices, Ethernet, and storage one at a time.
4. Record resolution and refresh rate before an approved display-setting change.

## Verification and recovery

Exercise the original control, audio stream, or display activity in Gaming Mode.
For docks, verify charging and each required port without reconnecting all
devices at once. Restore the prior layout or display setting if the change
regresses. Stop for power instability, heat, smell, damage, or repeated device
disconnection.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Isolation and reversible SteamOS settings reviewed | Ready for use; repairs remain unverified |
