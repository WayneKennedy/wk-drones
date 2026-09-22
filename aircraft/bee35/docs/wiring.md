# Wiring

Port map, solder notes and jumper settings. **Planned, untested:** the map below is
taken from the board's published definitions (ArduPilot hwdef and README for
`MicoAir743v2`, MicoAir's port diagram in the same hwdef folder, iNav target
`MICOAIR743V2`; read 2026-09-19). Confirm each against the hardware as it is wired.
**Verified so far:** the GPS row and its compass (2026-09-22, below); every other row is
untested.
Firmware is ArduPilot ([DEC-08](decisions.md)); parameters in
[`setup-ardupilot.md`](setup-ardupilot.md).

## Port map

Each peripheral goes on the board plug built for it, and each is the board's default
role for that UART in ArduPilot. iNav's target defaults match for UART2/3/6/7/8, so
the same wiring would serve either firmware.

| Peripheral | Protocol | FC port (plug) | ArduPilot | Notes |
|---|---|---|---|---|
| RadioMaster RP3 V2 | CRSF | UART6 (SBUS/CRSF plug: GND 5V TX6 RX6) | SERIAL6, RCIN (default) | CRSF needs both TX6 and RX6 |
| Flywoo GM10 Mini V3 (GPS) | UBX | UART3 (GPS plug: GND 5V TX3 RX3 SCL SDA) | SERIAL3, GPS (default) | |
| Flywoo GM10 Mini V3 (compass) | I2C | I2C1, same GPS plug | Probed as external | QMC5883L. The FC's own QMC5883L is on I2C2 and is disabled, see [`setup-ardupilot.md`](setup-ardupilot.md). I2C1 is also on its own 4-pin plug on the board's underside (SDA1, SCL1, 5V, GND; MicoAir diagram) |
| MicoAir MTF-01P | MAVLink ("mav-apm") | UART4 (UART4 plug: GND 5V TX4 RX4) | SERIAL4, set to MAVLink1 | Default there is MAVLink2; parameters in the setup doc. UART1 is kept free, below |
| Walksnail Avatar VTX | MSP DisplayPort | UART2 (HD VTX plug) | SERIAL2, DisplayPort (default) | See the VTX plug notes below |
| ESC telemetry | ESC serial | UART7, RX only (RX7 pin on the ESC plug) | SERIAL7, ESC telemetry (default) | Part of the stack harness |
| On-board Bluetooth | MAVLink2 115200 | UART8, internal | SERIAL8 (default) | Field configuration link |
| Camera tilt servo (optional) | PWM | S5 (8-pin M5–M10 plug) | Servo mount | S5/S6 are timer group TIM3, separate from motors S1–4 (TIM1), so PWM on S5 alongside DShot motors is supported |
| — spare — | | UART1 (TELEM1), UART5 | | UART1 kept for a telemetry radio if [OQ-02](open-questions.md) ever takes option 2 |

### HD VTX plug (SH1.0 6-pin)

MicoAir's diagram: **12V, GND, TX2, RX2, GND, RX6.**

- **The Walksnail lead is 4-pin** in the same order as the first four DJI wires, so it
  plugs into socket pins 1–4 and pins 5–6 stay open (owner, 2026-09-22). That leaves
  pin 6 (RX6) unconnected, as it must be: it is the same UART6 input the CRSF receiver
  uses, and a DJI-style harness with the SBUS wire fitted would fight the receiver.
- **Pin 1 voltage is unconfirmed:** MicoAir's diagram says 12 V (the board's 12 V 3 A
  BEC); ArduPilot's README says 9 V. Either is inside the **Mini VTX V3's 3.1–13 V
  input** ([Caddx](https://www.caddxfpv.com/products/walksnail-avatar-hd-mini-vtx-v3),
  read 2026-09-19). 12 V leaves 1 V of margin. **Not measured:** the VTX
  was plugged in from the first battery power-up (2026-09-22), and the owner accepts
  either value since both are inside the VTX's input range; the SH1.0 pins are too fine
  for the owner's meter. Never power the VTX from 4S VBAT (up to 16.8 V). The Nano
  Camera V3 is powered through the VTX.

## Solder notes

- **Interim M10Q-5883 harness (made 2026-09-22, working on USB power the same day):**
  the M10Q's own 6-wire lead does not mate with the FC's GPS plug, so a 6-wire lead that mates with the
  FC's GPS socket is spliced 6-to-6 to the M10Q's lead, which keeps its GPS-end
  connector (owner). All six signals go through the GPS socket; the I2C1 plug is unused.
  Wired by the silkscreen labels at both ends, not by colour or position: GPS TX → RX3,
  GPS RX → TX3, 5V, GND; SDA → SDA, SCL → SCL (I2C is a shared bus, not crossed).
  Checked 2026-09-22 with the FC on USB power only (no battery), read over MAVLink:
  GPS on SERIAL3 (`SERIAL3_PROTOCOL` 5, 230400) had a 3D fix, 6 satellites, indoors; two
  QMC5883L compasses were found, both at address 0x0D (`COMPASS_DEV_ID` I2C bus 1,
  `COMPASS_DEV_ID2` I2C bus 0). The board carries only one, so the GPS unit's compass
  answers over the socket's SDA and SCL. Compass 1 is flagged external (`COMPASS_EXTERNAL`
  1) and has first priority. Not yet checked by rotating the GPS unit on its own to
  confirm it is compass 1.

- **Motor phase wires are soldered directly to the ESC pads; the FC–ESC link is the
  stack's supplied 8-pin harness, plug to plug** (owner, photos 2026-09-22). Motor test
  the same day: FC outputs S1–S4 drive rear right, front right, rear left, front left
  (Betaflight order), handled by `FRAME_TYPE` 12; see
  [`setup-ardupilot.md`](setup-ardupilot.md) checklist step 2.

TBC. Record pad locations, wire gauges, and anything non-obvious about the physical
build here as it is done.

## Jumper settings

TBC. The MTF-01P's output protocol: MicoAir's ArduPilot page sets it to "mav-apm" in
MicoAssistant. An earlier note here said a solder jumper sets MSP mode; which applies
to the -01P is unverified. Record the actual state here.

## Power

XT60 pigtail and 35 V 470–1000 µF low-ESR capacitor on the ESC input. Check the
stack box contents before ordering.

**First battery power-up, 2026-09-22 (owner):** through a smoke stopper, with the FC
also on USB. ESC start-up tones were normal, then silent (armed on DShot); nothing
tripped. The smoke stopper was then removed.
