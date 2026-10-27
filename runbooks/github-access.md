# GitHub access

## Purpose

Use this runbook to verify or restore Git and GitHub SSH access on the Steam
Deck.

## Approval and prerequisites

Reading Git configuration and testing authentication are read-only. Creating
or replacing an SSH key, changing global Git configuration, or registering a
public key with GitHub is security-sensitive and requires the owner's explicit
approval. Confirm the intended GitHub account before changing anything.

## Configured identity

The Deck's configured commit identity is:

```bash
git config --global user.name "jaredwines"
git config --global user.email "jwines760@gmail.com"
```

GitHub SSH access uses `~/.ssh/id_ed25519_git`. Its private key must remain
local with mode `600`; only its `.pub` companion may be added to GitHub. Never
put either key in a repository or support ticket.

Git selects the key with:

```bash
git config --global core.sshCommand 'ssh -i /home/deck/.ssh/id_ed25519_git -o IdentitiesOnly=yes'
```

Treat this identity as device-specific configuration, not as a template for a
different owner. Before changing it, inspect the existing values:

```bash
git config --global --get user.name
git config --global --get user.email
git config --global --get core.sshCommand
```

## Restore and verify

Copy the public key and add it in GitHub under **Settings → SSH and GPG keys**:

```bash
cat ~/.ssh/id_ed25519_git.pub
```

Then verify authentication:

```bash
ssh -T git@github.com
```

Expected result: a greeting for `jaredwines` followed by a note that GitHub
does not provide shell access. `Permission denied (publickey)` means the public
key is missing from the account or Git is not selecting the configured key.

## If the dedicated key is missing

Do not overwrite an existing key. With explicit approval, create the dedicated
key only when both the private and public paths are absent:

```bash
test ! -e ~/.ssh/id_ed25519_git && test ! -e ~/.ssh/id_ed25519_git.pub && echo "READY" || echo "STOP: key path exists"
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_git -C "steam-deck-github"
chmod 600 ~/.ssh/id_ed25519_git
chmod 644 ~/.ssh/id_ed25519_git.pub
```

Show and register only the `.pub` file, then set `core.sshCommand` as documented
above. Never copy, print, commit, or upload the private key.

## Verification and recovery

After `ssh -T git@github.com` succeeds, verify the intended repository without
changing it:

```bash
git -C /home/deck/steamdeck-support remote -v
git -C /home/deck/steamdeck-support ls-remote --exit-code origin HEAD
```

Record the SteamOS build, authenticated GitHub account, selected public-key
fingerprint, and command result; never record the private key. If a newly
created key or configuration is wrong, keep the original session open, restore
the previously recorded Git values, and remove or revoke only the newly added
public key after explicit approval. Follow the
[verification standard](verification.md).
