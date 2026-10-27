# Steam Deck Support Runbooks

## Start here

This is the required entry point for remote command-line support of a Steam
Deck running SteamOS. The expected target is `deck@192.168.1.67`, but verify
the device, network address, and SSH host key before treating it as the Deck.

Use only the runbook that matches the task. Do not use a procedure when its
prerequisites, authorization, verification, or recovery path are unclear.

## Safety rules

- Obtain the owner's explicit approval before using `sudo` or making a
  destructive, security-sensitive, system-wide, or difficult-to-reverse
  change.
- Never request, record, display, or share passwords, private SSH keys,
  tokens, or host-key material.
- Prefer reversible user-level changes. Do not disable SteamOS read-only
  protection unless the task explicitly requires it and includes a recovery
  plan.
- Preserve normal Steam and Gaming Mode operation. After significant work,
  verify Gaming Mode before handoff.
- A SteamOS update may overwrite custom configuration; record that risk where
  it applies.

## Fast path

Use this only when the Deck and its host key have already been verified and a
valid SSH key is configured:

```bash
ssh -i <private-key-path> deck@192.168.1.67
whoami
sudo -l
```

`whoami` must return `deck`. If the task requires temporary shared sudo access
and `sudo -n true` fails, follow [Sudo access](sudo-access.md). When work is
complete, run `sudo -k` to clear temporary authorization and then `exit`.

## Choose a task

| Task | Runbook |
| --- | --- |
| Set up, verify, or disable SSH access | [Remote access](remote-access.md) |
| Use or configure temporary shared sudo access | [Sudo access](sudo-access.md) |
| Use Git or restore GitHub SSH access on the Deck | [GitHub access](github-access.md) |
| Plan, perform, document, and hand off support work | [Support session](support-session.md) |
| Collect safe diagnostics or resolve common access failures | [Diagnostics](diagnostics.md) |
| Add a non-Steam game, launcher, or artwork | [Non-Steam games](non-steam-games.md) |

## Before handoff

- [ ] Commands run, files changed, checks performed, and unresolved risks are recorded.
- [ ] Required verification passed; Gaming Mode was checked after significant work.
- [ ] Temporary sudo authorization was cleared, if used.
- [ ] Remote access was reviewed or disabled when it is no longer needed.
- [ ] Verified reusable knowledge was added to the applicable runbook.
