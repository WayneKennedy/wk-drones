# ArduPilot setup

First flash through maiden, per [DEC-08](decisions.md). Checklist steps are stubs until
hardware is in hand; the settings below are the target configuration. Port map:
[`wiring.md`](wiring.md). Nothing here is tested on this airframe yet.

## Firmware and tools

- **ArduCopter, board `MicoAir743v2`.** Copter stable for this board is 4.7.1
  (firmware.ardupilot.org, checked 2026-09-19). The board shipped with ArduCopter 4.6.2
  (git `1ebd4d99`, read over MAVLink 2026-09-22); updated to 4.7.1 the same day.
- **A ground station is for setup only.** Mission Planner (Windows) or QGroundControl
  (Windows/macOS/Linux/Android/iOS) over USB on the bench; Linux install:
  [`fleet/ground-station.md`](../../../fleet/ground-station.md). The FC also has an on-board
  Bluetooth module on UART8 (MAVLink2, 115200; BOOT button toggles its power), for
  field changes without a cable; whether a phone GCS connects to it is unverified. In
  flight the aircraft needs only the radio and goggles. `FS_GCS_ENABLE` stays 0.
- Board defaults worth knowing (hwdef): motor order is Betaflight X (`HAL_FRAME_TYPE`
  12, "for BF migration"), though the fresh 4.7.1 flash read `FRAME_TYPE` 1, so set 12
  explicitly; battery monitor 4 with `BATT_VOLT_MULT` 21.12 and
  `BATT_AMP_PERVLT` 40.2; OSD_TYPE 1 (on-board analog chip).

## Settings of note

- **Mounting (owner, 2026-09-22): the frame inverts both the FC and the motors.** The FC
  is upside down (rolled 180°) with its arrow forward: `AHRS_ORIENTATION` 8 (Roll180),
  set before accelerometer calibration and checked by tilting the airframe against the
  GCS attitude display. **Set and checked 2026-09-22** (MAVLink Inspector, `ATTITUDE`):
  nose up gives positive pitch, right side down positive roll, nose right positive
  `yawspeed`. The `yaw` heading is not a valid check before compass calibration. The
  internal compass follows `AHRS_ORIENTATION`; the external (GPS) compass does not, and its orientation is found by compass calibration
  (`COMPASS_AUTO_ROT`). The motors hang below the arms and push. Motor spin direction in
  ArduPilot's frame diagrams is as seen from above the aircraft, so it is judged from
  above, looking at the underside of each motor.

- **Hands-off hold is the goal (DEC-08): fly in Loiter.** Sticks centred, it holds
  position and height. Flight-mode switch (`FLTMODE_CH`, 3 positions):
  **Loiter → AltHold → Stabilize**. Loiter is the normal mode; AltHold holds height
  only, for when GPS is poor; Stabilize is the manual last resort. **RTL on its own
  switch** (`RCx_OPTION` 4). Loiter will not arm without a good position estimate.
- **Compass: external primary; internal off unless CompassMot clears it.** The GPS
  unit's QMC5883L is on the GPS plug's I2C1 (probed as external); the board's own
  QMC5883L is on I2C2. ESC current on a 30.5 mm stack makes the onboard mag a liability
  for Loiter — standard practice, not measured here. Run **CompassMot** (compass-motor
  calibration) with both enabled; keep the internal one as a backup only if its
  interference is low, otherwise set its `COMPASS_USEn` to 0 (check which index it got). A high figure on the
  external one means it is mounted too close to the power wiring. Calibrate away from
  the bench.
- **GPS and optical flow as two EKF source sets** (ArduPilot optical flow setup page):
  - `EK3_SRC1_*` = GPS (defaults): the normal outdoor source.
  - `EK3_SRC2_VELXY` 5 (Optical Flow), `EK3_SRC2_POSXY` 0, `EK3_SRC2_POSZ` 1 (Baro),
    `EK3_SRC2_VELZ` 0, `EK3_SRC2_YAW` 1 (Compass): low, GPS-poor or indoor flight.
  - `EK3_SRC_OPTIONS` 0; switch sets with an aux channel, `RCx_OPTION` 90
    (EKF Pos Source).
  - With flow as the only horizontal source, Loiter is capped at `RNGFND1_MAX`.
