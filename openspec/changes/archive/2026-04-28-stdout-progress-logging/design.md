## Context

`convert.py` already prints a few human-readable messages (`extract ...`, `convert ...`, `done ...`) and writes final aggregate stats into `_meta.json`. For large conversions (tens of thousands of pages), these logs are insufficient for agents that need to infer runtime state from streaming `stdout`: current stage, whether forward progress is happening, and how long each stage takes.

The change must improve observability without altering output artifacts or adding dependencies. User requirement is explicit: logs in `stdout`, `key=value` format, no JSON.

## Goals / Non-Goals

**Goals:**
- Emit machine-parseable `stdout` events for stage start/end and progress heartbeats.
- Include stage duration and run-time progress metrics (`done`, `total`, `pct`, `rate`, `eta`).
- Keep logging overhead low and deterministic for long runs.
- Preserve existing conversion behavior and output files.

**Non-Goals:**
- No JSON/JSONL logging.
- No additional progress log files.
- No redesign of conversion pipeline stages themselves.
- No integration with external logging backends.

## Decisions

### 1) Unified event logger with stable `key=value` envelope

Add a tiny helper (e.g. `log_event(event: str, **fields)`) that prints:

`[hbk-to-md] event=<event> key1=value1 key2=value2 ...`

Rules:
- Always include `event`.
- Keep field keys stable and lowercase.
- Serialize values into single-token-safe strings (spaces replaced or quoted consistently).
- Always `flush=True` for real-time agent visibility.

Why: one formatting path prevents drift and makes regex parsing reliable.

Alternative considered: leaving ad-hoc `print(...)` lines. Rejected because field naming and ordering become inconsistent over time.

### 2) Stage boundary instrumentation in `main()`

Wrap major steps with explicit begin/end events:
- `extract_shcntx`, `scan_titles_shcntx`, `build_index_shcntx`
- `extract_shlang`, `scan_titles_shlang`, `build_index_shlang` (if `--lang-hbk`)
- `convert_shcntx`, `convert_shlang`
- `build_toc`, `inject_breadcrumbs`, `write_logs`

For each stage:
- `event=stage_start stage=<name>`
- `event=stage_end stage=<name> elapsed_sec=<...>`

Why: agents can infer current state even when heartbeat is quiet.

Alternative considered: only final summary duration. Rejected because long-running stages remain opaque.

### 3) Progress heartbeat inside archive conversion loop

In `_convert_archive()`, emit periodic progress events with configurable cadence (constant interval by processed count, e.g. every 500 files, plus final emission at stage end):
- `event=progress stage=<convert_*> done=<n> total=<N> pct=<...> elapsed_sec=<...> rate_fps=<...> eta_sec=<...>`

`total` is precomputed per archive by materializing `iter_html(extracted_dir)` once for counting and iteration reuse.

Why: this gives liveness + ETA without excessive log spam.

Alternative considered: time-based heartbeat every N seconds. Rejected for now due to extra clock checks and less predictable emission in fast/slow environments.

### 4) Final summary normalized to same schema

Replace free-form `done: total=... converted=...` with structured summary event:
- `event=run_end total=... converted=... failed=... truncated=... collisions=... unresolved=... index_files=... breadcrumbs=... duration_sec=...`

Why: one schema family across start/progress/end simplifies parser logic.

Alternative considered: keep legacy line unchanged. Rejected because mixed formats increase parser complexity.

## Risks / Trade-offs

- **Log verbosity on large runs** -> Too frequent heartbeats can bloat CI logs.  
  **Mitigation:** fixed sparse interval (e.g. 500) and only one forced final heartbeat.

- **Parsing ambiguity for values with spaces** -> Naive split-by-space parsers may break.  
  **Mitigation:** keep values normalized to no spaces for high-volume fields; for textual fields use deterministic quoting/escaping.

- **Slight runtime overhead** -> Extra calculations and prints in loop.  
  **Mitigation:** O(1) math per heartbeat only, not per file; coarse emission interval.

- **Stage naming drift in future edits** -> Inconsistent names break dashboards.  
  **Mitigation:** document canonical stage names in code constants and tests.

## Migration Plan

No data migration required. Change is runtime-observability only.

Rollout steps:
1. Implement logger helper and stage/progress instrumentation.
2. Update/add tests for log format and presence of required keys.
3. Run conversion smoke test on real `.hbk` and verify parsing with simple `rg` checks.

Rollback:
- Revert instrumentation commit if needed; conversion output remains unchanged either way.

## Open Questions

- Should heartbeat interval be CLI-configurable (`--progress-every`) or fixed constant initially?
- Should `eta_sec` be omitted when `rate_fps=0` or emitted as `-1`/`na`?
