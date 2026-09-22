# Radio: TX16S layout

The fleet's one transmitter and the switch layout every model follows. Purchase and link
type: [`README.md`](README.md) (RC link row). Per-aircraft receiver: each aircraft's
`docs/bom.md`.

## Hardware

- **RadioMaster TX16S MKII MAX**, internal ExpressLRS module, **ELRS 3.3.0** (read from
  the ExpressLRS Lua script 2026-09-22). EdgeTX **2.11.2** (`RADIO/radio.yml`), SD card
  contents version 2.11. Stick mode 2.
- **Owner modifications** (owner, 2026-09-22):
  - **SH** swapped from the stock momentary push button to a 2-position lever switch.
    **SF** likewise, the owner believes; unconfirmed. EdgeTX configures both as `2pos`.
  - The optional **rear-case push switch** fitted, push to make, release to break. It is
    most likely EdgeTX's `SI` (type `toggle`); not confirmed.
  - An **Arduino inside the case**, the transmitter half of a head tracker. Model,
    wiring and which channels it drives: TBC.
- EdgeTX switch types (`radio.yml`, read 2026-09-22): SA, SB, SC, SD, SE, SG `3pos`;
  SF, SH `2pos`; SI `toggle`.
- The receivers bind by a binding phrase the owner used for every ELRS receiver; the
  phrase itself is not recorded (and would not be, in a public repo). A receiver can be
  bound without it: the transmitter's Bind sends the phrase-derived UID. Bee35 binding
  notes: [`aircraft/bee35/docs/bom.md`](../aircraft/bee35/docs/bom.md) (RX row).

## Channel layout

Read from the model files on the SD card 2026-09-22. `MODELS/model6.yml` ("TBS 5 inch")
and `model8.yml` ("Bee35") are identical but for name and receiver ID; Bee35 was made as
a copy of the 5". Internal module, CRSF, 16 channels, failsafe not set in EdgeTX
(ExpressLRS stops sending on link loss and the flight controller's failsafe acts).

| Ch | Source | EdgeTX mix name | Betaflight (5") | ArduPilot (Bee35) |
|---|---|---|---|---|
| 1 | Aileron stick | — | Roll | Roll (default `RCMAP`) |
| 2 | Elevator stick | — | Pitch | Pitch |
| 3 | Throttle stick | — | Throttle | Throttle |
| 4 | Rudder stick | — | Yaw | Yaw |
| 5 | SH | Arm | Arm | Arm/disarm (`RC5_OPTION` 153) |
| 6 | SB | Mode | Mode | Flight modes (`FLTMODE_CH` 6): back Stabilize, middle AltHold, toward Loiter |
| 7 | SF | Flip | Flip over after crash (turtle) | RTL (`RC7_OPTION` 4) |
| 8 | SI | Beep | Beeper | Lost-copter sound (`RC8_OPTION` 30), through the motors |

Every switch back (away from the pilot) is the safe pre-flight state on every model
([F-DEC-05](decisions.md)); on the Bee35 each channel reads low (~1000) there (checked
2026-09-22). ArduPilot values set on the Bee35:
[`aircraft/bee35/config/diff/2026-09-22-radio.txt`](../aircraft/bee35/config/diff/2026-09-22-radio.txt).
Pitch reads high with the stick forward, as EdgeTX sends it; ArduPilot reverses it
(`RC2_REVERSED` 1) rather than the transmitter, so the Bee35 model stays identical to the
5"'s (Betaflight needs no reversal).

Unassigned: SA, SC, SD, SE, SG. ExpressLRS treats channel 5 as the arm channel, so arm
stays on SH/channel 5 on every model.

**Bee35 model telemetry** (2026-09-22): sensors discovered from ArduPilot's CRSF
telemetry; top-bar widgets show `RQly`, `Sats`, `FM` and `Yaw`. First readings, on USB
power at the bench: RQly 100 %, Sats 20, FM STAB. From here on the Bee35 model differs
from the 5"'s in its telemetry sensors and screen layout; channels and mixes are
unchanged.

The fixed-wing models (Tasman, Swordfish, Avanti, OTTER) have not been read.
