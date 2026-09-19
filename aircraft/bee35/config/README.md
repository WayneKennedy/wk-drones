# Config

ArduPilot parameter snapshots ([DEC-08](../docs/decisions.md)). These are the source of
truth for the aircraft's configuration.

- `diff/` — the parameters changed from the firmware defaults, one file per dated
  revision, named `YYYY-MM-DD-description.txt`. Each has a matching line in
  [`../docs/tuning.md`](../docs/tuning.md).
- `dump/` — the full parameter file saved from the ground station, for complete
  restoration.

Each file records the ArduCopter version and board (`MicoAir743v2`) in its first lines.

## Restoring onto replacement hardware

TBC until first tested. Intended procedure:

1. Flash the ArduCopter version recorded in the snapshot, board `MicoAir743v2`.
2. Load the latest `dump/` file from the ground station, write, reboot.
3. Re-verify against [`../docs/setup-ardupilot.md`](../docs/setup-ardupilot.md): sensor
   orientation, compass and accelerometer calibration, receiver failsafe, motor
   direction. Calibration values do not transfer between boards.
4. Bench check with props off before flying.
