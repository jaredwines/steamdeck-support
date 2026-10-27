# Battle.net artwork backup

This folder contains verified Steam artwork for Battle.net:

- `wide-cover.png` — wide library cover
- `portrait-cover.png` — portrait cover
- `hero-background.png` — title-free selected-game hero
- `title-logo.png` — transparent title logo

Install and verify these files with the
[Non-Steam Game & Artwork Setup Guide](../../add-non-steam-game-and-artwork-guide.md).
Keep updates limited to verified artwork; do not add credentials or sensitive
diagnostics.

Before publishing an intended update, run `git status`, stage only the
intended files, review `git diff --cached`, then commit and push from the
repository root. See the [artwork overview](../README.md) for more context.
