# Steam Deck Support Guide

## Purpose

This guide covers remote command-line support for a Steam Deck running SteamOS
on the local network.

The Steam Deck account is `deck`. Its expected support address is
`192.168.1.67`; verify the device and host key before treating that address as
the Deck.

## Fast path

Use this when the Deck has already been set up and the host key was previously
verified:

```bash
ssh -i <private-key-path> deck@192.168.1.67
whoami
sudo -l
```

`whoami` must return `deck`. If the session needs temporary shared sudo access
and `sudo -n true` fails, run `sudo -v` in a trusted `deck` session and enter
the account password at its prompt. When support work is complete, run
`sudo -k` to clear that temporary authorization, then `exit`.

For a first connection, an address mismatch, a missing key, or any sudo-policy
change, use the detailed sections below instead.

## Quick connection

From the support computer, connect with:

```bash
ssh deck@192.168.1.67
```

This address is reachable only when the support computer and the Steam Deck are
on the same local network.

To close the session safely, run:

```bash
exit
```

## Prepare the Steam Deck

On the Steam Deck:

1. Switch to **Desktop Mode**.
2. Open **Konsole**.
3. Set or update the password for the `deck` account, if necessary:

   ```bash
   passwd
   ```

4. Enable and start the SSH service:

   ```bash
   sudo systemctl enable --now sshd
   ```

5. Confirm that it is active:

   ```bash
   systemctl is-active sshd
   ```

   Expected result: `active`.

## Verify the connection

After signing in, run:

```bash
whoami
uname -a
cat /etc/os-release
```

`whoami` should return `deck`. The remaining commands confirm that the session
is running on SteamOS.

### Verify the first-connection fingerprint

The first SSH connection displays a host-key fingerprint. Before accepting it,
run this locally on the Steam Deck in Konsole:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Confirm that the displayed SHA256 fingerprint matches the fingerprint shown on
the support computer. Accept it only when the values match.

### Confirm the expected network address

Run:

```bash
ip -4 addr show wlan0
ip route
```

Confirm that `wlan0` has `192.168.1.67`. Prefer a DHCP reservation configured
on the router so another device cannot receive this address later. If the Deck
uses Ethernet instead of Wi-Fi, check the active Ethernet interface as well.

## Recommended secure setup

Use an SSH key for recurring support access. Add only the public key to the
Steam Deck. Never copy or share the private key.

### Linux or macOS support computer

Generate a dedicated key:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/steam_deck_support -C "steam-deck-support"
```

Install its public key on the Steam Deck:

```bash
ssh-copy-id -i ~/.ssh/steam_deck_support.pub deck@192.168.1.67
```

If `ssh-copy-id` is unavailable, use:

```bash
cat ~/.ssh/steam_deck_support.pub | ssh deck@192.168.1.67 'umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys'
```

Test the key explicitly:

```bash
ssh -i ~/.ssh/steam_deck_support deck@192.168.1.67
```

### Dedicated Codex access

When a persistent Codex environment needs access, give it its own dedicated
SSH key rather than sharing a person's private key. Store that private key only
in the environment's protected SSH or credential storage, authorize its public
key for `deck`, and identify it with a clear comment such as
`codex-steamdeck`. Test it with an explicit identity path before relying on it.
For tools that use SSH's default key lookup, use a standard identity name such
as `~/.ssh/id_ed25519`, or configure the tool with the dedicated key path.
Revoke that one public-key line from `~/.ssh/authorized_keys` when the Codex
environment no longer needs access.

## Git and GitHub SSH access

Git is installed on the Steam Deck. The configured commit identity is:

```bash
git config --global user.name "jaredwines"
git config --global user.email "jwines760@gmail.com"
```

GitHub SSH access uses the dedicated key at `~/.ssh/id_ed25519_git`. The
private key must remain local, with mode `600`; only its `.pub` companion may
be added to a GitHub account. Do not put either key in a repository or support
ticket.

The Git configuration selects this key for SSH remotes:

```bash
git config --global core.sshCommand 'ssh -i /home/deck/.ssh/id_ed25519_git -o IdentitiesOnly=yes'
```

To restore GitHub access, copy the public key and add it in GitHub under
**Settings → SSH and GPG keys**:

```bash
cat ~/.ssh/id_ed25519_git.pub
```

Then verify that GitHub accepts the key:

```bash
ssh -T git@github.com
```

Expected result: a greeting for the `jaredwines` account followed by a note
that GitHub does not provide shell access. A `Permission denied (publickey)`
result means the public key has not been added to the account or the Git SSH
configuration is not selecting it.

### Windows PowerShell support computer

Generate a dedicated key:

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\steam_deck_support" -C "steam-deck-support"
```

