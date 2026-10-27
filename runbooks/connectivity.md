# Wi-Fi and Bluetooth connectivity

## Purpose and status

Use this runbook for Wi-Fi connection quality and Bluetooth pairing or reconnect
problems. It does not cover router administration. No repair in this runbook has
yet been verified on this Deck.

## Quick path

Record the current private connection state, determine whether the failure is
Deck-only or network/device-specific, try a normal reconnect first, and obtain
approval before forgetting or re-pairing anything.

## Approval and prerequisites

Basic status inspection is read-only. Obtain approval before changing network
settings, forgetting a network or Bluetooth device, re-pairing, restarting
services, or comparing another network. Never record passwords, SSIDs, local
addresses, paired-device identifiers, or router configuration in SS.

## Read-only baseline

Record whether other devices are affected, whether the issue occurs in both
Gaming and Desktop Mode, distance from the access point, dock use, and recent
changes. Review output locally:

```bash
nmcli general status
nmcli device status
rfkill list
systemctl --failed --no-pager
systemctl --user --failed --no-pager
```

Before a connection change, privately record the active profile and enough
non-secret state to restore it:

```bash
nmcli -t -f NAME,UUID,TYPE,DEVICE connection show --active
nmcli radio wifi
nmcli -f connection.autoconnect,connection.metered,ipv4.method,ipv6.method connection show '<active-profile>'
```

Do not share unredacted connection listings or logs. Confirm the prior network
password and pairing method are available before forgetting anything; SS must
not store either one.

## Wi-Fi path

1. Keep the Deck awake and test near the known access point.
2. Disconnect optional docks or USB devices one at a time.
3. Determine whether failure is Deck-only, network-only, or location-specific.
4. With approval, reconnect using SteamOS interfaces. Forgetting a network is a
   separate change and requires the password and recovery path to be available.
5. Compare another authorized network only when it will distinguish Deck from
   router behavior.

## Bluetooth path

1. Confirm Bluetooth is enabled and the accessory is charged and available.
2. Disconnect other hosts that may automatically claim the accessory.
3. Attempt a normal reconnect before forgetting anything.
4. With approval and the pairing method available, forget and re-pair only the
   intended device.

## Verification and recovery

Test the original activity for at least ten minutes and through one sleep/wake
cycle when relevant. For Bluetooth, test the actual input or audio path. If a
comparison fails, reconnect the recorded prior profile through SteamOS and
confirm its recorded autoconnect, metered, and IP-method state. Re-pair only the
recorded intended Bluetooth device. Stop for repeated hardware disappearance,
kernel errors, missing credentials, or a change requiring undocumented service
edits.

## Compatibility record

| Review date | SteamOS version/build | Scope | Result |
| --- | --- | --- | --- |
| 2026-10-26 | 3.9.5 / 20261023.100 | Read-only network baseline and active-profile recovery-state capture | Passed: baseline and recorded autoconnect, metered, and IP-method queries completed; reconnect, forget, re-pair, and failure recovery remain unverified |
