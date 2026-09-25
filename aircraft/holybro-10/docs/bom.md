# Bill of materials

As ordered, per the supplier invoices in the owner's mailbox, read 2026-09-17 (how:
[wk-robotics `AGENTS.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/AGENTS.md#invoices-and-order-history)).
Prices are line totals inc VAT. Nothing here has been checked against the hardware.
Assignment of a part to this aircraft is the owner's recollection on 2026-09-17 unless
the row says otherwise; the reasoning is in [`decisions.md`](decisions.md) and
[`open-questions.md`](open-questions.md).

| Item | Part | Notes | Source | Price | Ordered |
|---|---|---|---|---|---|
| Frame kit | Holybro X500 V2 Frame Kit, ARTF | 500 mm wheelbase. Kit contents below | Flying Tech #83693 | £247.90 | 2025-07-24 |
| Camera mount | Holybro Depth Camera Mount for Intel RealSense | | Flying Tech #83693 | £12.90 | 2025-07-24 |
| Landing gear | Holybro X500 V2 Landing Gear Reinforcement Brace | | Flying Tech #83693 | £6.90 | 2025-07-24 |
| Flight controller | Matek H743 Wing V3 | [DEC-01](decisions.md). In hand, unused (owner, 2026-09-17) | HobbyRC #302285 | £96.30 | 2025-07-27 |
| Flow/lidar | Matek Optical Flow & Lidar Sensor | Exact model not on the invoice; same order as the flight controller | HobbyRC #302285 | £23.26 | 2025-07-27 |
| GPS/compass 1 | Matek M10Q-5883 | [OQ-01](open-questions.md). **One M10Q-5883 is fitted to the airframe** (owner, 2026-09-19); which of the two invoiced units it is cannot be told apart | HobbyRC #301738 | £31.80 | 2025-07-22 |
| GPS/compass 2 | Matek M10Q-5883 | [OQ-01](open-questions.md). Ordered with the F405 Wing V2 now assigned to the [Phoenix](../../phoenix/docs/decisions.md) | HobbyRC #303459 | £31.80 | 2025-08-07 |
| Rangefinder | Benewake TFmini Plus lidar, I²C version, 12 m, IP65 | **Confirmed by the owner 2026-09-19: bought for this aircraft, downward-facing, for accurate height on landing.** In hand: found 2026-09-19 (owner); the only Benewake purchase on invoice (ArduPilot `RNGFND1_TYPE` 25, TFminiPlus-I2C; `RNGFND1_ORIENT` 25 down). Not an obstacle sensor in that role — see OQ-09 | 3DXR #32525 | £50.00 | 2025-08-15 |
| Optical flow | MicoAir MTF-01P, flow + 12 m ToF | Fleet standard for every multirotor ([F-DEC-07](../../../fleet/decisions.md)). **On order**, due 2026-09-28. Downward-facing; mounting not designed. Duplicates the TFmini Plus's ToF — the TFmini stays, and which one is `RNGFND1` is unsettled | Unmanned Tech #19494 | £22.99 | 2026-09-25 |
| GPS mast | Holybro 29 mm fixed carbon GPS stand, 100 mm tube | | 3DXR #32525 | £11.50 | 2025-08-15 |
| CAN adapters | 2× Matek AP_Periph CAN Node L431 | £16.00 each. [OQ-01](open-questions.md) | 3DXR #32918 | £32.00 | 2025-09-01 |
| Companion computer | TBC | Raspberry Pi or Jetson Orin Nano; [OQ-03](open-questions.md) | TBC | TBC | TBC |
| RX | TBC | No receiver found on a 2025 Holybro-period order. A Radiomaster RP3 V2 ELRS Diversity (HobbyRC #303808, 2025-08-11, £22.99) was bought with the Phoenix glider and is likely its receiver | TBC | TBC | TBC |
| Video | Walksnail Avatar HD Pro Micro Kit, 32 GB — **moved from the Swordfish** ([DEC-04](decisions.md), 2026-09-23) | Nothing bought: neither kit was free, so the Swordfish's is redeployed. **Condition unassessed** after that aircraft's two crashes; bench-test before mounting. Originally HobbyRC #231336 or #236190, 2023, £159.00 — which is unknown and immaterial ([fleet](../../../fleet/README.md#walksnail-kit-bought)) | — | — | — |
| Battery | TBC | Holybro recommends "4S 3000-5000mAh 20C+ with XT60 Lipo" and quotes ~18 min hover with no payload on 5000 mAh ([product page](https://holybro.com/products/x500-v2-kits), read 2026-09-17). Candidates already owned, none tested on this airframe: 2 × GNB 5500 mAh 4S 70C (XT90, HobbyRC 2023-07; aircraft unrecorded) and the fleet's 4S1P P45B Li-ion packs ([fleet](../../../fleet/README.md)) | TBC | TBC | TBC |

Order totals inc VAT and shipping: Flying Tech #83693 £273.60; HobbyRC #301738 £34.30,
#302285 £116.53, #303459 £218.06 (also holds fleet items, see
[`../../../fleet/README.md`](../../../fleet/README.md)); 3DXR #32525 £66.35, #32918 £34.69.
HobbyRC #302285 and #303459 each carry a 5% discount (−£5.98, −£11.17), which is why their
line totals exceed the order total; the line prices above are before it.

## ARTF kit contents

Per [Holybro's product page](https://holybro.com/products/x500-v2-kits) (read 2026-09-17),
the ARF kit ships with these preinstalled: 4× Holybro 2216 motors with XT30 plugs, 4×
BLHeli_S 20 A ESCs, a power distribution board (XT60 battery input, XT30 outputs to the
ESCs and peripherals), and 6× 1045 propellers. No flight controller, GPS, receiver,
telemetry radio or battery. **Motor KV: taken as 880** (owner, 2026-09-17): the motor cases carry no markings, so the seller's listing is accepted as accurate. Flying Tech, the seller, lists
the X500 V2 ARF Kit (SKU30125) with "Holybro 2216 KV880" motors (owner's screenshot of the
listing, 2026-09-17); Holybro's own page lists KV920; the order emails give none. Both
listings were read in 2026-09, not at the 2025-07-24 purchase. Holybro's recommended
battery is the same 4S either way.

Frame per the same Flying Tech listing: 500 mm wheelbase, 16 × 16 mm motor mount pattern,
144 × 144 mm body plates 2 mm thick with 28 mm between them, 215 mm landing gear, 610 g.
Not measured here. Plate dimensions and the full hole map, taken from Holybro's own STEP
file rather than the listing, are in [`../print/sources.md`](../print/sources.md): the
plates are 143.72 mm square, the 28 mm gap is confirmed, and the flight-controller
patterns are on the lower plate, not the upper one.

One ESC per motor, each powered from the distribution board, so the flight controller
supplies four signal lines only. The H743 Wing V3's own ESC power pads are not needed.