- **MTF-01P** (MicoAir's ArduPilot page, written for the MTF-01; that it applies
  unchanged to the -01P is unverified):
  - Sensor set to **"mav-apm"** protocol in MicoAssistant, and its `mav_id` set to
    anything but 1 (ArduPilot 4.5+).
  - `SERIAL4_PROTOCOL` 1 (MAVLink1), `SERIAL4_BAUD` 115, `SERIAL4_OPTIONS` 1024
    (don't forward MAVLink).
  - `FLOW_TYPE` 5 (MAVLink), `RNGFND1_TYPE` 10 (MAVLink), `RNGFND1_ORIENT` 25 (down),
    `RNGFND1_MIN` 0.01. MicoAir gives `RNGFND1_MAX` 8 for the MTF-01; the -01P value
    is TBC.
  - Orientation: MicoAir's default is ArduPilot orientation; if mounted the iNav/FMT
    way, `FLOW_ORIENT_YAW` 18000. Wrong orientation causes a flyaway. Verify flow
    values move the right way before flight.
  - Calibrate in flight: `RCx_OPTION` 158 (Optflow Calibration), then rock in pitch
    and roll; this sets `FLOW_FXSCALER`/`FLOW_FYSCALER`.
- **Walksnail OSD** (ArduPilot DisplayPort page): `SERIAL2_PROTOCOL` 42 (the board
  default), `SERIAL2_BAUD` 115, `OSD_TYPE2` 5 per the board README (or `OSD_TYPE` 5 with
  no analog OSD), `MSP_OPTIONS` bit 0 clear. Font chosen in the goggle menu;
  `OSDn_TXT_RES` for HD layout.
- **Receiver:** CRSF on UART6 (`SERIAL6_PROTOCOL` 23, RCIN, the board default).
- **Battery: Li-Ion, 4S P45B.** Not LiPo defaults. Full 4.2 V/cell; `BATT_LOW_VOLT`
  13.2 (3.3 V/cell) with `BATT_FS_LOW_ACT` RTL; `BATT_CRT_VOLT` 12.0 (3.0 V/cell) with
  `BATT_FS_CRT_ACT` Land. `BATT_CAPACITY` 4500 (one 4S1P pack). `BATT_VOLT_MULT` 21.21,
  calibrated against a meter 2026-09-22 (board default 21.12 read 0.4% low).
- **Anti-crash features to enable:**
  - Radio failsafe `FS_THR_ENABLE` → RTL; verify by switching the transmitter off,
    props off.
  - Geofence: `FENCE_ENABLE` 1, altitude + circle, `FENCE_ACTION` RTL. `FENCE_ALT_MAX`,
    `FENCE_RADIUS` and `RTL_ALT` TBC per flying site.
  - EKF failsafe (`FS_EKF_ACTION`) and crash check (`FS_CRASH_CHECK`, disarms after a
    crash) at their defaults.
  - Surface tracking: with the downward rangefinder, AltHold and Loiter hold height
    above the ground below `RNGFND1_MAX`.
  - No obstacle avoidance: nothing looks forward. The duct cage is the protection.
- **Tune:** harmonic notch from ESC RPM needs bidirectional DShot (outputs 1–8 support
  it; whether the AM32 ESC has it enabled is TBC), then AutoTune. Record every change
  in [`tuning.md`](tuning.md).

## Checklist

Stub. Fill in as each step is done, in order.

1. Update to ArduCopter stable, `MicoAir743v2` — **done 2026-09-22:** 4.7.1, flashed from
   QGroundControl v5.1.4 (ArduPilot / ChibiOS / Multi-Rotor / "MicoAir H743 v2.0 - 4.7.1"),
   USB power only
2. Frame, orientation, DShot, motor order and direction, props off — **done 2026-09-22.**
   Quad (QGC Frame page), `AHRS_ORIENTATION` 8, `MOT_PWM_TYPE` 6 (DShot600). Motor test
   showed outputs S1–S4 = rear right, front right, rear left, front left (Betaflight
   order), all spinning the same way, so `FRAME_TYPE` 12 (BetaFlightX; set in Parameters,
   QGC's Frame page does not list it) and `SERVO_DSHOT_ESC` 1 with `SERVO_BLH_RVMASK` 9
   (reverse S1 and S4 by DShot command). Retest: A front right CCW, B rear right CW,
   C rear left CCW, D front left CW, viewed from above, as ArduPilot's BetaFlightX
   layout requires. B and D did not respond on the first attempt and did after the FC–ESC
   harness plug was pressed home; cause not established. QGC's "All" button spun one
   motor only; unexplained, not used
3. Ports per [`wiring.md`](wiring.md)
4. Receiver: CRSF, channel map, radio failsafe
5. GPS and external compass; calibrate compass and accelerometer — accelerometer
   **done 2026-09-22** (QGC, after `AHRS_ORIENTATION` was set); compass pending, to be
   done away from the bench
6. CompassMot, then keep or disable the internal compass on its result
7. MTF-01P: mav-apm mode, parameters above, verify live flow and range values
8. EKF source sets and their switch
9. Walksnail DisplayPort OSD
10. Battery: Li-Ion thresholds and failsafes; geofence; RTL altitude — battery part
    **set 2026-09-22** (values above; failsafe actions not yet tested); geofence and RTL
    altitude pending
11. Notch filter, then bench hover checks
12. Maiden in AltHold, then Loiter; AutoTune; then optical-flow calibration flight

## Optional: pitch-stabilised camera

Standard cinewhoop uptilt (~20°) exists to correct for nose-down forward flight and
is wrong for a machine that hovers level. Try low-tilt printed inserts (0/5/10°)
first. Loiter keeping the airframe level may remove the need entirely.

If a tilt axis is still wanted: an ArduPilot servo mount (`MNT1_TYPE` 1) on **S5**,
stabilised in pitch, with an aux channel for manual look-down. S5/S6 are their own
timer group (TIM3), separate from motors S1–4 (TIM1), so S5 can drive a PWM servo
while the motors run DShot (board README). S5 is on the 8-pin M5–M10 plug.

Do not buy SpeedyBee's 28 g "shock-absorbing gimbal" accessory expecting this. It
is passive damping only.
