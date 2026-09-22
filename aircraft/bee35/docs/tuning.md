# Tuning

PID and filter changes, one entry per change, with rationale. Every entry
corresponds to a file in [`../config/diff/`](../config/diff/) named
`YYYY-MM-DD-description.txt`.

Untested configs must be marked as such.

## Log

| Date | Diff file | What changed | Why | Tested |
|---|---|---|---|---|
| 2026-09-22 | [`2026-09-22-frame-motors.txt`](../config/diff/2026-09-22-frame-motors.txt) | Board orientation Roll180; Quad BetaFlightX; DShot600; S1 and S4 reversed | Inverted FC; motor order as wired; ESCs all spun one way | Bench (motor test, props off); not flown |
| 2026-09-22 | [`2026-09-22-battery.txt`](../config/diff/2026-09-22-battery.txt) | Li-Ion low/critical voltages and failsafe actions; capacity 4500; `BATT_VOLT_MULT` 21.21 | P45B packs, not LiPo defaults; FC read 0.4% low against a meter | Voltage reading bench-checked; failsafes untested; not flown |
| 2026-09-22 | [`2026-09-22-radio.txt`](../config/diff/2026-09-22-radio.txt) | Flight modes on SB; arm on SH, RTL on SF, lost-copter sound on SI; DShot beeper; RSSI from CRSF; radio calibration, roll un-reversed | Fleet switch layout ([`fleet/radio.md`](../../../fleet/radio.md)); arm must stay on channel 5 for ExpressLRS | Bench, disarmed: switches, stick directions, RC-loss detection; RTL failsafe not tested armed; not flown |
