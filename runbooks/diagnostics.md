# Diagnostics

## Purpose

Use this runbook to collect safe information for a support ticket or resolve
common remote-access failures.

## Safe collection

On the Deck, collect the following and remove sensitive details before sharing:

```bash
systemctl is-active sshd
ip -br addr
whoami
uname -a
```

For recent SSH-service messages:

```bash
sudo journalctl -u sshd --since "30 minutes ago"
```

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `Connection refused` | Start SSH with `sudo systemctl enable --now sshd`. |
| Timeout or `No route to host` | Confirm both devices use the same local network and the Deck still uses `192.168.1.67`. |
| `Permission denied` | Confirm username `deck`; verify the password or authorized public key. |
| SSH works but `sudo -n` fails | Refresh authorization with `sudo -v` if shared authorization is configured. |
| Connection drops | Keep the Deck awake and connected to power during support work. |
| Access fails after an update | Recheck SSH and intentional custom configuration. |

Stop if the target identity, authorization, consequences, or recovery path is
unclear. Do not bypass a failed verification.
