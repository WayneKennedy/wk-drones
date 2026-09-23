# Wiring

Port map, solder notes and jumper settings for the Matek H743-WING V3
([DEC-01](decisions.md)) in the X500 V2 airframe. **Nothing here is wired yet**
(2026-09-23); the board is in hand and unused. Board geometry and how its three-board
stack is joined: [`../print/sources.md`](../print/sources.md). Firmware: none flashed,
ArduPilot implied.

## Port map

| Peripheral | Protocol | FC pads/port | Status |
|---|---|---|---|
| 4 × BLHeli_S 20 A ESC, signal | PWM or DShot, TBC | **S3–S6 planned** (signal + G only), needs `SERVO3_FUNCTION` 33 … `SERVO6_FUNCTION` 36 | Headers to solder, below |
| ESC power | — | Not on the FC. Each ESC takes XT30 from the frame's distribution board ([`bom.md`](bom.md)) | As shipped, ARTF |
| FC power | — | PD/ESC plate + and − pads, from the frame's distribution board | TBC |
| Receiver (ELRS, not chosen) | CRSF | **SERIAL6** = UART4, pads `Tx4`/`Rx4`; `SERIAL6_PROTOCOL` 23 | Planned. Receiver not chosen ([F-OQ-01](../../../fleet/open-questions.md)) |
| GPS/compass, Matek M10Q-5883 | UBX + I²C compass | **SERIAL3** = USART2, pads `Tx2`/`Rx2` (GPS1 default, no change); compass on I2C1 or I2C2, TBC | One unit fitted to the airframe (owner, 2026-09-19); wiring TBC, and whether a second unit joins it is open ([OQ-01](open-questions.md)) |
| Rangefinder, Benewake TFmini Plus (I²C) | I²C | TBC — I2C1 or I2C2, shared with the compass | In hand, not fitted. Downward-facing ([`bom.md`](bom.md)) |
| Companion computer (Pi or Jetson) | MAVLink over a 3.3 V UART | **SERIAL1** proposed = UART7, pads `Tx7`/`Rx7` (+ `Cts7`/`Rts7` for flow control); Telem1 default | Proposal only; port, baud and UART-or-USB stay open ([OQ-02](open-questions.md)) |
| Video, Walksnail Avatar HD Pro Micro Kit | MSP DisplayPort | **SERIAL2** = USART1, pads `Tx1`/`Rx1`; `SERIAL2_PROTOCOL` 42, `OSD_TYPE` 5. Power from the `9V` and `G` pads | Kit to be moved from the Swordfish ([DEC-04](decisions.md)) |

The H743's own ESC power pads are unused: one ESC per motor, each powered from the
distribution board ([`bom.md`](bom.md)).

### UART allocation follows the Bee35 (owner, 2026-09-23)

Same role, same SERIAL number on both aircraft, so one map serves the fleet. ArduPilot's
SERIAL numbers are **not** the board's silkscreen numbers: hwdef `MatekH743` gives
`SERIAL_ORDER OTG1 UART7 USART1 USART2 USART3 UART8 UART4 USART6` (read 2026-09-23), so
SERIAL1 = `Tx7/Rx7`, SERIAL2 = `Tx1/Rx1`, SERIAL3 = `Tx2/Rx2`, SERIAL4 = `Tx3/Rx3`,
SERIAL5 = `Tx8/Rx8`, SERIAL6 = `Tx4/Rx4`, SERIAL7 = `Tx6/Rx6`.

| Role | Bee35 | Here |
|---|---|---|
| GPS | SERIAL3 | SERIAL3, unchanged |
| Video, DisplayPort | SERIAL2 | SERIAL2 |
| RC | SERIAL6 | SERIAL6 |
| Off-board link | SERIAL1, kept spare | SERIAL1, companion computer |
| Flow sensor | SERIAL4 | n/a — the TFmini Plus is I²C |
| ESC telemetry | SERIAL7 | n/a — the ESC leads are ground and signal only |
| Bluetooth | SERIAL8 | n/a — this board has no SERIAL8 |

