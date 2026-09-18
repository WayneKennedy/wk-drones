# Decisions

Unresolved items live in [`open-questions.md`](open-questions.md). Format:
`DEC-nn — decision (date)`.

- **DEC-01 — Flight controller: Matek H743 Wing V3** (2026-09-17, owner). The owner is
  sure this board was bought for this airframe, as the more capable of the flight
  controllers in hand, to pair with an onboard companion computer. The invoices agree: it
  was ordered three days after the frame, with an optical flow sensor, and the CAN nodes
  bought five weeks later need its CAN port. Alternatives in hand, not chosen: a Matek
  F405 Wing V2 (unused; since assigned to the Phoenix, its
  [DEC-01](../../phoenix/docs/decisions.md)) and a SpeedyBee F405 (used; since identified as the Swordfish's own board, see its
  page; formerly listed in
  [wk-inventory `docs/stock.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/docs/stock.md)).
  - **Outputs:** a wing board suits a quad. ArduPilot's
    [MatekH743 page](https://ardupilot.org/copter/docs/common-matekh743-wing.html) lists 13
    outputs, all PWM and DShot capable, and a CAN port. The board's two ESC positions are
    power pads for a twin-motor plane, not a limit on motor outputs.
  - **Firmware:** not flashed. The family rule needs two-way MAVLink, so ArduPilot rather
    than iNav ([wk-robotics `docs/common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#aircraft-and-the-tiers)).

- **DEC-02 — The flight controller mounts on a printed deck above the upper plate**
  (2026-09-17, owner). The owner wants the H743 fixed to an adapter and the adapter to the
  X500's upper plate, raised on a deck with room underneath, on Matek's own silicone
  grommets rather than a soft-mounted tray. The part is
  [`../print/src/h743-deck.py`](../print/src/h743-deck.py); its interfaces, hardware and
  print settings are in [`../print/sources.md`](../print/sources.md). **Designed only —
  not printed, and nothing has been offered up to the hardware.**
  - **Why a part is needed at all:** the X500 V2's 30.5 × 30.5 and 45 × 45 autopilot
    patterns are on the **lower** plate. The upper plate has nothing drilled inside
    |x| < 29, |y| < 21.5 (measured, [`../print/sources.md`](../print/sources.md)), so a
    board mounted there has to bridge out to the 4 × Ø3.4 holes at (±13.5, ±43) or the
    4 × Ø2.2 at (±29, ±21.5). The deck uses both.
  - **How the board is fixed** (owner, from the hardware, 2026-09-17). The grommets Matek
    supplies are not spare hardware: each wraps a brass standoff inside the board's own
    three-PCB stack, and the bottom PD/ESC plate screws up into those standoffs with M2
    countersunk. The deck therefore carries the board on longer M2 screws driven up into
    the same standoffs, clamping the PD plate between boss and standoff. Nothing threads
    into plastic. An earlier reading of the vendor STEP put a second mounting pattern at
    32 × 50 mm; there is no such pattern on the hardware.
  - **Not a grounding path, and it does not need to be** (owner). The board's four
    mounting holes are GND, but flight controllers are routinely fitted to non-metallic
    airframes, often on double-sided tape; ground reaches the board through its wiring.
  - **Print material is open.** Modelled and dimensioned for a rigid print; the owner is
    considering TPU for the final part, which would make the deck itself the isolator.
  - **Not decided by this:** which plate axis is forward ([OQ-06](open-questions.md)), and
    therefore the board's orientation and ArduPilot's `AHRS_ORIENTATION`.
