# Support runbooks

This folder holds the authoritative, task-specific procedures for Steam Deck
support. Start with the [runbook index](index.md), then use only the runbook
that matches the task.

Add a runbook update only after work is verified and reusable. Keep commands,
approval requirements, recovery steps, and verification results accurate; do
not record credentials or sensitive diagnostics.

Before publishing an intended update, run `git status`, stage only the
intended files, review `git diff --cached`, then commit and push from the
repository root. See the [repository README](../README.md) for the full
workflow.
