# Remote access

## Purpose

Use this runbook to prepare, verify, or end SSH access to the Steam Deck.

## Quick path

Inspect the existing service, listener, address, and intended identity before
changing anything. Verify the host fingerprint locally, preserve a working
session during approved changes, and disable temporary access when finished.

## Approval and prerequisites

Inspecting network and SSH status is read-only. Setting a password, enabling or
disabling SSH, authorizing or revoking a key, and changing SSH configuration
require the owner's explicit approval. Perform setup in Desktop Mode with local
access available so a failed remote change cannot lock out the owner.

## Diagnose an existing connection

Before enabling or changing anything, use local access on the Deck to inspect
the service, listener, address, and route:

```bash
systemctl is-active sshd
systemctl is-enabled sshd
ss -ltn 'sport = :22'
ip -br addr
ip route
```

An inactive service or missing listener explains `Connection refused`; an
active listener with a timeout points instead to the address, route, network,
sleep state, or filtering. Review addresses locally and do not copy them into
SS. Enabling the service remains a separate approved change.

For an existing key that reports `Permission denied`, keep verbose output local
and force the intended identity:

```bash
ssh -vv -o IdentitiesOnly=yes -i <private-key-path> deck@192.168.1.67
ssh-keygen -lf <public-key-path>
```

With local Deck access, compare only public-key fingerprints and permissions:

```bash
stat -c '%a %U:%G %n' ~/.ssh ~/.ssh/authorized_keys
ssh-keygen -lf ~/.ssh/authorized_keys
```

Expected ownership is `deck:deck`; expected modes are `700` for `~/.ssh` and
`600` for `authorized_keys`. Do not display that file or change permissions
without approval. If the intended fingerprint is absent, follow the dedicated
key setup below instead of repeatedly guessing identities. If it is present
and permissions are correct, preserve the sanitized relevant `ssh -vv` lines
and stop before changing server configuration.

## Prepare the Deck

In Desktop Mode, open Konsole. Set or update the `deck` password if necessary:

```bash
passwd
```

Enable SSH and confirm it is active:

```bash
sudo systemctl enable --now sshd
systemctl is-active sshd
```

Expected result: `active`.

## Verify the first connection

Connect from the support computer:

```bash
ssh deck@192.168.1.67
```

Before accepting a new host key, display the fingerprint locally on the Deck:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Accept the host key only if its SHA256 fingerprint matches the connection
prompt. After signing in, verify the account and operating system:

```bash
whoami
uname -a
cat /etc/os-release
```

`whoami` must return `deck`.

### Replace a legitimately changed host key

A changed key is a security stop, not an authentication problem. On the Deck,
display its current fingerprint locally:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

On the support computer, inspect the exact target's stored entries locally; do
not paste their key material into a record:

```bash
ssh-keygen -F 192.168.1.67 -f "$HOME/.ssh/known_hosts"
```

Proceed only when local access proves this is the intended Deck and its current
fingerprint explains the change, such as after a verified re-image. With
approval, back up the file and remove entries for only that exact address:

```bash
backup="$HOME/.ssh/known_hosts.backup-$(date +%Y%m%d-%H%M%S)"
cp -p "$HOME/.ssh/known_hosts" "$backup"
ssh-keygen -R 192.168.1.67 -f "$HOME/.ssh/known_hosts"
```

Reconnect and accept only the fingerprint already verified on the Deck. Open a
second connection with strict checking and confirm `whoami` returns `deck`. If
the fingerprint differs or the connection fails unexpectedly, stop; restore
the backup only after determining that doing so represents the intended host.
Keep the backup until access and Gaming Mode are confirmed normal.

### When the support computer rejects its SSH configuration

If the local SSH client stops before connecting with `Bad owner or permissions`
for a file under `/etc/ssh/ssh_config.d`, do not weaken permissions or edit that
system file without a separate diagnosis and approval. For a read-only support
connection, bypass the rejected client configuration while retaining the
dedicated identity and strict existing host-key check:

