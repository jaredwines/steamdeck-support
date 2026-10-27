# Power, charging, heat, and performance

## Purpose and status

Use this runbook to distinguish workload, settings, accessory, and possible
hardware problems affecting battery, charging, temperature, or performance. It
does not prescribe hardware repair. No repair here has been verified on this Deck.

## Quick path

Stop immediately for physical battery danger; otherwise record power source,
workload, limits, and idle behavior, remove optional causes one at a time, and
return to stock settings before escalating persistent symptoms.

## Approval and prerequisites

Observation and Steam's performance overlay are diagnostic. Obtain approval
before changing performance limits, update state, startup software, or power
configuration. Use a known suitable power supply. Stop immediately for swelling,
liquid, smoke, unusual smell, visible damage, or unsafe temperature and contact
Steam Support; do not charge or open the Deck.

## Baseline

Record the power source, charge percentage and trend, workload, frame cap,
refresh rate, thermal environment, connected accessories, and whether the
symptom persists at idle. Read-only command-line context:

```bash
cat /etc/os-release
uname -r
upower -i /org/freedesktop/UPower/devices/battery_BAT1
```

If the battery path is absent, record that result rather than guessing another
device. Battery identifiers and detailed histories stay outside SS.

## Isolation

1. Close optional applications and remove optional peripherals one at a time.
2. Compare idle behavior with one representative game using Steam's overlay.
3. Record per-game performance settings before changing them. With approval,
   return one affected game to known stock limits and retest.
4. Compare direct charging with docked charging using appropriate known-good
   equipment when available.
5. If abnormal behavior remains on an updated stock configuration, preserve
   sanitized evidence and escalate instead of changing low-level power controls.

## Verification and recovery

Repeat the same workload and duration, confirm stable charging or performance,
and ensure controls, audio, network, sleep/wake, and Gaming Mode remain normal.
Restore recorded per-game settings when the test does not help. Do not calibrate
by intentionally deep-discharging the battery or modify firmware controls.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | Not tested on-device | Safe observation and stock-setting isolation reviewed | Ready for use; repairs remain unverified |
