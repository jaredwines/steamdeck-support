# Steam Deck Support

This repository stores verified, reusable guidance for supporting a Steam Deck
running SteamOS, plus backed-up Steam artwork. Start with the
[runbook index](runbooks/index.md) before support work.

**Steam Deck Support (SS)** is the name of this repository and its canonical
root folder, `/home/deck/steamdeck-support`. Use the full name on first
mention; use **SS** afterward only when the abbreviation improves clarity.

## Repository map

- [runbooks/](runbooks/README.md) — operational procedures and safety rules.
- [steam/](steam/README.md) — non-Steam game and artwork guidance.
- [codex/](codex/README.md) — instructions used by Codex in this repository.

## Supported scope

SS currently covers remote access, temporary sudo authorization, GitHub SSH
access, safe diagnostics, support-session handoff, and non-Steam
game/launcher artwork. “Verified” means a procedure produced the documented
result when it was used; it does not mean that every procedure is valid for
every SteamOS release or network.

Before using a runbook, confirm its prerequisites and record the current
SteamOS build and relevant result as described in the
[verification standard](runbooks/verification.md). A missing topic is a
coverage gap, not permission to improvise a risky procedure.

## Validate the repository

Run the local quality checks after documentation or artwork changes:

```bash
bash scripts/validate-repository.sh
```

The check verifies local Markdown links, the exact `AGENTS.md` backup, required
files, shell syntax, and the dimensions and alpha channel of backed-up artwork.
The same check runs automatically for pushes and pull requests.

## Update this repository

Add only verified, reusable knowledge or intended artwork. Never commit
passwords, private keys, tokens, host-key material, or sensitive diagnostics.

From the repository root, review and publish an intended update:

```bash
git status
git add <intended-files>
git diff --cached
git commit -m "docs: describe the update"
git push
```

Stage only the files you intend to publish. Read
[Support session](runbooks/support-session.md) for the documentation and
handoff requirements.
