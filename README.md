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
- [scripts/validate-repository.sh](scripts/validate-repository.sh) — the local
  quality gate; `scripts/` also contains the read-only non-Steam shortcut
  inspector and its supporting validators.
- [runbooks/triage.md](runbooks/triage.md) — symptom-first routing when the
  cause is not yet known.
- [runbooks/coverage-matrix.md](runbooks/coverage-matrix.md) — diagnostic,
  repair, recovery, and evidence coverage at a glance.
- [runbooks/readiness-scorecard.md](runbooks/readiness-scorecard.md) — measurable
  10/10 release gates and their current evidence status.
- [scripts/collect-diagnostics.sh](scripts/collect-diagnostics.sh) — read-only,
  topic-specific collection with dry-run support; sanitize and manually review
  its local output before sharing it. The companion sanitizer redacts common
  patterns and the summary tool reports coverage without collected values.

## Supported scope

SS currently covers remote access, temporary sudo authorization, GitHub SSH
access, full-system restore planning, safe diagnostics, common SteamOS issue
triage, support-session handoff, and non-Steam game/launcher artwork.
“Verified” means a procedure produced the documented result when it was used;
documentation review alone is labeled separately and does not establish
on-device compatibility.

Before using a runbook, confirm its prerequisites and record the current
SteamOS build and relevant result as described in the
[verification standard](runbooks/verification.md). A missing topic is a
coverage gap, not permission to improvise a risky procedure.

## Validate the repository

Run the local quality checks after documentation or artwork changes:

```bash
bash scripts/validate-repository.sh
```

The check verifies every required repository component, local Markdown files
and heading links, required runbook structure, common secret patterns, the
exact `AGENTS.md` backup, shell syntax, the non-Steam shortcut inspector's
self-test, and PNG integrity, inventory, dimensions, color format, and real
logo transparency. It also checks working-tree and staged whitespace. CI checks
committed whitespace and external links on pushes and pull requests.

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
