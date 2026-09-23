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
| Receiver | TBC | TBC | Not chosen ([F-OQ-01](../../../fleet/open-questions.md)) |
| GPS/compass, Matek M10Q-5883 | UBX + I²C compass | TBC — a UART for the GPS, I2C1 or I2C2 for the compass | One unit fitted to the airframe (owner, 2026-09-19); wiring TBC, and whether a second unit joins it is open ([OQ-01](open-questions.md)) |
| Rangefinder, Benewake TFmini Plus (I²C) | I²C | TBC — I2C1 or I2C2, shared with the compass | In hand, not fitted. Downward-facing ([`bom.md`](bom.md)) |
| Companion computer (Pi or Jetson) | MAVLink over a 3.3 V UART | Which H743 UART: open ([OQ-02](open-questions.md)) | Open |
| Video | TBC | TBC | Not chosen |

The H743's own ESC power pads are unused: one ESC per motor, each powered from the
distribution board ([`bom.md`](bom.md)).

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
