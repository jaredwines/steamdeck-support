# Non-Steam games, launchers, and artwork

## Purpose

Use this runbook as the entry point for non-Steam shortcuts. The
[Non-Steam Game & Artwork Setup Guide](../steam/add-non-steam-game-and-artwork-guide.md)
owns the file mapping, backup, installation, restart, troubleshooting, and
per-game record. Verified artwork is stored under
[`steam/artworks/`](../steam/artworks/).

## Approval and prerequisites

Inspecting an existing shortcut and artwork is read-only. Adding or changing a
shortcut, replacing artwork, closing software, or restarting Steam requires
the owner's approval. Confirm the intended display name, exact executable,
Steam user, and App ID before changing files. Keep a timestamped backup and a
working path back to Gaming Mode.

## Standard workflow

1. Add or inspect the shortcut in Desktop Mode.
2. Confirm its App ID against both its name and exact executable path.
3. Back up existing Steam grid files, then install all four artwork formats.
4. Close the game, launcher, Proton, and Wine processes before restarting Steam.
5. Verify the wide cover, portrait cover, selected-game hero, and title logo in Gaming Mode.

Do not guess an App ID, force-close running software without approval, or
replace artwork without a timestamped backup. If no trusted method on the
current Steam build exposes the App ID, stop and record the gap rather than
using an unverified calculation.

## WowUp (CurseForge) for WoW Forever

The stable launcher is `~/Applications/WowUp-CurseForge`; AppImage files live
in `~/Applications/`. Its wrapper selects the newest `WowUp-CF-*.AppImage`,
clears `LD_PRELOAD`, and runs it with `--no-sandbox`. Use the wrapper rather
than adding a versioned AppImage directly to Steam. Keep Steam Overlay disabled
for this shortcut.

WoW Forever add-ons are under:

```text
~/.local/share/Steam/steamapps/compatdata/3104267125/pfx/drive_c/
Program Files (x86)/World of Warcraft/_forever_/Interface/AddOns
```

Back up add-ons and configuration before changing the prefix or reinstalling
the launcher.

## Verification and recovery

Use the detailed guide to correct format, title, transparency, or stale-cache
problems. Restore the timestamped artwork backup if the new files cannot be
verified. Record the App ID, SteamOS build, all four observed formats, and the
Gaming Mode result according to the [verification standard](verification.md).
