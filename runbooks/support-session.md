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

Use the [verification standard](verification.md) to record the SteamOS build,
expected result, recovery path, and sanitized evidence. A request to diagnose
does not by itself authorize a repair, and approval for one change does not
authorize additional system changes.

Copy the [support-session record template](support-session-record-template.md)
outside the repository for working notes. Keep the completed record private if
it contains device, network, account, or other identifying information.

## Verify and hand off

After significant changes, reboot only when appropriate, confirm Gaming Mode
works normally, and record the final result. Report commands run, files
changed, checks performed, unresolved risks, and recovery information.

Keep transient session notes outside the repository. Commit only sanitized,
reusable guidance; do not commit raw logs, device identifiers, local addresses,
account data, or credentials.

## Update this documentation

After verified work produces reusable knowledge, update the runbook that owns
the topic and its compatibility note. Include only the prerequisites, verified
commands, expected results, recovery, and unresolved risks needed to repeat the
work safely. Exclude unverified observations, session details, secrets, and
sensitive diagnostics.

Run the repository quality gate, review the intended diff, then commit and
push. The update is complete after the push succeeds unless the owner directs
otherwise or a documented blocker prevents it.
