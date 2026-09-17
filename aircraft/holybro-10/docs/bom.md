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
| GPS/compass 1 | Matek M10Q-5883 | [OQ-01](open-questions.md) | HobbyRC #301738 | £31.80 | 2025-07-22 |
| GPS/compass 2 | Matek M10Q-5883 | [OQ-01](open-questions.md). Ordered with the F405 Wing V2 now assigned to the [Phoenix](../../phoenix/docs/decisions.md) | HobbyRC #303459 | £31.80 | 2025-08-07 |
| Rangefinder | Benewake TFmini Plus lidar, I²C version, 12 m | Assignment to this aircraft not confirmed by the owner | 3DXR #32525 | £50.00 | 2025-08-15 |
| GPS mast | Holybro 29 mm fixed carbon GPS stand, 100 mm tube | | 3DXR #32525 | £11.50 | 2025-08-15 |
| CAN adapters | 2× Matek AP_Periph CAN Node L431 | £16.00 each. [OQ-01](open-questions.md) | 3DXR #32918 | £32.00 | 2025-09-01 |
| Companion computer | TBC | Raspberry Pi or Jetson Orin Nano; [OQ-03](open-questions.md) | TBC | TBC | TBC |
| RX | TBC | No receiver found on a 2025 Holybro-period order. A Radiomaster RP3 V2 ELRS Diversity (HobbyRC #303808, 2025-08-11, £22.99) was bought with the Phoenix glider and is likely its receiver | TBC | TBC | TBC |
| Video | TBC | None found in the mail, June–October 2025 | TBC | TBC | TBC |
| Battery | TBC | Holybro recommends 4S 3000–5000 mAh, XT60; nothing on these invoices | TBC | TBC | TBC |

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
telemetry radio or battery. **Motor KV: likely 880, TBC.** Flying Tech, the seller, lists
the X500 V2 ARF Kit (SKU30125) with "Holybro 2216 KV880" motors (owner's screenshot of the
listing, 2026-09-17); Holybro's own page lists KV920; the order emails give none. Both
listings were read in 2026-09, not at the 2025-07-24 purchase, so confirm on a motor label.

Frame per the same Flying Tech listing: 500 mm wheelbase, 16 × 16 mm motor mount pattern,
144 × 144 mm body plates 2 mm thick with 28 mm between them, 215 mm landing gear, 610 g.
Not measured here.

One ESC per motor, each powered from the distribution board, so the flight controller
supplies four signal lines only. The H743 Wing V3's own ESC power pads are not needed.
