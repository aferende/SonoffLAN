# Aferende SonoffLAN fork

This repository tracks [AlexxIT/SonoffLAN](https://github.com/AlexxIT/SonoffLAN) as its read-only upstream. Changes specific to this deployment are made only in this fork.

## `3.12.2-aferende.5`

### Reconciled cloud-response alerts

- Treats a `411` or `504` response as ambiguous until a state query verifies the
  outcome. A command that has actually reached the device is recorded as
  recovered instead of being reported as a failed command.
- For the opt-in safe retry, verifies the device state after the retry before
  retaining an error. This avoids reporting a transient response error when the
  requested state is already in effect.
- Emits the existing `Cloud command error ...` warning only for an unconfirmed
  outcome. Home Assistant/Telegram monitoring consequently alerts only for a
  failure requiring attention, while debug logs retain the initial cloud reply.

## `3.12.2-aferende.4`

### Redundant cloud commands and safe diagnostics

- Re-checks an explicit `switch: on` or `switch: off` command while holding the
  per-device cloud lock and skips it when the known state already matches.
- Queues the non-actuating post-command state query before releasing that lock,
  reducing command overlap for the same cloud-only device.
- Explicitly redacts app credentials, cloud credentials, device/bridge IDs,
  sequence values, device names and local network addresses from exported
  diagnostics and from diagnostic copies of system-log messages.
- Retains only non-identifying troubleshooting context in diagnostics: command
  type and parameter names, error code, model, firmware, RSSI, latency and
  reconciliation result.

## `3.12.2-aferende.3`

### Cloud alert readability

- Adds the resolved Sonoff device name to each cloud-command error log. Existing
  `system_log_event`/Telegram monitoring therefore reports both the `deviceid`
  and the human-readable device name for errors `411` and `504`.

## `3.12.2-aferende.2`

### Cloud command recovery and diagnostics

- Extends the optional cloud recovery setting from error `504` to errors `411` and `504`.
- Retries only a single, unconfirmed and idempotent `switch: on` or `switch: off` command. The setting is disabled by default.
- Performs a state reconciliation before the retry and does not retry when that reconciliation reports the requested state.
- Does not retry toggles, scenes, multi-parameter commands, or commands whose effects cannot be repeated safely.
- Adds redacted telemetry to integration diagnostics and device diagnostics: cloud transport, command origin, parameter names, command/error latency, parent model, bridge framework, and reported device/bridge RSSI.
- Marks commands to a `ZBBridge-P` Zigbee child as cloud transport with the reason `zbbridge_child_lan_unsupported`. Framework 3.3.0 does not support LAN control of those children.

## `3.12.2-aferende.1`

### Safe eWeLink error handling

- Adds per-device cloud command serialisation and an in-flight command registry.
- Logs cloud errors without API keys, user identifiers or command values.
- Captures a bounded, redacted history of cloud command errors in diagnostics.
- Schedules one non-actuating state reconciliation after errors `411` and `504`.
- Adds the optional cloud recovery setting, initially limited to safe switch commands after `504`.
- Treats eWeLink responses containing `error: 0` without `params` as successful acknowledgements rather than unknown-response warnings.
- Adds the Home Assistant monitor automation used by this deployment for real `411` and `504` events. The automation is local deployment configuration and is not part of this repository.

## Upgrade notes

1. Keep the integration in `auto` mode.
2. Leave cloud retry disabled until diagnostic data confirms that a single retry improves the affected devices.
3. If enabled, monitor `Cloud command error code=411` and `Cloud command error code=504` together with the exported integration diagnostics before changing retry behaviour.
