# Holybro 10"

A Holybro X500 V2 (500 mm wheelbase, 10" props), **bought specifically to carry a Raspberry Pi or
Jetson hard-wired to its flight controller.** That makes it the fleet's only candidate
for a wk-robotics aerial robot ([F-DEC-01](../../fleet/decisions.md)), and the only
aircraft the [wk-robotics index](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/projects.md)
lists as a project.

## Status

**Parts identified from invoices 2026-09-17; build state unknown.** Frame kit bought
2025-07-24; flight controller is a Matek H743 Wing V3, in hand and unused
([DEC-01](docs/decisions.md)). Parts as ordered are in [`docs/bom.md`](docs/bom.md).
Nothing is flashed; the family rule implies ArduPilot. Open: the two-GPS plan, the
companion link wiring, Pi or Jetson, and everything about build state, receiver, video
and battery ([`docs/open-questions.md`](docs/open-questions.md)). Nothing has been
checked against the hardware.

## Role in the family

Onboard-intent topology: the companion computer is the intent tier, the flight controller
the reflex tier, wired together. See wk-robotics
[`docs/common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#aircraft-and-the-tiers)
for what that permits, and the same document's compute pattern for the tiers themselves.
How it joins the family's topic contract is unrecorded.

## Where things live

Follows the shape of [`../bee35/`](../bee35/README.md). Files are created when there is
content for them, not before.

- [`docs/bom.md`](docs/bom.md) — bill of materials, suppliers, prices, order dates
- [`docs/decisions.md`](docs/decisions.md) — decisions (`DEC-nn`)
- [`docs/open-questions.md`](docs/open-questions.md) — pending decisions (`OQ-nn`)
