# Wiring

Port map, solder notes and jumper settings for the Matek H743-WING V3
([DEC-01](decisions.md)) in the X500 V2 airframe. **Nothing here is wired yet**
(2026-09-23); the board is in hand and unused. Board geometry and how its three-board
stack is joined: [`../print/sources.md`](../print/sources.md). Firmware: none flashed,
ArduPilot implied.

## Port map

| Peripheral | Protocol | FC pads/port | Status |
|---|---|---|---|
| 4 × BLHeli_S 20 A ESC, signal | PWM or DShot, TBC | S1–S4 (signal + G only) | Headers to solder, below |
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
- **Pin headers are to be soldered by the owner.** The board ships with bare pads. On the
  H743-WING the outputs are grouped in threes — each `Sn` pad sits in a row with its own
  `G` and `Vx` (Matek layout page). Two-wire ESC leads need the `Sn` and `G` of each row
  only; **leave `Vx` unconnected**, it is the board's 5/6/7.2 V servo BEC. Which header
  type and how many rows: TBC as fitted.
- **Vx is unused on this aircraft** unless something else needs it: the X500 V2 has no
  servos.

## Jumper settings

TBC. `Vx` voltage (5 V default, 6 V or 7.2 V) is set by a jumper on the PD/ESC plate;
irrelevant while nothing uses Vx. The `9V→12V` jumper on the main board is for
camera/VTX, TBC with the video system.

## Power

TBC: battery not chosen ([`bom.md`](bom.md)). Battery and ESC power land on the PD/ESC
plate's + and − pads; the board takes 8–36 V DC (3–8S). Matek warns that the current
sensor is sensitive to ESC switching noise and ships a bypass capacitor
(ArduPilot [MatekH743 page](https://ardupilot.org/copter/docs/common-matekh743-wing.html),
read 2026-09-23).
