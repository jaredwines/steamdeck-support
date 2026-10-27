# Remote access

## Purpose

Use this runbook to prepare, verify, or end SSH access to the Steam Deck.

## Approval and prerequisites

Inspecting network and SSH status is read-only. Setting a password, enabling or
disabling SSH, authorizing or revoking a key, and changing SSH configuration
require the owner's explicit approval. Perform setup in Desktop Mode with local
access available so a failed remote change cannot lock out the owner.

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
