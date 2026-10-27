# Verification standard

## Purpose

Use this standard to decide whether a support procedure is safe to run and
whether its result is strong enough to document as verified, reusable SS
guidance.

## Before using a runbook

Record enough context to detect version-dependent behavior without collecting
account data or secrets:

```bash
cat /etc/os-release
uname -r
```

Record the SteamOS version/build, kernel version, connection type, applicable
runbook, and intended outcome. Confirm the runbook's prerequisites, approval
boundary, verification, and recovery path. Stop if any of those are unclear.

## Evidence required after a change

A procedure is verified only when all of the following are true:

1. The intended command or change completed without an unexplained error.
2. The runbook's expected result was observed.
3. A functional check confirmed the affected feature works.
4. Recovery remains available or was tested when practical.
5. Gaming Mode works normally after significant system work.
6. Commands, changed files, deviations, and unresolved risks were recorded.

Use this compact record in the support-session notes:

```text
Date:
SteamOS version/build:
Kernel:
Runbook and section:
Commands run:
Files changed:
Expected result:
Observed result:
Functional check:
Gaming Mode check (if significant):
Recovery available/tested:
Deviations and unresolved risks:
```

Do not commit a session record when it contains usernames beyond `deck`, local
addresses, device identifiers, account information, logs, or other sensitive
details. Transfer only reusable, sanitized findings into the owning runbook.

## Documentation review

When a procedure is newly verified on a SteamOS release, add a short
compatibility note to that runbook containing the review date, SteamOS
version/build, and result. Do not claim compatibility with releases that were
not tested. Revalidate after a major SteamOS update, an upstream behavior
change, or a failure that contradicts the documented result.

## Repository quality gate

From the repository root, run:

```bash
bash scripts/validate-repository.sh
git diff --check
```

Both commands must pass before publishing. Then review the complete diff and
confirm it contains only intended, reusable, sanitized material.
