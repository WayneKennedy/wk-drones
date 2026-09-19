# 5" freestyle

The existing 5" freestyle quad, on a TBS Source One V5 frame, running Betaflight. It covers
the acro use case, which is why the Bee35 deliberately does not
([Bee35 README](../bee35/README.md)). Bee35 DEC-01 chose iNav partly for commonality with
this aircraft in the belief that it ran iNav; that premise was false, and the Bee35 now runs
ArduPilot ([Bee35 DEC-08](../bee35/docs/decisions.md)).

Not a wk-robotics robot: a human on the sticks ([F-DEC-01](../../fleet/decisions.md)).

## Status

**Flight ready.** Flown several times; last flown about a year before 2026-09-15 (owner's
account). Firmware confirmed as Betaflight by the owner in the SpeedyBee app, 2026-09-15.
Switching to iNav is open ([OQ-01](docs/open-questions.md)). Parts as ordered are in
[`docs/bom.md`](docs/bom.md). Not yet recorded: Betaflight
version and config, props, pack count and condition, and maintenance
history ([F-OQ-01](../../fleet/open-questions.md)).

## Idea, not a plan

The owner has floated fitting a small Raspberry Pi (a Zero 2 W or similar; which one is
unconfirmed) to this airframe. If it were wired to the flight controller as an intent
tier, the aircraft would cross the family's robot criterion. No decision has been taken,
nothing has been bought, and no payload or power budget has been done.

## Where things live

Follows the shape of [`../bee35/`](../bee35/README.md). Files are created when there is
content for them, not before.

- [`docs/bom.md`](docs/bom.md) — bill of materials, supplier, prices, order date
- [`docs/open-questions.md`](docs/open-questions.md) — pending decisions
