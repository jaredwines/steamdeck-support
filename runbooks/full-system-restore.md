# Full-system restore after a wipe

## Emergency checklist

Use this checklist during a restore. Follow the linked sections when a check
cannot be completed confidently.

### Before the wipe

- [ ] Confirm this is the intended Steam Deck and note whether it is LCD or OLED.
- [ ] Review Valve's current [recovery options](https://help.steampowered.com/en/faqs/view/1B71-EDF2-EB6D-2BB3); use a less destructive option when suitable.
- [ ] Inventory every operating system, partition, and boot customization on the internal drive; a full re-image removes all of them.
- [ ] Confirm Steam Cloud synchronization and resolve conflicts.
- [ ] Complete [Backup and restore readiness](backup-and-restore.md) and pass its acceptance test.
- [ ] Confirm the latest Steam Deck Support (SS) commit is accessible from another device.
- [ ] Confirm Steam account recovery works without relying only on the Deck.
- [ ] Remove the microSD card and unrelated external storage.
- [ ] Identify the USB drive that will be erased for recovery media; confirm it is not a backup destination and contains nothing needed.
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

## Quick path

Use the emergency checklist: prove the encrypted backup and account recovery,
prefer a less destructive official option, obtain immediate approval before any
wipe, establish a healthy stock checkpoint, and restore one verified layer at a
time.

## Prepare before an emergency

Keep the latest SS commits outside the Deck at:

```text
git@github.com:jaredwines/steamdeck-support.git
```

Follow [Backup and restore readiness](backup-and-restore.md) to inventory the
Deck, create encrypted off-device copies, and prove that representative data
can be restored. Do not wipe until that runbook's acceptance test passes and
the owner accepts every exclusion or unrecoverable item.

Keep private keys, passwords, tokens, account data, completed worksheets, and
raw diagnostics out of SS.

### Recovery kit

- Deck power supply and a trusted network.
- Another computer with Internet access and this runbook.
- An expendable USB drive of at least 8 GB and any required USB-C adapter.
- Steam account sign-in and recovery methods.
- The encrypted backup and protected credential storage.

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

Download the image only through Valve's current page. Record its source URL,
download date, filename, and size. If Valve publishes a checksum, verify and
record it; if Valve does not, record that fact rather than substituting an
untrusted third-party checksum. Use the imaging tool's validation or read-back
feature when it provides one, safely eject the USB, and treat a successful boot
to the recovery desktop as the practical media check. Never continue from a
download, write, validation, or boot error.

### Optional non-destructive rehearsal

With separate owner approval, prepare the recovery USB and boot only as far as
the recovery desktop. Select no install, repair, erase, or recovery-tool
action. Power down, boot SteamOS normally, and confirm Gaming Mode works.
Record the image source, date, Deck model, recovery-desktop result, and final
Gaming Mode check. Also record elapsed boot time and any prompts or labels that
differ from Valve's current guide. Preparing the USB still erases the USB
drive. This rehearsal verifies the media and boot path, not the re-image or
data restore.

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
Valve pages reviewed; recovery image source, filename, size, and verification:
Backup tool, source manifest, destination, result, and exclusions:
Independent restore-test sample and result:
Internal-drive operating systems/partitions and accepted losses:
Wipe/install result, elapsed time, prompts, and deviations:
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

For the first observed use on each Deck model or materially different SteamOS
release, record the following as separate evidence; do not promote a lower
level into a claim about a higher one:

1. Valve-document review and local repository validation.
2. Recovery image written, validated when supported, and booted to the recovery desktop.
3. Full re-image completed and Checkpoint A passed.
4. Required layers restored and Checkpoints B through D passed.

After a verified execution, add the SteamOS build, Deck model, highest evidence
level reached, important label or timing differences, recovery result, and any
remaining limitation to the compatibility record.

## Compatibility record

| Review date | Deck model | SteamOS version/build | Evidence level | Result |
| --- | --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Not tested on-device | 1 — documentation review | Compared with Valve's current pages; checked SS paths and remote locally; media boot, re-image, and restore remain unverified |
