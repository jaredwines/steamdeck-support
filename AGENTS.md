# Agent Instructions

## Project context

- These instructions apply to this directory and all files beneath it.
- This project supports a Steam Deck running SteamOS.
- Read `main-support.md` before performing support work.
- The expected SSH target is `deck@192.168.1.67`.
- Treat the address as expected, not guaranteed, when diagnosing connectivity.
- Keep detailed support procedures in `main-support.md`; do not duplicate them here.

## Required workflow

- Documentation-only requests authorize file edits only, not changes to the Steam Deck.
- Run commands against the Deck only when the task calls for system work; relevant read-only verification is allowed.
- Inspect first, explain the findings, and make the smallest necessary change.
- Verify the result before declaring the task complete.

## Safety and credentials

- Get approval before using `sudo` or making destructive, security-sensitive, system-wide, or difficult-to-reverse changes.
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

- Stop and report when the observed system conflicts with `main-support.md`.
- Stop when the target device, authorization, consequences, or recovery path is unclear.
- Do not force a documented procedure when verification fails.

## Verification and handoff

- Report commands run, files changed, checks performed, and unresolved risks.
- After significant system work, confirm that Gaming Mode operates normally.
- Update `main-support.md` when a verified support procedure changes.
- Keep this file concise and free of secrets and duplicated tutorials.
