# Flatpak and Discover applications

## Purpose and status

Use this runbook when a Discover or Flatpak application will not launch, update,
or behave normally. It avoids changing the wrong installation. No repair in
this runbook has yet been verified on this Deck.

## Quick path

Identify the exact application ID and user/system installation, reproduce one
sanitized error, classify it, and apply only an approved targeted action to that
installation.

## Approval and prerequisites

Listing applications and history is read-only. Obtain approval before updating,
repairing, reinstalling, changing permissions, or deleting application data.
Record the exact application ID and whether it is installed for the user or
system. Protect application data before repair or reinstall work.

## Read-only baseline

```bash
flatpak list --app --columns=application,origin,version,installation
flatpak history --user --columns=time,change,application,installation
flatpak history --system --columns=time,change,application,installation
flatpak remotes --show-details
```

Keep unrelated application history and remote details private. An unavailable
optional command is a finding, not a reason to install another tool.

## Isolate and repair

1. Confirm whether one application or all Flatpaks are affected.
2. With the graphical instance closed, launch the exact application from
   Konsole and preserve only the relevant, sanitized error:

   ```bash
   flatpak info --user <application-id>
   flatpak info --system <application-id>
   flatpak run <application-id>
   flatpak override --show <application-id>
   ```

   Only one `info` command should find the intended installation. The override
   command is read-only; its output can reveal filesystem paths and must stay
   local unless sanitized.
3. Classify the result before changing anything:

   | Finding | Next step |
   | --- | --- |
   | Application ID or installation not found | Recheck the baseline; do not reinstall by display name |
   | Network or remote error during update | Confirm general connectivity and the recorded remote; do not repair local data |
   | Missing runtime or ref named in the error | Compare `flatpak list --runtime` with `flatpak info`; use the targeted approved update below |
   | Permission or filesystem path error | Record overrides and ownership context; do not reset permissions or use `sudo flatpak` |
   | Application starts but crashes with its own data | Protect `~/.var/app/<application-id>` before considering app-specific recovery |
   | Multiple applications fail | Stop treating it as one-app data damage; preserve sanitized common errors before repair |

4. With approval, update only the installation shown by the baseline:

   ```bash
   flatpak update --user <application-id>
   flatpak update --system <application-id>
   ```

   Run one command, not both.
5. If installed data appears inconsistent, review `flatpak repair --help`.
   `flatpak repair --user` changes data and requires separate approval.

Do not use `sudo flatpak`, reset permissions, remove runtimes, delete
`~/.var/app`, or reinstall as a generic first response.

## Verification and recovery

Launch the exact application twice, exercise the affected function, and confirm
another known-good Flatpak still starts. Preserve app data and stop if repair
would require deletion or an unexplained system-wide change. Confirm Gaming
Mode if the application is exposed there.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | 3.9.5 / 20261023.100 | Existing application identification, installation-specific `info`, runtime listing, and override inspection | Passed read-only checks; application launch failure, update, and repair remain unverified |