Install its public key on the Steam Deck:

```powershell
Get-Content "$env:USERPROFILE\.ssh\steam_deck_support.pub" | ssh deck@192.168.1.67 'umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys'
```

Test the key explicitly:

```powershell
ssh -i "$env:USERPROFILE\.ssh\steam_deck_support" deck@192.168.1.67
```

Do not disable password authentication until key-based login has succeeded in
a separate connection. Keep the original session open while testing so a setup
mistake does not cause a lockout.

Do not include passwords, private keys, or other secrets in support tickets,
chat messages, or this document.

The `deck` account may require its password for `sudo`. Enter that password only
at a trusted local or SSH password prompt; never paste it into chat.

### Optional: share a temporary sudo authentication across SSH sessions

If the owner specifically needs a recently authenticated `deck` sudo session
to be reusable from another SSH session, configure a per-user sudo timestamp
policy. This does **not** make general sudo passwordless: `deck` must first
authenticate with its own password, and the usual sudo timeout still applies.

On the Deck, first confirm that the dedicated configuration file does not
already exist:

```bash
sudo test ! -e /etc/sudoers.d/90-deck-global-sudo-timestamp && echo "ready to create" || echo "STOP: file already exists"
```

Only when it reports `ready to create`, install and validate the narrowly
scoped rule:

```bash
printf '%s\n' 'Defaults:deck timestamp_type=global' | sudo tee /etc/sudoers.d/90-deck-global-sudo-timestamp >/dev/null
sudo chmod 440 /etc/sudoers.d/90-deck-global-sudo-timestamp
sudo visudo -c
sudo -l
```

`sudo -l` should list `timestamp_type=global` under the matching defaults.
Run `sudo -v` in one `deck` session, then verify from a separate SSH session:

```bash
sudo -n true && echo SUDO_OK || echo SUDO_NOT_AVAILABLE
```

Use `sudo -k` to invalidate the cached authorization when the support work is
complete. The policy and authorized SSH keys persist across a reboot, but the
active sudo authorization does not; after reboot, run `sudo -v` as `deck` and
enter the account password before relying on shared authorization again. Recheck
this policy after major SteamOS updates.

### Restore shared sudo access when it expires

If SSH works but a noninteractive check reports `SUDO_NOT_AVAILABLE`, the sudo
authorization has likely expired or was cleared. In a trusted `deck` session,
run:

```bash
sudo -v
```

Enter the `deck` password only at that prompt, then repeat the noninteractive
check from the other SSH session. If `sudo -v` itself is denied, stop and check
the `deck` sudo policy locally; do not attempt to bypass it.

## Support-session procedure

Before making changes:

1. Explain the intended change and obtain the owner’s approval.
2. Record the commands that will be run.
3. Back up configuration files before editing them.
4. Avoid disabling SteamOS read-only protections unless a task explicitly
   requires it and includes a recovery plan.

After significant changes, reboot if appropriate, confirm that Gaming Mode
works normally, and record the final result.

## Non-Steam games, launchers, and artwork

For the complete repeatable procedure, use the
[Non-Steam Game & Artwork Setup Guide](steam/add-non-steam-game-and-artwork-guide.md).
The verified artwork backups are stored in
[steam/artworks/battle.net](steam/artworks/battle.net/) and
[steam/artworks/wowup-curseforge](steam/artworks/wowup-curseforge/).

### Standard workflow

1. Add or inspect the non-Steam shortcut in Desktop Mode and record its App ID.
2. Back up its existing Steam grid files before replacing anything.
3. Install the four format-specific artwork files.
4. Confirm the game and launcher are closed before restarting Steam.
5. Verify the wide cover, portrait cover, selected-game hero, and title logo in
   Gaming Mode.

### Verified Steam artwork mapping

| File | Size | Purpose | Title rule |
| --- | ---: | --- | --- |
| `<appid>.png` | 920 x 430 | Wide library cover | Bake the title into the image. |
| `<appid>p.png` | 600 x 900 | Portrait cover | Bake the title into the image. |
| `<appid>_hero.png` | 1920 x 620 | Selected-game hero background | Do not bake in a title. |
| `<appid>_logo.png` | 1200 x 300 | Hero title logo | Transparent PNG; title only. |

The plain `.png` is the wide cover and the `p.png` file is the portrait cover.
Steam overlays the transparent logo on the hero; a title in both files appears
twice.

