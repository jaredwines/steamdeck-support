# GitHub access

## Purpose

Use this runbook to verify or restore Git and GitHub SSH access on the Steam
Deck.

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
