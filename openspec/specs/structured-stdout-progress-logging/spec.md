## Purpose

Define structured stdout runtime logging for stages, progress, and run summary.

## Requirements

### Requirement: Structured stdout events in key-value format

The converter SHALL emit runtime events to `stdout` in machine-parseable `key=value` format. Each log line SHALL include `event=<event_name>` and SHALL be flushed immediately.

#### Scenario: Stage start event is emitted
- **WHEN** converter starts any major pipeline stage
- **THEN** `stdout` contains a line with `event=stage_start`
- **THEN** the same line contains `stage=<stage_name>`

#### Scenario: Stage end event includes duration
- **WHEN** a major pipeline stage completes
- **THEN** `stdout` contains a line with `event=stage_end`
- **THEN** the same line contains `stage=<stage_name>` and `elapsed_sec=<number>`

### Requirement: Progress heartbeat for long conversion stages

During archive conversion loops, the converter SHALL periodically emit progress heartbeat events in `stdout` with status and duration metrics.

#### Scenario: Heartbeat includes progress metrics
- **WHEN** conversion of an archive is in progress and heartbeat threshold is reached
- **THEN** `stdout` contains a line with `event=progress`
- **THEN** the same line contains `stage=<convert_stage> done=<n> total=<N> pct=<number> elapsed_sec=<number> rate_fps=<number>`

#### Scenario: Heartbeat includes ETA when rate is known
- **WHEN** heartbeat is emitted and `done > 0` and `elapsed_sec > 0`
- **THEN** the same line contains `eta_sec=<number>`

### Requirement: Structured run summary in stdout

At the end of execution, the converter SHALL emit one final structured summary event in `stdout` containing top-level counters and total duration.

#### Scenario: Final summary is emitted on successful run
- **WHEN** conversion finishes without fatal startup errors
- **THEN** `stdout` contains a line with `event=run_end`
- **THEN** the same line contains `total`, `converted`, `failed`, `truncated`, `collisions`, `unresolved`, and `duration_sec`
