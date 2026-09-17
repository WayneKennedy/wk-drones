# Bill of materials

As ordered, per the supplier invoices in the owner's mailbox, read 2026-09-17 (how:
[wk-robotics `AGENTS.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/AGENTS.md#invoices-and-order-history)).
Prices are line totals inc VAT; no order had a discount. All orders below were delivered;
which parts are in hand now is not recorded beyond the [README](../README.md) status.

| Item | Part | Notes | Source | Price | Ordered |
|---|---|---|---|---|---|
| Frame | SpeedyBee Bee35 Pro | 153 mm, CNC VTX heatsink + alloy front end, 138 g + 15 g heatsink | Unmanned Tech #18595 | £35.75 | 2026-09-07 |
| FC/ESC | MicoAir743 V2 | BMI088, 30.5×30.5, 2–6S, 55 A AM32. Ships with ArduPilot preloaded; reflash to iNav | Unmanned Tech #18595 | £64.99 | 2026-09-07 |
| Flow/ToF | MicoAir MTF-01P | Optical flow + 12 m lidar, MSP mode | Unmanned Tech #18595 | £22.99 | 2026-09-07 |
| GPS/compass | Flywoo GOKU GM10 Mini V3 | u-blox M10050 + QMC5883L, 18×18 mm, 4.1 g | Unmanned Tech #18595 | £16.90 | 2026-09-07 |
| RX | RadioMaster RP3 V2 ELRS 2.4 GHz nano | CRSF | Unmanned Tech #18595 | £19.99 | 2026-09-07 |
| VTX | Walksnail Avatar HD Mini VTX V3 Module, 32 GB | MSP DisplayPort. Mis-order: VTX only, no camera or antenna (owner, 2026-09-17) | Flying Tech #118823 | £79.00 | 2026-09-07 |
| Camera | Walksnail Avatar HD Nano Camera V3 | Bought to fill that gap. Not the camera the owner meant to order, but expected to work (owner, 2026-09-17); untested. With the Mini VTX V3 it makes Walksnail's Nano Kit V3 pairing ([Oscar Liang review](https://oscarliang.com/walksnail-avatar-hd-nano-kit-v3/)): 14 × 14 mm, 1/3.2" 4:3 sensor, 160° FOV, 1080p60 recording, no Gyroflow support ([Caddx](https://www.caddxfpv.com/blogs/news/how-to-choose-a-walksnail-vtx-kit-for-1s-3s-fpv-drones)). The frame lists a 19/20 mm camera mount ([SpeedyBee](https://www.speedybee.com/speedybee-bee35-3-5-inch-frame/)); whether the kit holds a 14 mm adapter is to be checked (owner). Read 2026-09-17 | HobbyRC #344663 | £40.00 | 2026-09-11 |
| VTX antenna | Walksnail Avatar HD VTX V2 Antenna | | HobbyRC #344663 | £7.80 | 2026-09-11 |
| Motors | 4× T-Motor F2004 3000KV (TM-A) | 1.5 mm T-mount shaft, 12×12 mm bolt pattern, 16.4 g. £18.90 each | Drone Authority DA-23129 | £75.60 | 2026-09-11 |
| Props | HQProp Duct-T90MMX3, transparent grey | 90 mm, 3" pitch, 3-blade, 2.35 g, 1.5 mm T-mount. 2 packs of 4 at £1.85 a pack (owner, 2026-09-17): 8 props: a set of 4 plus a spare set | HobbyRC #344663 | £3.70 | 2026-09-11 |
| Battery | 3× existing 4S1P 21700, Molicel P45B | 4500 mAh, 315 g, self-built, shared across fleet. Pack count vs cells bought: see [fleet](../../../fleet/README.md) | existing | — | — |

Order totals inc shipping: Unmanned Tech #18595 £160.62 (free shipping), delivered
2026-09-10; Flying Tech #118823 £82.90, delivered 2026-09-09; Drone Authority DA-23129
£81.30, delivered 2026-09-15; HobbyRC #344663 £54.99, a HobbyRC parcel delivered
2026-09-16 (taken to be this order, the only one open).

**Also bought, not fitted:** 4× T-Motor F2004 **1700KV**, Unmanned Tech #18596, 2026-09-07,
£75.60 (£79.19 with shipping), delivered 2026-09-10 — the mis-order in
[DEC-03](decisions.md). Kept, not returned: in hand and unassigned (owner, 2026-09-17), listed with the
[wk-inventory `docs/stock.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/docs/stock.md).

Decisions behind several of these choices: [`decisions.md`](decisions.md).

## Outstanding

- XT60 pigtail and 35 V 470–1000 µF low-ESR capacitor. Check stack box contents first.
- Battery strap
- Printed parts. See [`../print/sources.md`](../print/sources.md).

## Existing kit assumed present

Walksnail goggles and RadioMaster ELRS transmitter (models in [`fleet/README.md`](../../../fleet/README.md)), 5" Betaflight quad ([`../../fpv-5/`](../../fpv-5/README.md)), DJI Neo.
