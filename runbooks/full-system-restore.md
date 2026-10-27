# Full-system restore after a wipe

## Emergency checklist

Use this checklist during a restore. Follow the linked sections when a check
cannot be completed confidently.

### Before the wipe

- [ ] Confirm this is the intended Steam Deck and note whether it is LCD or OLED.
- [ ] Review Valve's current [recovery options](https://help.steampowered.com/en/faqs/view/1B71-EDF2-EB6D-2BB3); use a less destructive option when suitable.
- [ ] Confirm Steam Cloud synchronization and resolve conflicts.
- [ ] Pass the [backup acceptance test](#backup-acceptance-test).
- [ ] Confirm the latest Steam Deck Support (SS) commit is accessible from another device.
- [ ] Confirm Steam account recovery works without relying only on the Deck.
- [ ] Remove the microSD card and unrelated external storage.
- [ ] Identify the USB drive that will be erased for recovery media.
- [ ] Obtain the owner's explicit approval immediately before the full wipe.

### Re-image and establish a baseline

- [ ] Follow Valve's current [SteamOS installation instructions](https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227).
- [ ] Recheck the recovery option and storage target before selecting the full wipe/install action.
- [ ] Complete SteamOS setup and install stable-channel system and firmware updates.
- [ ] Verify controls, display, audio, Wi-Fi, charging, sleep/wake, and storage.
- [ ] Launch a Steam game in Gaming Mode and check a representative Cloud save.
- [ ] Record **Checkpoint A — stock system healthy**.

### Restore in order

- [ ] Restore and verify SSH, GitHub access, and SS; record **Checkpoint B**.
- [ ] Reinsert and verify the microSD card, if applicable.
- [ ] Restore Steam games and Cloud saves, reviewing any conflicts.
- [ ] Restore selected personal files and non-Cloud saves from the tested backup.
- [ ] Reinstall required applications, then restore only their required data.
- [ ] Restore supported non-Steam software and artwork using SS runbooks.
- [ ] Verify each layer before starting the next; record **Checkpoint C**.
- [ ] Complete the [final verification](#final-verification) and record **Checkpoint D — owner accepted restore**.

## Purpose, authority, and status

Use this runbook to recover from a full internal-drive wipe and restore SS-
supported access and customizations. A full re-image erases local accounts,
settings, applications, games, and other data on the internal drive.

Preparing or updating this guide does not authorize a wipe. Stop when the
device, target, backup state, current Valve instructions, consequences,
approval, or recovery path is unclear. Valve's current instructions take
precedence over summaries in SS.

This guide was reviewed on 2026-10-26 against Valve's documentation, but the
complete wipe-and-restore sequence has not been tested on this Deck.

## Prepare before an emergency

Keep the latest SS commits outside the Deck at:

```text
git@github.com:jaredwines/steamdeck-support.git
```

Maintain an encrypted backup outside the Deck. Keep private keys, passwords,
tokens, account data, and raw diagnostics out of SS.

### Recovery kit

- Deck power supply and a trusted network.
- Another computer with Internet access and this runbook.
- An expendable USB drive of at least 8 GB and any required USB-C adapter.
- Steam account sign-in and recovery methods.
- The encrypted backup and protected credential storage.

### Private recovery worksheet

Keep the completed worksheet in encrypted storage outside the Deck and SS.
Use `not applicable`, `unknown`, or `not recoverable` instead of blanks.

```text
Inventory review date/person:
Deck model and storage size:
SteamOS channel, version/build, and kernel:
Internal storage used/free; microSD contents:
Steam account recovery verified:
Games with Cloud confirmed; non-Cloud saves:
Non-Steam games, launchers, prefixes, and saves:
Flatpak/Discover applications and sources:
Desktop files and application-data paths:
Intentional customizations and owning SS runbook:
Required SSH/GitHub public-key fingerprints:
Backup location, date, encryption, and verification:
Restore-test sample and date:
Known exclusions and accepted losses:
Owner's wipe approval record:
```

When the Deck still boots, these read-only commands help build the worksheet:

```bash
cat /etc/os-release
uname -r
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
df -h / /home
flatpak list --app --columns=application,origin
find ~/.var/app -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort
find ~/Applications -mindepth 1 -maxdepth 2 -printf '%P\n' | sort
git -C /home/deck/steamdeck-support log -1 --format='%H %cI %s'
git -C /home/deck/steamdeck-support remote -v
```

Missing paths are valid findings; do not create them. Review output locally
because names and labels may be private. Check Steam Cloud in Steam for every
important game rather than assuming library membership means Cloud support.

### Backup acceptance test

A backup is ready only when:

- [ ] It is outside the Deck, and its physical or remote destination is identified.
- [ ] Sensitive data is encrypted and can be decrypted on another device.
- [ ] It completed without unexplained errors and has a plausible size.
- [ ] Its checksum or backup-tool verification passes after reconnecting it.
- [ ] Representative files open, including a non-Cloud save and application data when applicable.
- [ ] The recorded SS commit is available from another device.
- [ ] The owner accepts every recorded exclusion or unrecoverable item.

After the wipe, restore selected data rather than the entire old home directory;
this avoids reintroducing stale caches, permissions, and obsolete settings.

## Choose the recovery method

| Situation | Assess first | Data expectation |
| --- | --- | --- |
| A recent update or system modification caused a boot problem | Previous-OS rollback | Intended to retain user data |
| SteamOS needs repair | **Repair SteamOS** | Attempts to preserve games and personal content |
| The Deck boots and a fresh local state is intended | Factory reset in Steam Settings | Clears local data |
| A clean internal drive is required or other options are unsuitable | Full wipe/install from recovery media | Erases internal-drive data and operating systems |

Use Valve's current wording to make the final choice. If the Deck cannot boot,
record unavailable evidence honestly rather than treating it as backed up.

## Install stock SteamOS

At execution time, follow Valve's
[SteamOS Installation and Repair](https://help.steampowered.com/en/faqs/view/65B4-2AA3-5F37-4227)
page. The current high-level flow is:

1. Download Valve's recovery image on another computer.
2. Write it to the identified USB drive using Valve's supported method. This
   erases that drive.
3. Shut down the powered Deck, attach power and the recovery USB, and use
   Valve's current button sequence to enter the Boot Manager.
4. Boot **EFI USB Device** and wait for the recovery desktop.
5. Recheck approval and the target, then select Valve's full wipe/install option.
6. Reboot into the SteamOS welcome experience when installation completes.

Stop if the environment, labels, target, or result differs from Valve's guide.
Do not improvise with partitions or recovery-shell commands.

### Optional non-destructive rehearsal

With separate owner approval, prepare the recovery USB and boot only as far as
the recovery desktop. Select no install, repair, erase, or recovery-tool
action. Power down, boot SteamOS normally, and confirm Gaming Mode works.
Record the image source, date, Deck model, recovery-desktop result, and final
Gaming Mode check. Preparing the USB still erases the USB drive.

## Restore access and SS

After **Checkpoint A**, work in Desktop Mode with local access available:

1. Follow [Remote access](remote-access.md). A re-image changes the Deck's SSH
   host key; verify the new fingerprint locally before replacing only the
   obsolete entry on a support computer.
2. Follow [GitHub access](github-access.md). Recover a private key only from
   protected storage, or create a new key with explicit approval.
3. After `ssh -T git@github.com` identifies the intended account, restore SS:

   ```bash
   test ! -e /home/deck/steamdeck-support && echo "READY" || echo "STOP: path exists"
   git clone git@github.com:jaredwines/steamdeck-support.git /home/deck/steamdeck-support
   cd /home/deck/steamdeck-support
   bash scripts/validate-repository.sh
   git status --short
   ```

Validation must pass and the worktree must be clean. Stop for an unexpected
path, account, remote, validation failure, or worktree change. Record only
public-key fingerprints and **Checkpoint B — intended access and SS healthy**.

## Restore data in layers

After **Checkpoint B**, verify each layer before continuing:

1. Reinsert the microSD card and add its Steam library through Steam's storage
   interface; test a game already on it.
2. Download required Steam games and Cloud saves. Review both copies of any
   Cloud conflict before choosing one.
3. Restore personal files and non-Cloud saves from the tested backup.
4. Reinstall required Flatpak or Discover applications from trusted sources,
   then restore only data each application requires.
5. Reinstall non-Steam launchers and games before their saves or prefixes. Use
   [Non-Steam games](non-steam-games.md) for supported shortcuts and artwork.
6. Reapply other customizations only when an SS runbook supports the current
   SteamOS build.

Stop at the first failed layer. When all required layers pass, record
**Checkpoint C — required data and applications healthy**, including deferred
or unrecoverable items.

## Final verification

- [ ] No stable SteamOS or firmware updates remain pending.
- [ ] Gaming Mode, controls, display, audio, network, charging, and sleep/wake work.
- [ ] A Steam game and representative Cloud save work.
- [ ] Restored files and non-Cloud saves pass representative checks.
- [ ] The microSD library, required applications, and non-Steam shortcuts work.
- [ ] SSH and GitHub access are limited to intended accounts and keys.
- [ ] SS validation passes and its worktree is clean.
- [ ] Temporary sudo authorization is cleared and unneeded SSH is disabled.
- [ ] Commands, changes, deviations, unresolved risks, and backup disposition are recorded.

Confirm Gaming Mode after the last significant change. Keep the recovery USB
and backup until the owner accepts **Checkpoint D**.

## Restore record

Keep the detailed record outside SS while it contains private information.

```text
Restore date/operator and Deck model:
Approval confirmed immediately before wipe:
Valve pages reviewed; recovery image used:
Backup acceptance result; known unavailable data:
Wipe/install result:
Checkpoint A — stock system healthy:
Checkpoint B — intended access and SS healthy:
Checkpoint C — required data and applications healthy:
Checkpoint D — owner accepted restore:
Commands, changed files, and restored layers:
Final Gaming Mode result:
Temporary access disposition:
Deviations, deferred items, accepted losses, and required runbook updates:
```

## Failure and maintenance

If installation fails, preserve the exact sanitized error, recheck Valve's
current guide, and contact Steam Support when the documented path does not
match the device. If a restored layer causes a regression, roll back only that
layer when its runbook documents a safe recovery; otherwise stop at the last
working checkpoint.

Review this runbook before each planned wipe and whenever Valve changes its
recovery process, SteamOS changes restore behavior, SS coverage changes, or a
backup/restore test reveals a gap. Open both Valve links, compare requirements
and labels, then verify SS's path, Git remote, linked runbooks, artwork
inventory, and quality gate. Transfer only sanitized, reusable findings into
SS and follow [Support session](support-session.md).

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Compared with Valve's current pages; checked SS paths and remote locally | Plan ready; full wipe and restore remain unverified |
