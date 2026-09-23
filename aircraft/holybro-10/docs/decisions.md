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
  print settings are in [`../print/sources.md`](../print/sources.md). **Rev A was printed
  in red PETG on 2026-09-18** and is superseded for the flying part by rev C,
  [DEC-03](#dec-03).
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
  - **Print material: TPU, settled by [DEC-03](#dec-03).** Rev A was modelled for a rigid
    print.
  - **Not decided by this:** which plate axis is forward ([OQ-06](open-questions.md)), and
    therefore the board's orientation and ArduPilot's `AHRS_ORIENTATION`.

<a id="dec-03"></a>
- **DEC-04 — Video: the Swordfish's Walksnail Pro Micro Kit moves here** (2026-09-23,
  owner). Resolves OQ-08. Exactly two Pro Micro Kits were ever bought and both were
  fitted: one to the 5", one to the [Swordfish](../../swordfish/README.md) canopy. The
  Swordfish's is redeployed — that aircraft is repaired but not commissioned, while this
  one is being built — so the 5" keeps its video and nothing is bought.
  - **Condition unassessed.** The kit took two hard crashes on the Swordfish and has never
    been tested since ([Swordfish `README.md`](../../swordfish/README.md)). Bench-test it
    before it is mounted.
  - **Wiring:** MSP DisplayPort on SERIAL2, power from the board's `9V` pads
    ([`wiring.md`](wiring.md)). The board's analog `VTx`, `C1`/`C2` pads and its AT7456E
    OSD go unused.
  - **Mounting is still open.** Not on the flight-controller deck — see the airframe notes
    under [OQ-06](open-questions.md) for the anchors that suit a bracket, and the camera
    waits on which edge is forward.

- **DEC-03 — The deck is rev C: the board on a floating TPU platform hung on four Z-flexure
  arms** (2026-09-21, owner; printed and checked 2026-09-22). Answers most of
  [OQ-07](open-questions.md). The part is
  [`../print/src/h743-deck-revc.py`](../print/src/h743-deck-revc.py), exported to
  [`../print/stl/`](../print/stl/); the owner-reviewed drawing is
  [`../print/h743-deck-revc-2d.png`](../print/h743-deck-revc-2d.png). **The drawing shows
  4.55 AF bores and 2.0 mm arms; the model's corrected values govern.**
  - **Shape.** Two anchor blocks on rev A's M3 anchors at (±13.5, ±43), each two Ø11 × 19.8 mm
    pillars joined by a 6 mm top bar. A 38 × 56 × 5 mm platform on the 30.5 FC pattern. Four
    Z-arms, 5 mm thick, turning corners so they bend in every axis. Footprint 97 × 56.
  - **Standoffs.** M3 × 20 brass hex, 4.55 AF, pressed straight through each pillar. The
    pillar is 0.2 mm shorter than the standoff, so the screws clamp brass and the TPU
    carries no preload. **Bore 4.85 AF — verified 2026-09-22**: the standoff pushes in by hand
    and needs pliers to remove (owner, one pillar tried).
  - **Arms drawn 1.9 mm to print 2.0.** A calibration coupon of the same TPU printed 2.0 mm
    walls at 2.10, and stiffness goes with width³. Not yet measured on the deck itself.
  - **Board fixing.** M2 through-bolt from below, through the platform and the stack, with a
    locknut on top. Fit of M2 in the Ø2.4 holes not yet reported.
  - **Material and print.** TPU 95A: Reprapper Silk TPU, yellow, batch 20260407S01. Printed
    upside down with no support, on 3d-printing's calibrated `tpu` profile, 3 h, 17 g; owner:
    "perfect". Allowances and evidence:
    [3d-printing `decisions.md`](https://github.com/WayneKennedy/3d-printing/blob/main/docs/decisions.md#materials).
  - **What it costs** (from the drawing). The platform covers the whole underside of the
    board, so its long axis is fixed fore-aft. The 14 AWG leads on the PD plate bypass the
    isolator unless given slack loops.
  - **Tuning is empirical.** The drawing's crude beam estimate is ~20–30 Hz vertical and
    ~35–40 Hz in-plane against the 25–40 Hz target, with printed-TPU modulus uncertain. The
    flight FFT decides; arm width (`ARM_W`) and thickness (`PLAT_T`) are the parameters.
