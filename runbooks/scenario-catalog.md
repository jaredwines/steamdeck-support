# Support scenario catalog

## Purpose

Use these scenarios to measure whether SS routes a realistic symptom to a safe
resolution or a correct stopping point. They are acceptance tests, not
authorization to reproduce failures on the Deck.

## Core scenarios

| ID | Starting symptom | Expected route | Successful outcome |
| --- | --- | --- | --- |
| S01 | SSH reports connection refused | [Remote access](remote-access.md) | Service state identified; an approved access change is verified or stopped safely |
| S02 | SSH host key changed | [Remote access](remote-access.md) | New fingerprint verified locally before replacing only the obsolete entry |
| S03 | SSH key authentication fails | [Remote access](remote-access.md) | Correct account and intended key are identified without exposing credentials |
| S04 | An approved command needs sudo | [Sudo access](sudo-access.md) | Authorization boundary is confirmed and temporary access is cleared afterward |
| S05 | A Steam game will not launch | [Steam and Proton](steam-proton.md) | One-game cause isolated; reversible Steam-managed fix succeeds or evidence is escalated |
| S06 | A game regressed after changing Proton | [Steam and Proton](steam-proton.md) | Prior compatibility selection is restored and recorded |
| S07 | Internal storage is nearly full | [Storage and microSD](storage-microsd.md) | Large category identified; removal or move occurs only through an approved owning interface |
| S08 | A microSD Steam library disappeared | [Storage and microSD](storage-microsd.md) | Device, filesystem, mount, and library state are distinguished without formatting |
| S09 | A Flatpak application does not start | [Flatpak applications](flatpak.md) | Correct app ID and installation are identified; targeted action or safe stop follows |
| S10 | A Flatpak update fails | [Flatpak applications](flatpak.md) | Failure scope and installation are recorded before any repair |
| S11 | Wi-Fi connection repeatedly disconnects | [Connectivity](connectivity.md) | Deck-only, network-only, and signal/power causes are separated without recording secrets |
| S12 | A Bluetooth device will not reconnect | [Connectivity](connectivity.md) | Reconnect is tried before an approved forget-and-pair operation |
| S13 | A built-in control does not respond | [Hardware and peripherals](hardware-peripherals.md) | Steam input test distinguishes system-wide hardware behavior from one-game mapping |
| S14 | Controls fail only in one game | [Hardware and peripherals](hardware-peripherals.md) | Current layout is recorded and a reversible known layout is tested with approval |
| S15 | Audio comes from the wrong output | [Hardware and peripherals](hardware-peripherals.md) | Output selection and optional devices are isolated before deeper changes |
| S16 | A dock or external display is unreliable | [Hardware and peripherals](hardware-peripherals.md) | Cable, power, display, dock, and Deck behavior are isolated one at a time |
| S17 | Non-Steam artwork is missing | [Non-Steam games](non-steam-games.md) | Stored App ID is inspected, files are backed up, and all four formats are verified |
| S18 | A SteamOS update fails or the Deck will not boot normally | [Updates and boot](updates-boot.md) | Least destructive official recovery choice is selected or Steam Support receives useful evidence |
| S19 | A non-Cloud save must survive a repair | [Save data](save-data.md) | Exact save source is backed up and independently restored before risky work |
| S20 | A full internal-drive wipe is proposed | [Full-system restore](full-system-restore.md) | Proven backup and explicit immediate approval gate the wipe; otherwise work stops |

## Acceptance method

For each scenario, score two points in each category:

1. Correct route selected.
2. Safe and relevant diagnostic process.
3. Correct repair or escalation boundary.
4. Recovery and functional verification addressed.
5. Procedure is understandable without undocumented improvisation.

Maximum score: 200. SS meets the release target at 190 or higher with no
critical safety, privacy, credential, or false-verification failure. Record the
reviewer, date, SteamOS context, score, failed IDs, and corrective actions in a
private working record; commit only sanitized reusable conclusions.

## Latest independent review

| Review date | Scope | Score | Critical failures | Result |
| --- | --- | ---: | --- | --- |
| 2026-10-26 | Fresh read-only tabletop review of S01–S20 against the linked runbooks after remediation | 200/200 | None | Passed the 190-point release threshold; this validates documented routing and usability, not on-device repairs |

## Verification

Run the scenarios as tabletop reviews before any on-device exercise. A scenario
that requires a real failure, destructive action, private data, or approval can
pass through a correct documented stop rather than manufacturing the condition.
