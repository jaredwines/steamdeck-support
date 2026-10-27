# GitHub access

## Purpose

Use this runbook to verify or restore Git and GitHub SSH access on the Steam
Deck.

## Approval and prerequisites

Reading Git configuration and testing authentication are read-only. Creating
or replacing an SSH key, changing global Git configuration, or registering a
public key with GitHub is security-sensitive and requires the owner's explicit
approval. Confirm the intended GitHub account before changing anything.

## Inspect the configured identity

Git identity and key paths are owner-specific. Inspect them before changing
anything; do not copy personal values from this runbook:

```bash
git config --global --get user.name
git config --global --get user.email
git config --global --get core.sshCommand
```

This Deck conventionally uses `~/.ssh/id_ed25519_git`. Its private key must
remain local with mode `600`; only its `.pub` companion may be added to GitHub.
Never put either key in a repository or support ticket.

Git selects the key with:

```bash
git config --global core.sshCommand 'ssh -i /home/deck/.ssh/id_ed25519_git -o IdentitiesOnly=yes'
```

Treat every identity as device-specific configuration. With explicit approval,
set the intended values only after confirming the target GitHub account:

```bash
git config --global user.name '<intended-name>'
git config --global user.email '<intended-email>'
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

Expected result: a greeting for the intended account followed by a note that
GitHub does not provide shell access. `Permission denied (publickey)` means the
public key is missing from the account or SSH is not selecting the configured
key.

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
