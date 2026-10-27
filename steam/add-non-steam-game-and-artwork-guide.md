# Steam Deck Non-Steam Game & Artwork Setup Guide

Use this guide to add a game or launcher to Steam on a Steam Deck and give it
reliable custom artwork in Desktop Mode and Gaming Mode.

## Approval and prerequisites

- Obtain the owner's approval before adding or changing a shortcut, replacing
  artwork, closing software, or restarting Steam.
- Do not replace existing artwork before creating a timestamped backup.
- Close the game and its launcher before restarting Steam.
- Keep the hero background title-free. Steam displays the separate transparent
  logo over the hero; putting a title in both places causes duplicate names.
- Check the finished artwork in Gaming Mode before treating the setup as done.

## Information to collect

| Item | Example |
| --- | --- |
| Display name | `Battle.net` |
| Executable or launcher path | `/path/to/launcher.exe` |
| Steam shortcut App ID | `3104267125` |
| Steam user ID | `48955311` |
| Artwork folder | `~/.local/share/Steam/userdata/<steam-user-id>/config/grid/` |

## 1. Add the non-Steam game

1. Switch to **Desktop Mode** and open Steam.
2. Select **Add a Game** > **Add a Non-Steam Game**.
3. Choose the executable or add it manually, then set the display name.
4. Configure compatibility settings or launch options when the game needs
   Proton or a launcher-specific command.
5. Restart Steam once so it saves the shortcut information.
6. From SS, use the read-only shortcut inspector to list the IDs Steam stored:

   ```bash
   python3 /home/deck/steamdeck-support/scripts/list-non-steam-shortcuts.py \
     --match '<display-name>'
   ```

   The output can contain private executable paths; review it locally and do
   not paste it into a ticket. If `python3` or the shortcut file is unavailable,
   stop and use a trusted inspection method rather than installing an
   unreviewed tool.
7. Match both the display name and exact executable path, then record the
   corresponding stored App ID. Never calculate, guess, or reuse another
   shortcut's ID.

## 2. Create the four artwork files

Create a separate image for every Steam layout. Do not crop one image into all
formats without checking the title placement.

| Artwork | Size | Steam filename | Title rule |
| --- | ---: | --- | --- |
| Wide library cover | 920 x 430 | `<appid>.png` | Bake the title into the image. |
| Portrait cover | 600 x 900 | `<appid>p.png` | Bake the title into the image. |
| Hero background | 1920 x 620 | `<appid>_hero.png` | Do **not** bake in a title. |
| Transparent title logo | 1200 x 300 | `<appid>_logo.png` | Transparent background; title only. |

Important: for this Steam Deck setup, the plain `.png` file is the **wide**
cover and the `p.png` file is the **portrait** cover.

### Design checklist

- Keep title text inside a generous safe margin.
- Use strong contrast and a thin outline when the art is busy.
- Avoid large translucent title panels unless that appearance is intentional.
- Keep titles baked into portrait and wide artwork only.
- Make the logo background truly transparent (PNG with alpha), not black.
- Leave the hero background free of title text so Steam can use the logo once.

## 3. Back up existing Steam artwork

Replace `<steam-user-id>`, `<appid>`, and `<game-name>` before running:

```bash
grid="$HOME/.local/share/Steam/userdata/<steam-user-id>/config/grid"
backup="$grid/.backup-<game-name>-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup"

for suffix in .png p.png _hero.png _logo.png; do
  file="$grid/<appid>$suffix"
  [ -f "$file" ] && cp -p "$file" "$backup/"
done
```

Keep the reported backup folder until the new artwork has been verified in
Gaming Mode.

## 4. Install the artwork

Put the prepared files somewhere convenient, then copy them to Steam's grid
folder. Replace the placeholders:

```bash
grid="$HOME/.local/share/Steam/userdata/<steam-user-id>/config/grid"

test -d "$grid" && echo "READY" || echo "STOP: grid folder not found"
```

Continue only after the check reports `READY`:

```bash
grid="$HOME/.local/share/Steam/userdata/<steam-user-id>/config/grid"

cp -f wide.png     "$grid/<appid>.png"
cp -f portrait.png "$grid/<appid>p.png"
cp -f hero.png     "$grid/<appid>_hero.png"
cp -f logo.png     "$grid/<appid>_logo.png"
```

Confirm that Steam received the intended formats:

```bash
file "$grid/<appid>.png" \
     "$grid/<appid>p.png" \
     "$grid/<appid>_hero.png" \
     "$grid/<appid>_logo.png"
```

Expected sizes are 920x430, 600x900, 1920x620, and 1200x300 respectively.
The logo should report an RGBA PNG, indicating a transparent alpha channel.

## 5. Reload Steam and verify

Before restarting Steam, confirm that the game and launcher are closed.

```bash
systemctl --user restart app-steam@autostart.service
```

In Gaming Mode, verify all four views:

- Wide library/shelf card: correct composition and one readable baked title.
- Portrait card: correct composition and one readable baked title.
- Selected-game hero: correct background with no baked title.
- Hero title: one readable transparent Steam logo, with no duplicate title.

If any view is wrong and cannot be corrected immediately, restore the files
from the timestamped backup, restart Steam safely, and verify the original
artwork is visible again.

## Troubleshooting

| Problem | Likely cause and fix |
| --- | --- |
| Wide and portrait art appear backward | Swap `<appid>.png` and `<appid>p.png`. |
| Title is clipped | Create a format-specific layout and move the title farther into its safe area. |
| Title appears twice on the hero | Remove the baked title from `<appid>_hero.png`; retain `<appid>_logo.png`. |
| A dark rectangle appears behind the title | Re-render without a translucent title panel; a thin outline is usually enough. |
| Steam still shows old art | Restart Steam and recheck the App ID, Steam user ID, and grid folder. |
| Logo appears with a black box | Re-export `<appid>_logo.png` with a transparent RGBA background. |

## Per-game record

Copy this block for each new game:

```md
## Game: <name>

- Added to Steam: <date>
- Steam App ID: <appid>
- Steam user ID: <steam-user-id>
- Executable: `<path>`
- Artwork source folder: `<folder>`
- Artwork backup folder: `<folder>`
- Portrait cover verified: Yes / No
- Wide cover verified: Yes / No
- Hero background verified: Yes / No
- Transparent logo verified: Yes / No
- Gaming Mode verified: Yes / No
- Notes:
```

Also record the SteamOS version/build and the date of verification. Use the
[SS verification standard](../runbooks/verification.md) for the complete
evidence and sanitization requirements.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | 3.9.5 / 20261023.100 | Read-only shortcut inspection and installed-file comparison | Inspector matched the stored Battle.net and WowUp shortcuts; all eight installed artwork files matched SS byte for byte; Steam restart and visual Gaming Mode verification remain pending |
