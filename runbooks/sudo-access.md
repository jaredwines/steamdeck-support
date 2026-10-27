# Sudo access

## Purpose

Use this runbook when a support task needs `sudo`, or when the owner explicitly
requests temporary sudo authorization to be shared across SSH sessions.

## Quick path

Confirm the exact approved command and expected account, authenticate only at a
trusted prompt, avoid persistent policy changes unless specifically required,
and clear temporary authorization with `sudo -k` at handoff.

## Approval and prerequisites

Every command in this runbook that invokes `sudo` requires the owner's
explicit approval. Verify that the session belongs to the expected `deck`
account before continuing. Shared authorization increases what another active
`deck` session can do during the normal sudo timeout; use it only when that
specific behavior is needed.

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

## Remove shared authorization

Removal is a system-wide change and requires fresh explicit approval. First
verify that the file contains only the rule installed by this runbook:

```bash
sudo test "$(sudo cat /etc/sudoers.d/90-deck-global-sudo-timestamp)" = \
  'Defaults:deck timestamp_type=global' && echo "EXPECTED_RULE" || echo "STOP: unexpected content"
```

Stop unless the result is `EXPECTED_RULE`. Preserve a recoverable copy, remove
the active rule, validate sudoers, and clear the timestamp:

```bash
backup="$HOME/90-deck-global-sudo-timestamp.backup-$(date +%Y%m%d-%H%M%S)"
sudo cp -p /etc/sudoers.d/90-deck-global-sudo-timestamp "$backup"
sudo chown deck:deck "$backup"
sudo chmod 600 "$backup"
sudo rm /etc/sudoers.d/90-deck-global-sudo-timestamp
sudo visudo -c
sudo -k
```

Verify from a second session that `sudo -n true` reports authentication is
required. Keep the backup until ordinary sudo behavior and Gaming Mode have
been confirmed. If validation fails, restore the backup only with approval:

```bash
sudo install -o root -g root -m 440 "$backup" /etc/sudoers.d/90-deck-global-sudo-timestamp
sudo visudo -c
```

## When authorization expires

If the check reports `SUDO_NOT_AVAILABLE`, in a trusted `deck` session run:

```bash
sudo -v
```

Then repeat the noninteractive check. If `sudo -v` is denied, stop and check
the local `deck` sudo policy; do not attempt to bypass it.

## Verification record

Record the SteamOS build, whether standard or shared authorization was used,
the result of `sudo -l`, whether `sudo -k` was run, and whether any persistent
rule remains. Follow the [verification standard](verification.md).

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Standard and shared authorization procedures reviewed | Ready for use; no sudo command was run during this review |
