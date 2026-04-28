## 1. Logging foundation

- [x] 1.1 Add a single stdout logging helper that emits stable `key=value` lines with mandatory `event` field and immediate flush.
- [x] 1.2 Define canonical stage names/constants for all major pipeline steps to prevent naming drift in logs.
- [x] 1.3 Normalize final run summary output to the same structured `key=value` logging format.

## 2. Stage instrumentation

- [x] 2.1 Instrument `main()` with `stage_start` and `stage_end` events for extraction, title scan, index build, conversion, TOC build, breadcrumb injection, and log writing stages.
- [x] 2.2 Add per-stage elapsed time calculation and emission via `elapsed_sec` on each `stage_end` event.
- [x] 2.3 Ensure optional `shlang` branch emits the same stage events only when `--lang-hbk` is provided.

## 3. Progress heartbeat

- [x] 3.1 Add periodic heartbeat emission in archive conversion loops with `event=progress`.
- [x] 3.2 Include progress metrics in heartbeat logs: `stage`, `done`, `total`, `pct`, `elapsed_sec`, `rate_fps`, `eta_sec`.
- [x] 3.3 Implement sparse emission policy (fixed item interval + forced final progress event) to balance observability and log volume.

## 4. Verification

- [x] 4.1 Add/update tests to verify presence and format of `stage_start`, `stage_end`, `progress`, and `run_end` stdout events.
- [x] 4.2 Run `pytest` and confirm no regressions in conversion behavior and output artifacts.
- [x] 4.3 Run a real conversion smoke test and validate that agent-relevant status/duration fields are visible in stdout throughout execution.
