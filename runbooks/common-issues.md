# Common SteamOS issues

## Purpose and status

Use this runbook to triage common storage, Flatpak, game compatibility, input,
audio, Bluetooth, and network problems before choosing a narrower procedure.
It favors Steam's interfaces and read-only evidence over system modification.

This runbook was reviewed on 2026-10-26 against Valve's current Steam Deck
[basic-use guide](https://help.steampowered.com/en/faqs/view/69E3-14AF-9764-4C28),
[software guide](https://help.steampowered.com/en/faqs/view/7DD4-C618-182E-0E49),
the official [Proton project](https://github.com/ValveSoftware/Proton), and
[Flatpak documentation](https://docs.flatpak.org/en/latest/using-flatpak.html).
Its diagnostic commands were checked locally, but no repair in this runbook
has been verified on this Deck.

## Approval and prerequisites

Reading status and using Steam's input test are diagnostic. Obtain the owner's
approval before installing updates, restarting the Deck, changing a game's
compatibility tool or controller layout, repairing Flatpak data, forgetting a
network or Bluetooth device, uninstalling software, moving game data, or
formatting storage. Formatting, deletion, and prefix replacement are
destructive and require a verified backup and recovery plan.

Record the symptom, when it began, affected software or hardware, SteamOS
build, kernel, and available storage. Never collect network passwords, account
data, device serial numbers, or complete logs in SS.

## Establish a read-only baseline

In Desktop Mode, collect only what is relevant:

```bash
cat /etc/os-release
uname -r
df -h / /home
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
systemctl --failed --no-pager
systemctl --user --failed --no-pager
flatpak list --app --columns=application,origin,version,installation
flatpak history --user --columns=time,change,application,installation
flatpak history --system --columns=time,change,application,installation
```

Missing paths, an empty failure list, and an unavailable optional command are
findings; do not create or change anything to make the baseline succeed.
Sanitize mount labels, device models, application history, and network details
before sharing them.

## Isolate the problem

1. Confirm whether the symptom affects Gaming Mode, Desktop Mode, one game,
   one user application, or the whole Deck.
2. Check **Steam > Settings > System** for pending stable-channel updates. With
   approval, install an available update and restart through Steam, then retest.
3. Exit third-party launchers and Desktop Mode applications, then retest the
   smallest affected feature.
4. Disconnect optional docks, hubs, displays, storage, and Bluetooth devices
   one at a time when it is safe to do so.
5. Stop when the failure becomes narrower; use the matching section below and
   change only one variable before each test.

Do not switch update channels, force power off a responsive Deck, or apply
Internet commands merely because they describe a similar symptom.

## Storage

Use **Steam > Settings > Storage** to confirm which library is full or missing.
Compare it with `df` and `lsblk`; do not assume a missing microSD card is safe
to format. Reseat removable storage only after software using it is closed.

Moving or uninstalling a game through Steam requires approval. Before deleting
anything outside Steam, identify its owner, size, backup state, and recovery
source. Never delete `compatdata`, shader caches, Flatpak data, or unknown
files as a generic space-recovery step. If a filesystem reports errors or a
device repeatedly disconnects, stop writes and escalate rather than repairing
it in place.

## Flatpak and Discover applications

Use the application ID and installation from the baseline rather than guessing
from a display name. With approval, update through Discover or use the matching
command for a user or system installation:

```bash
flatpak update --user <application-id>
flatpak update --system <application-id>
```

Run only one of those commands for the installation shown by the baseline.

Expected result: the update completes without unexplained errors and the
affected application launches. If the installation appears inconsistent,
review `flatpak repair --help` first. `flatpak repair --user` changes local
Flatpak data and requires separate approval; record its output and retest the
specific application. Do not use `sudo flatpak`, reset application
permissions, remove unused runtimes, or delete `~/.var/app` as a generic fix.

## Steam games and Proton

Check the game's current Deck Verified details, pending downloads, and recent
configuration changes. Verify the game files through Steam only with approval,
because Steam may replace files or download data. For a Windows game, record
the selected compatibility tool before changing it and prefer a Proton version
supplied by Steam.

For one diagnostic launch, the owner may approve this launch option:

```text
PROTON_LOG=1 %command%
```

Remove it after the test. The resulting `~/steam-<appid>.log` can contain paths,
account names, and system details; keep it outside SS and sanitize excerpts.
Never delete or replace a game's `compatdata/<appid>` prefix without confirming
the App ID, save locations, Cloud state, backup, and recovery plan.

## Input, audio, Bluetooth, and network

- For built-in controls, use **Steam > Settings > Controller > Test Controller
  Inputs**. Record which input fails without changing layouts first.
- For a game-specific control problem, record the current layout before trying
  a Valve template or another known layout with approval.
- For audio, confirm the selected output and disconnect optional audio devices
  before retesting the built-in speakers.
- For Bluetooth, reconnect first. Forgetting and re-pairing a device requires
  approval and access to the device's pairing method.
- For Wi-Fi, compare another network only when authorized. Do not record the
  SSID, password, local addresses, or router configuration in SS.

If hardware input tests fail consistently, storage disconnects repeatedly, or
the issue persists on an updated stock configuration, preserve sanitized
evidence and contact Steam Support rather than applying unrelated system
changes.

## Verification and recovery

Retest the original symptom after each approved change. A successful result
must include the affected feature, a representative Gaming Mode check when
appropriate, and confirmation that unrelated controls, network, and Steam
operation remain normal. Reverse the last reversible change if it causes a
regression; otherwise stop at the last known-good state.

Record the baseline, commands and UI actions, expected and observed results,
recovery used or available, and unresolved risk according to the
[verification standard](verification.md). Add an on-device compatibility entry
only after the complete procedure and recovery path have been observed.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Compared conservative triage with current Valve, Proton, and Flatpak documentation | Ready for use; repairs remain unverified |
