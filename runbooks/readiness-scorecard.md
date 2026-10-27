# SS readiness scorecard

## Purpose

Use this scorecard to distinguish implemented improvements from evidence that
still requires a real support case, owner approval, private backup destination,
physical media, or independent review. Passing repository checks alone cannot
produce a 10/10 practical-usefulness claim.

## Current gate status

| Gate | Target | Current result | Status |
| --- | --- | --- | --- |
| Symptom routing | 20 representative scenarios have one clear owning route | 20 ordered routes validated automatically | Passed |
| Runbook structure | Every operational runbook states purpose, approval, verification, and evidence where applicable | 19 operational runbooks validated | Passed |
| Local quality gate | Links, scripts, artwork, secrets, whitespace, and repository invariants pass | `scripts/validate-repository.sh` passes | Passed |
| Safe diagnostics | Eight topic profiles are read-only, dry-runnable, private by default, and available on the Deck | Eight profiles and 26 command sections completed on SteamOS 3.9.5 | Passed for collection |
| High-frequency repairs | At least one complete verified repair in every high-frequency category | Procedures written; repair cases not manufactured | Pending real cases |
| SSH lifecycle | Setup, authentication, revocation, and shutdown verified | Existing authentication and strict host checking verified | Partial |
| Non-Steam artwork | Files and all four visual placements verified | Files verified; visual Gaming Mode check pending | Partial |
| Backup acceptance | Encrypted off-device copy, remount verification, and representative restore pass | No destination or copying approval provided | Approval-gated |
| Recovery-media rehearsal | Official image written, validated, booted, and normal Gaming Mode restored | No identified expendable USB or erase/boot approval | Approval-gated |
| Independent acceptance | Fresh reviewer scores at least 190/200 with no critical failure | Independent tabletop re-review scored 200/200 with no critical failure | Passed |

## Release rule

Do not call SS 10/10 while an approval-gated, partial, or pending gate remains.
The repository implementation can be release-ready while practical evidence is
still incomplete. Close a gate only with the owning runbook's sanitized evidence
and update the coverage matrix and compatibility dashboard in the same change.

## Next safe actions

1. Use the focused runbooks during genuine support cases and record complete
   verification rather than manufacturing failures.
2. With the owner's explicit approval and a selected encrypted destination,
   perform the backup acceptance test.
3. With an identified expendable USB and explicit erase/boot approval, perform
   the non-destructive recovery-media rehearsal.
4. Complete the non-Steam artwork visual check in Gaming Mode without changing
   files unless a defect is found and separately approved.

## Verification

Run `bash scripts/validate-repository.sh`, compare every status with the owning
runbook, and preserve `Pending` or `Partial` when evidence is incomplete.
