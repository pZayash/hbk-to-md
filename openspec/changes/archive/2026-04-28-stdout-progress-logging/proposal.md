## Why

`convert.py` already prints a few high-level messages (`extract`, `convert`, `done`), but long runs still look opaque to agents and CI logs. During conversion of large `.hbk` archives, there is no structured visibility into current stage, intermediate progress, per-stage duration, or ETA-like signals. This makes it harder for automated agents to determine whether the process is healthy, slow, or stalled.

## What Changes

- Add structured `stdout` logs in `key=value` format for all major pipeline stages (start/end).
- Emit per-stage elapsed time on stage completion (seconds).
- Add periodic heartbeat/progress logs during long conversion loops (processed, total, percent, rate, elapsed, eta).
- Keep final summary line, but make it consistent with the same `key=value` style.
- Do not add JSON logging and do not introduce new output files for progress (`stdout` only).

## Capabilities

### New Capabilities

- `structured-stdout-progress-logging`: Emit machine-parseable stage/progress events in `key=value` form so agents can infer current state and duration of the running conversion.

### Modified Capabilities

- `hbk-to-md-converter`: Runtime observability improves from sparse human messages to structured progress/duration logging in `stdout`.

## Impact

- `convert.py`: Add a lightweight logging helper (event + `key=value` fields), instrument stage boundaries, and add periodic progress logs inside archive conversion loop(s).
- No changes to conversion output structure (`.md`, `_meta.json`, `_errors.log`, etc.).
- No new dependencies.
