# Steam Deck Support

This repository stores verified, reusable guidance for supporting a Steam Deck
running SteamOS, plus backed-up Steam artwork. Start with the
[runbook index](runbooks/index.md) before support work.

## Repository map

- [runbooks/](runbooks/README.md) — operational procedures and safety rules.
- [steam/](steam/README.md) — non-Steam game and artwork guidance.
- [codex/](codex/README.md) — instructions used by Codex in this repository.

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
