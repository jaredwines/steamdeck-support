# Verified Steam artwork backups

This folder stores per-game or per-launcher artwork backups. Each collection
should contain the four images described in the
[setup guide](../add-non-steam-game-and-artwork-guide.md): a wide cover,
portrait cover, hero background, and transparent title logo.

Use a dedicated subfolder for each title. Keep the hero title-free and the logo
transparent. Do not store secrets or unrelated files with the artwork.

Before publishing an intended update, run `git status`, stage only the
intended files, review `git diff --cached`, then commit and push from the
repository root. See the [repository README](../../README.md) for the full
workflow.