### Safe Steam restart for artwork changes

Before restarting Steam, confirm that no game, launcher, Proton, or Wine
process is active. Then restart Steam's user service:

```bash
systemctl --user restart app-steam@autostart.service
pgrep -u deck -x steam >/dev/null && echo "STEAM_RUNNING"
```

Do not force-close Steam while a game or launcher is running unless the owner
has explicitly approved interrupting it.

### WowUp (CurseForge) for WoW Forever

The stable WowUp launcher is `~/Applications/WowUp-CurseForge`; its AppImage
files live in `~/Applications/`. The wrapper selects the newest executable
`WowUp-CF-*.AppImage`, clears `LD_PRELOAD`, and runs it with `--no-sandbox`.
Use the wrapper rather than adding a versioned AppImage directly to Steam.

Keep Steam Overlay disabled for the WowUp shortcut. If WowUp fails from Steam,
first verify that the shortcut targets the stable wrapper and that Overlay is
off before changing anything else.

WoW Forever add-ons are installed under:

```text
~/.local/share/Steam/steamapps/compatdata/3104267125/pfx/drive_c/
Program Files (x86)/World of Warcraft/_forever_/Interface/AddOns
```

Keep a separate backup of add-ons and configuration before changing the game
prefix or reinstalling the launcher.

### Artwork recovery notes

| Symptom | Recovery |
| --- | --- |
| Portrait and wide cards are reversed | Swap `<appid>.png` and `<appid>p.png`. |
| Title is clipped | Use a format-specific design and move it farther inside the safe area. |
| Hero has a duplicate title | Remove the title from `<appid>_hero.png`; keep `<appid>_logo.png`. |
| A dark title panel is unwanted | Re-render without the translucent panel; retain a thin text outline if needed. |
| Steam shows old artwork | Restart Steam and verify the App ID, Steam user ID, and grid folder. |
| The logo has a black box | Export it as transparent RGBA PNG artwork. |

## Diagnostics for support tickets

If access fails, collect the following on the Steam Deck and share the output
only after removing anything sensitive:

```bash
systemctl is-active sshd
ip -br addr
whoami
uname -a
```

For recent SSH service messages, run:

```bash
sudo journalctl -u sshd --since "30 minutes ago"
```

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `Connection refused` | Start SSH with `sudo systemctl enable --now sshd`. |
| Timeout or `No route to host` | Confirm both devices are on the same local network and that the Deck still uses `192.168.1.67`. |
| `Permission denied` | Confirm the username is `deck` and verify the password or authorized SSH key. |
| SSH works but `sudo -n` fails | Refresh the temporary authorization with `sudo -v`, if shared sudo authorization is configured. |
| Connection drops | Keep the Steam Deck awake and connected to power during support work. |
| Access fails after an update | Recheck the SSH service and any intentionally customized configuration. |

## End temporary SSH access

Closing a session with `exit` does not turn off the SSH service. If remote
access is no longer needed, disable and stop the service on the Steam Deck:

```bash
sudo systemctl disable --now sshd
```

Confirm the result:

```bash
systemctl is-active sshd
```

Expected result: `inactive`.

Do not forward TCP port 22 from the internet to the Steam Deck. Use SSH only on
a trusted local network unless remote access is protected through a properly
configured VPN.

## SteamOS safety notes

SteamOS is designed to be updated and managed as a console operating system.
Avoid unnecessary system-wide changes, get the owner’s approval before making
changes, and record each change made during a support session.

## Completion checklist

- [ ] `sshd` is active on the Steam Deck.
- [ ] The first-connection host fingerprint has been verified.
- [ ] `192.168.1.67` is assigned to the Deck and reserved on the router.
- [ ] `ssh deck@192.168.1.67` connects successfully.
- [ ] `whoami` returns `deck`.
- [ ] Key-based authentication works, if configured.
- [ ] Temporary shared sudo authorization has been verified or intentionally omitted.
- [ ] Significant changes have been recorded and normal Gaming Mode operation has been checked.
- [ ] Support access has been reviewed or disabled when it is no longer needed.

### Non-Steam game completion checklist

- [ ] The non-Steam shortcut launches as expected.
- [ ] Its wide and portrait covers display in the correct layouts.
- [ ] Its hero background has no duplicate baked-in title.
- [ ] Its transparent title logo displays once on the hero.
- [ ] Associated launcher and add-ons, if any, work as expected.
- [ ] Steam restarted cleanly and Gaming Mode works normally.
