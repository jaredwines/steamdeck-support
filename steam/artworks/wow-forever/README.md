# WoW Forever artwork backup

This folder contains Steam artwork for WoW Forever:

- `wide-cover.png` — wide library cover
- `portrait-cover.png` — portrait cover
- `hero-background.png` — title-free selected-game hero
- `title-logo.png` — transparent title logo

Install and verify these files with the
[Non-Steam Game & Artwork Setup Guide](../../add-non-steam-game-and-artwork-guide.md).
Keep updates limited to intended artwork; do not add credentials or sensitive
diagnostics.

## Evidence and provenance

| Item | Record |
| --- | --- |
| Source or creation method | Owner-supplied 1200x675 WoW Forever map-and-logo image adapted into four format-specific assets with OpenAI's built-in image-generation tool on 2026-10-28; exact Steam formats were resized locally with FFmpeg |
| Redistribution status | Source image supplied by the owner, who explicitly directed publication to the SS Git repository on 2026-10-28; redistribution rights were not independently assessed |
| Repository format and visual validation | Passed 2026-10-28: wide 920x430 RGB, portrait 600x900 RGB, hero 1920x620 RGB, and logo 1200x300 RGBA with transparency |
| SteamOS build | 3.9.5 / 20261023.100 |
| Wide, portrait, hero, logo, and Gaming Mode verification | Replacement repository files passed format validation and matched the installed files byte for byte on 2026-10-28. The portrait cover, title-free hero, and wide transparent logo were visually verified in Steam's gamepad UI. The wide cover was visually reviewed before installation; its gamepad recent-shelf placement was not exercised because the shortcut has no launch history. |

