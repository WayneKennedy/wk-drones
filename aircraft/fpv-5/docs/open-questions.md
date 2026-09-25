# Open questions

Pending decisions for the 5". Decisions, once taken, go in `decisions.md` as a DEC
(none yet). Format: `OQ-nn — question (date raised)`.

- **OQ-01 — Switch from Betaflight to iNav — when, and to iNav or ArduPilot?**
  (2026-09-15, owner; narrowed 2026-09-25). **Whether is settled:**
  [F-DEC-06](../../../fleet/decisions.md) puts every aircraft on ArduPilot or iNav and
  rules Betaflight out, so this aircraft converts. Open: **when**, and **which of the
  two**. The owner is open to it. On Betaflight the aircraft is very fast and position hold is poor ("a feather in a
  storm"); the owner puts much of that down to pilot skill and plans more simulator
  time. The firmware-commonality argument Bee35 DEC-01 made no longer applies: the Bee35 runs
  ArduPilot ([Bee35 DEC-08](../../bee35/docs/decisions.md), 2026-09-19).
  - **Firmware support:** iNav has a `SPEEDYBEEF405V3` target, in the iNav repo since
    2022-09 (checked 2026-09-15; latest release 9.1.0). Not flashed or tested on this
    board.
  - **The F405 all but settles "which of the two": iNav** (2026-09-25). ArduPilot does have
    a `speedybeef4v3` target, but the STM32F405's **1 MB flash** forces features out of the
    build, and its hwdef includes `minimize_fpv_osd.inc`, which sets
    **`AP_OPTICALFLOW_ENABLED 0`** — optical flow is **not compiled in** (ArduPilot master,
    read 2026-09-25). The MTF-01P bought for this aircraft under
    [F-DEC-07](../../../fleet/decisions.md) would therefore do nothing on stock ArduPilot.
    Also cut there: `HAL_GYROFFT_ENABLED 0` (no in-flight FFT for the harmonic notch),
    gimbal mount, camera backends, most GPS, battery and rangefinder backends. iNav on F405
    supports MSP flow natively and the MTF-01P speaks MSP. **Untested alternative:** a
    custom ArduPilot build with flow enabled (custom firmware server) — whether it fits in
    1 MB is unverified. The H743 boards the fleet uses elsewhere (480 MHz, 2 MB flash) have
    none of this constraint.
  - **Hardware gap:** no optical flow or lidar is fitted (owner, 2026-09-15), and the
    owner judges that additions are needed to get the best from iNav. A downward
    **MicoAir MTF-01P** is now the fleet standard for every multirotor
    ([F-DEC-07](../../../fleet/decisions.md)) and one must be bought for this aircraft. GPS is fitted
    (Walksnail WS-M181); whether it has a compass is TBC ([`bom.md`](bom.md)). What to
    add, where it mounts on the Source One V5, and which UART it takes are unassessed.
  - **Before any reflash:** save the Betaflight `diff all` and `dump all` to
    `../config/`, so the flying configuration can be restored.
