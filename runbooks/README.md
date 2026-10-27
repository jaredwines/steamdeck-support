# Support runbooks

This folder holds the authoritative, task-specific procedures for Steam Deck
support. Start with the [runbook index](index.md), then use only the runbook
that matches the task.

When the cause is unknown, use [Symptom triage](triage.md). The
[Support coverage matrix](coverage-matrix.md), [Scenario catalog](scenario-catalog.md),
and [Compatibility status](compatibility-status.md) track breadth, acceptance,
and evidence without replacing the owning procedures. The
[SS readiness scorecard](readiness-scorecard.md) prevents implemented changes
from being mistaken for completed practical verification.

Add a runbook update only after work is verified and reusable. Keep commands,
approval requirements, recovery steps, and verification results accurate; do
not record credentials or sensitive diagnostics.

Every new or materially changed procedure must follow the
[verification standard](verification.md): state prerequisites and approval,
include expected results and recovery, record compatibility evidence, and pass
the repository validation check.

Use the [support-session record template](support-session-record-template.md)
for private working notes. Do not commit a completed record; transfer only
sanitized, reusable findings into the runbook that owns the topic.