- **Do not use the `Rx6` pad for an ELRS receiver.** It is timer-mapped for PPM/SBUS and
  cannot carry CRSF or SRXL2 unless `BRD_ALT_CONFIG` 1 remaps it as SERIAL7's RX, which
  costs PPM. SERIAL7 is TX-only in the default config for the same reason. CRSF on
  SERIAL6 avoids all of it and keeps the Bee35's number.
- **Spare:** SERIAL4 (`Tx3`/`Rx3`), which is the GPS2 default and so suits a second GPS
  ([OQ-01](open-questions.md)) with no parameter change, and SERIAL5 (`Tx8`/`Rx8`).

## Solder notes

- **ESC signal leads carry ground and signal only, no +ve** (owner, 2026-09-23). So the
  FC feeds four signal lines and a common ground, and nothing back-feeds the servo rail.
- **Pin headers are to be soldered by the owner.** The board ships with bare pads. Pad
  layout (owner photo, 2026-09-23): **S2–S10 form one bank** of three rows — `Sn` on top,
  `Vx` in the middle, `G` at the bottom, nine columns. **S1 is separate**, on its own tab
  at the left edge with its own `Vx` and `G`. S11, S12, LED and 5V are on the right edge
  beside the UART pad field. Two-wire ESC leads need the `Sn` and `G` of a column only;
  **leave `Vx` unconnected** at the ESC end — it is the board's 5/6/7.2 V servo BEC.
- **Headers: right-angle, all three rows across S2–S10** (owner, 2026-09-23, in hand, not
  yet soldered). 27 pins. `Vx` is populated **for flexibility of what can plug in later**,
  not because the ESCs use it. **Clearance confirmed** (owner photo, 2026-09-23, board on
  the rev C deck on the frame plate): the pins exit sideways, clear of the TPU platform
  that covers the board's underside ([DEC-02](decisions.md)). S1's tab and the right-edge
  pads are unpopulated; how the receiver, GPS, rangefinder and companion link connect is
  [OQ-10](open-questions.md).
- **Two JST-GH harnesses on the top edge, as supplied** (owner photo, 2026-09-23): one to
  the USB-C/DFU/buzzer extender board, one CAN (`G`, `CAN-L`, `CAN-H`, `4V5`).
- **Motors on S3–S6, planned, not soldered.** ArduPilot's output groups on this board are
  `1/2`, `3/4/5/6`, `7/8/9/10`, `11/12`, `13`; every output in a group must run the same
  protocol, so DShot on one means DShot on all
  ([MatekH743 page](https://ardupilot.org/copter/docs/common-matekh743-wing.html), read
  2026-09-23). **S3–S6 puts all four motors in one group**, contiguous in the S2–S10 bank,
  and the bidirectional-DShot pairs (`3-4`, `5-6`; only outputs 1–8 are capable) fall
  inside it. Cost: ArduPilot expects motors on outputs 1–4, so set `SERVO3_FUNCTION` 33
  (Motor1) … `SERVO6_FUNCTION` 36 (Motor4) and leave `SERVO1/2_FUNCTION` 0. S1, S2 and
  S7–S12 stay free.
- **Vx is unused on this aircraft** unless something else needs it: the X500 V2 has no
  servos.

## Jumper settings

Three separate rails, often confused (Matek manual, read 2026-09-23): **5V** 2 A fixed;
**9V** 2 A for camera/VTX, raised to 12 V by the `9V→12V` solder jumper **on the main
board**; **Vx** 8 A for servos, 5 V default with 6 V and 7.2 V options, set by its own
jumper **on the PD/ESC base plate**. The main board's `9V→12V` jumper does not affect Vx.

- **Vx on this board is unverified** — 5 V is Matek's stated default, not a measurement.
  The `Vx` row is populated across the whole S2–S10 header, so **check it before anything
  is plugged into that row**: read which pads are bridged on the base plate, or measure Vx
  to ground with a battery connected (the BECs are dead on USB power alone).
- `9V→12V`: TBC with the video system.

## Power

TBC: battery not chosen ([`bom.md`](bom.md)). Battery and ESC power land on the PD/ESC
plate's + and − pads; the board takes 8–36 V DC (3–8S). Matek warns that the current
sensor is sensitive to ESC switching noise and ships a bypass capacitor
(ArduPilot [MatekH743 page](https://ardupilot.org/copter/docs/common-matekh743-wing.html),
read 2026-09-23).
