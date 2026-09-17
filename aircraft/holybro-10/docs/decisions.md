# Decisions

Unresolved items live in [`open-questions.md`](open-questions.md). Format:
`DEC-nn — decision (date)`.

- **DEC-01 — Flight controller: Matek H743 Wing V3** (2026-09-17, owner). The owner is
  sure this board was bought for this airframe, as the more capable of the flight
  controllers in hand, to pair with an onboard companion computer. The invoices agree: it
  was ordered three days after the frame, with an optical flow sensor, and the CAN nodes
  bought five weeks later need its CAN port. Alternatives in hand, not chosen: a Matek
  F405 Wing V2 (unused) and a SpeedyBee F405 (used), both listed in
  [`../../../fleet/README.md`](../../../fleet/README.md).
  - **Outputs:** a wing board suits a quad. ArduPilot's
    [MatekH743 page](https://ardupilot.org/copter/docs/common-matekh743-wing.html) lists 13
    outputs, all PWM and DShot capable, and a CAN port. The board's two ESC positions are
    power pads for a twin-motor plane, not a limit on motor outputs.
  - **Firmware:** not flashed. The family rule needs two-way MAVLink, so ArduPilot rather
    than iNav ([wk-robotics `docs/common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#aircraft-and-the-tiers)).