```bash
ssh -F /dev/null \
  -i <private-key-path> \
  -o IdentitiesOnly=yes \
  -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile="$HOME/.ssh/known_hosts" \
  deck@192.168.1.67
```

This is valid only when the expected host key is already present and the
explicit identity and target are correct. It does not repair the rejected
system configuration. Stop if strict host checking or authentication fails.

## Verify the expected address

On the Deck, run:

```bash
ip -4 addr show wlan0
ip route
```

Confirm that `wlan0` has `192.168.1.67`. Prefer a router DHCP reservation. If
the Deck uses Ethernet, check the active Ethernet interface instead.

## Set up a dedicated SSH key

Add only public keys to the Deck; never copy or share a private key. Use a
dedicated key for recurring support access.

### Linux or macOS

```bash
ssh-keygen -t ed25519 -f ~/.ssh/steam_deck_support -C "steam-deck-support"
ssh-copy-id -i ~/.ssh/steam_deck_support.pub deck@192.168.1.67
ssh -i ~/.ssh/steam_deck_support deck@192.168.1.67
```

If `ssh-copy-id` is unavailable:

```bash
cat ~/.ssh/steam_deck_support.pub | ssh deck@192.168.1.67 'umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys'
```

### Windows PowerShell

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\steam_deck_support" -C "steam-deck-support"
Get-Content "$env:USERPROFILE\.ssh\steam_deck_support.pub" | ssh deck@192.168.1.67 'umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys'
ssh -i "$env:USERPROFILE\.ssh\steam_deck_support" deck@192.168.1.67
```

Do not disable password authentication until a separate key-authenticated
connection succeeds. Keep the original session open while testing.

### Persistent Codex access

Give a persistent Codex environment a dedicated SSH key, rather than sharing a
person's private key. Store the private key only in protected credential
storage; authorize its public key for `deck` with a clear comment such as
`codex-steamdeck`. Test an explicit identity path before relying on it. Revoke
that public-key line when the environment no longer needs access.

## Revoke a dedicated key

With explicit approval, keep one working session open and back up the current
authorization file before editing it:

```bash
backup="$HOME/.ssh/authorized_keys.backup-$(date +%Y%m%d-%H%M%S)"
cp -p ~/.ssh/authorized_keys "$backup"
chmod 600 "$backup"
ssh-keygen -lf ~/.ssh/authorized_keys
```

Match the fingerprint of the public key being revoked, then remove only that
exact line from `~/.ssh/authorized_keys` with a local editor. Do not paste the
file into a support ticket. Restore mode `600`, then confirm a new connection
using the revoked key fails while an intended access method still succeeds:

```bash
chmod 600 ~/.ssh/authorized_keys
```

If intended access fails, restore the timestamped backup from the session that
remained open and re-test. Keep the backup until access and Gaming Mode are
confirmed normal.

## End temporary access

`exit` closes only the session. When remote access is no longer needed, and
the owner approves, disable SSH on the Deck:

```bash
sudo systemctl disable --now sshd
systemctl is-active sshd
```

Expected result: `inactive`. Never forward Internet TCP port 22 to the Deck;
use a trusted local network or a properly configured VPN.

## Verification record

Record the SteamOS build, connection type, verified target identity, access
method tested, SSH service state at handoff, and whether a backup remains.
Record only the public-key fingerprint when needed—never key material. Follow
the [verification standard](verification.md).

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | 3.9.5 / 20261023.100 | Existing dedicated-key connection with strict known-host checking; service, enablement, listener, authorization permissions, fingerprint parsing, and explicit client-config bypass | Passed read-only checks: authenticated as `deck`, `sshd` was active and enabled, port 22 listened, SSH authorization modes and ownership matched expectations, and the explicit bypass worked around a rejected local system SSH configuration; key installation/revocation and service shutdown were not repeated |
