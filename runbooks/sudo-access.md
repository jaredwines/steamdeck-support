# Sudo access

## Purpose

Use this runbook when a support task needs `sudo`, or when the owner explicitly
requests temporary sudo authorization to be shared across SSH sessions.

## Standard temporary authorization

Never assume passwordless sudo. In a trusted `deck` session, run:

```bash
sudo -v
```

Enter the account password only at that prompt. When work is complete, clear
the temporary authorization:

```bash
sudo -k
```

## Optional shared authorization

Use this only with the owner's explicit approval. It does not make sudo
passwordless: `deck` must authenticate first and the normal timeout applies.

First confirm the dedicated configuration does not already exist:

```bash
sudo test ! -e /etc/sudoers.d/90-deck-global-sudo-timestamp && echo "ready to create" || echo "STOP: file already exists"
```

Only when it reports `ready to create`, install and validate the narrow rule:

```bash
printf '%s\n' 'Defaults:deck timestamp_type=global' | sudo tee /etc/sudoers.d/90-deck-global-sudo-timestamp >/dev/null
sudo chmod 440 /etc/sudoers.d/90-deck-global-sudo-timestamp
sudo visudo -c
sudo -l
```

`sudo -l` should list `timestamp_type=global` under matching defaults. Run
`sudo -v` in one `deck` session, then verify from another:

```bash
sudo -n true && echo "SUDO_OK" || echo "SUDO_NOT_AVAILABLE"
```

The configuration and authorized SSH keys persist through reboot; active sudo
authorization does not. Recheck the policy after major SteamOS updates.

## When authorization expires

If the check reports `SUDO_NOT_AVAILABLE`, in a trusted `deck` session run:

```bash
sudo -v
```

Then repeat the noninteractive check. If `sudo -v` is denied, stop and check
the local `deck` sudo policy; do not attempt to bypass it.
