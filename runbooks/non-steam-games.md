# Non-Steam games, launchers, and artwork

## Purpose

Use this runbook to add or verify a non-Steam game or launcher. For the full
repeatable procedure, use the [Non-Steam Game & Artwork Setup Guide](../steam/add-non-steam-game-and-artwork-guide.md). Verified artwork backups are in
[`steam/artworks/battle.net`](../steam/artworks/battle.net/) and
[`steam/artworks/wowup-curseforge`](../steam/artworks/wowup-curseforge/).

## Standard workflow

1. Add or inspect the shortcut in Desktop Mode and record its App ID.
2. Back up existing Steam grid files before replacing them.
3. Install the four format-specific artwork files.
4. Confirm the game and launcher are closed before restarting Steam.
5. Verify the wide cover, portrait cover, selected-game hero, and title logo in Gaming Mode.

## Verified artwork mapping

| File | Size | Purpose | Title rule |
| --- | ---: | --- | --- |
| `<appid>.png` | 920 x 430 | Wide library cover | Bake the title into the image. |
| `<appid>p.png` | 600 x 900 | Portrait cover | Bake the title into the image. |
| `<appid>_hero.png` | 1920 x 620 | Selected-game hero background | Do not bake in a title. |
| `<appid>_logo.png` | 1200 x 300 | Hero title logo | Transparent PNG; title only. |

The plain `.png` is the wide cover and `p.png` is the portrait cover. Steam
overlays the transparent logo on the hero; a title in both appears twice.

## Restart Steam safely

Confirm no game, launcher, Proton, or Wine process is active. Then restart the
Steam user service:

```bash
systemctl --user restart app-steam@autostart.service
pgrep -u deck -x steam >/dev/null && echo "STEAM_RUNNING"
```

Do not force-close Steam while software is running unless the owner explicitly
approves interrupting it.

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

## Recovery

| Symptom | Recovery |
| --- | --- |
| Portrait and wide cards are reversed | Swap `<appid>.png` and `<appid>p.png`. |
| Title is clipped | Use a format-specific design and move it inside the safe area. |
| Hero has a duplicate title | Remove the title from `_hero.png`; retain `_logo.png`. |
| Dark title panel is unwanted | Re-render without the panel; retain a thin text outline if needed. |
| Steam shows old artwork | Restart Steam; verify App ID, Steam user ID, and grid folder. |
| Logo has a black box | Export it as transparent RGBA PNG artwork. |
