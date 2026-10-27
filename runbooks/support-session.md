# Support session

## Purpose

Use this runbook for every support change, from planning through documentation
and handoff.

## Before making changes

1. Explain the intended change and obtain the owner's approval.
2. Record the commands that will be run.
3. Back up configuration files before editing them.
4. Prefer reversible user-level changes.
5. Do not disable SteamOS read-only protection unless explicitly required with
   a recovery plan.

## Verify and hand off

After significant changes, reboot only when appropriate, confirm Gaming Mode
works normally, and record the final result. Report commands run, files
changed, checks performed, unresolved risks, and recovery information.

## Update this documentation

After verified work produces reusable knowledge, update the SS (Steam Deck
Support): this repository and its documentation. Update the runbook that owns
the topic, and record only what is needed to repeat the work safely:

1. What changed and why.
2. Verified commands, paths, and expected results.
3. Required approval, safety constraints, recovery steps, and SteamOS-update risks.
4. Verification performed, including Gaming Mode after significant changes.
5. Remaining limitations or unresolved risks.

Do not document unverified observations, transient session details, passwords,
private keys, tokens, host-key material, or sensitive diagnostic output. Before
handoff, review the documentation diff for accuracy and scope, confirm commands
and Markdown links are valid, exclude unrelated changes, then commit and push
the documentation update. The update is complete only after the push succeeds,
unless the owner directs otherwise or a documented blocker prevents it.
