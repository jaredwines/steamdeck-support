# Diagnostics

## Purpose

Use this runbook to collect safe information for a support ticket or resolve
common remote-access failures.

## Quick path

Choose the smallest relevant read-only collector profile, preview it, run it
locally, and sanitize and manually review any output before sharing. Diagnostics
do not authorize a repair.

## Approval and sanitization

The basic commands below are read-only. `sudo journalctl` requires explicit
approval because it uses elevated access and its output can contain sensitive
system details. Before sharing output, remove local addresses, hostnames,
device identifiers, usernames other than `deck`, account data, tokens, and
unrelated log lines.

## Safe collection

For a topic-specific, read-only collection with a local privacy warning, use:

```bash
bash scripts/collect-diagnostics.sh --list
bash scripts/collect-diagnostics.sh --dry-run <profile>
bash scripts/collect-diagnostics.sh <profile>
bash scripts/collect-diagnostics.sh <profile> | python3 -B scripts/summarize-diagnostics.py
```

The collector uploads nothing. Its output can still contain sensitive values.
Review it manually; `scripts/sanitize-diagnostics.py` removes common patterns
but cannot guarantee that arbitrary diagnostic text is safe to share.

On the Deck, collect the following and remove sensitive details before sharing:

```bash
systemctl is-active sshd
ip -br addr
whoami
uname -a
cat /etc/os-release
df -h /
systemctl --failed --no-pager
systemctl --user --failed --no-pager
```

For recent SSH-service messages:

```bash
sudo journalctl -u sshd --since "30 minutes ago"
```

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `Connection refused` | With owner approval, follow [Remote access](remote-access.md) to enable and verify SSH. |
| Timeout or `No route to host` | Confirm both devices use the same local network and the Deck still uses `192.168.1.67`. |
| `Permission denied` | Confirm username `deck`; verify the password or authorized public key. |
| SSH works but `sudo -n` fails | Refresh authorization with `sudo -v` if shared authorization is configured. |
| Connection drops | Keep the Deck awake and connected to power during support work. |
| Access fails after an update | Recheck SSH and intentional custom configuration. |

Stop if the target identity, authorization, consequences, or recovery path is
unclear. Do not bypass a failed verification.

## Verification record

Record the SteamOS build, symptom, commands run, sanitized result, and whether
the issue was resolved. Diagnostics alone do not authorize a configuration
change. Follow the [verification standard](verification.md) before turning a
finding into reusable guidance.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | 3.9.5 / 20261023.100 | Ran all eight read-only collector profiles through an existing strict-host-key SSH connection | Passed: 26 command sections completed with no unavailable-command marker; no repair was attempted |
