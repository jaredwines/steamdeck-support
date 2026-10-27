# Agent Instructions

## Project context

- These instructions apply to this directory and all files beneath it.
- The canonical project root is `/home/deck/steamdeck-support`.
- Do not use the retired path `/home/deck/Documents/codex-steamdeck-support`.
- This project supports a Steam Deck running SteamOS.
- Read `main-support.md` before performing support work.
- The expected SSH target is `deck@192.168.1.67`; treat it as expected, not guaranteed.
- Keep detailed support procedures in `main-support.md`; do not duplicate them here.

## Required workflow

- Documentation-only requests authorize file edits, not changes to the Steam Deck.
- For system work, inspect first, explain findings, make the smallest necessary change, and run only the requested Deck commands. Read-only verification is allowed.
- Verify the result before declaring the task complete.

## Safety and credentials

- Get explicit approval before using `sudo` or making destructive, security-sensitive, system-wide, or difficult-to-reverse changes.
- Never assume passwordless `sudo` access.
- Never request, display, store, or log passwords or private SSH keys.
- Public SSH keys may be handled when required.
- Remove sensitive information from diagnostic output before sharing it.

## SteamOS safeguards

- Prefer user-level, reversible changes.
- Preserve Gaming Mode and normal Steam functionality.
- Do not disable SteamOS read-only protection unless explicitly requested and supported by a recovery plan.
- Consider whether a SteamOS update could overwrite a proposed change.

## Stop conditions

- Stop and report when the system conflicts with `main-support.md`, or when the target, authorization, consequences, or recovery path is unclear.
- Do not force a documented procedure when verification fails.

## Verification and handoff

- Report commands run, files changed, checks performed, and unresolved risks.
- After significant system work, confirm that Gaming Mode operates normally.
- Update `main-support.md` when a verified support procedure changes.
- Keep this file concise and free of secrets and duplicated tutorials.
