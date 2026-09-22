# Tuning

PID and filter changes, one entry per change, with rationale. Every entry
corresponds to a file in [`../config/diff/`](../config/diff/) named
`YYYY-MM-DD-description.txt`.

Untested configs must be marked as such.

## Log

| Date | Diff file | What changed | Why | Tested |
|---|---|---|---|---|
| 2026-09-22 | [`2026-09-22-frame-motors.txt`](../config/diff/2026-09-22-frame-motors.txt) | Board orientation Roll180; Quad BetaFlightX; DShot600; S1 and S4 reversed | Inverted FC; motor order as wired; ESCs all spun one way | Bench (motor test, props off); not flown |
