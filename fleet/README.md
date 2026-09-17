# Fleet

Kit and facts shared by more than one aircraft. Anything true of one aircraft only
belongs in that aircraft's folder. Decisions: [`decisions.md`](decisions.md). Open:
[`open-questions.md`](open-questions.md).

## Shared kit

| Item | What is known | Source of the fact |
|---|---|---|
| RC link | ExpressLRS 2.4 GHz. Transmitter: Radiomaster TX16S MKII MAX (ELRS), HobbyRC #231404, 2023-06-30, £249.98, with a Radiomaster 6200 mAh transmitter battery (£29.99) — the only transmitter purchase in the mail, so taken to be this one. Receivers: Bee35 RadioMaster RP3 V2; 5" Happymodel EP1 Dual TCXO | Bee35 [`docs/bom.md`](../aircraft/bee35/docs/bom.md), [OQ-02](../aircraft/bee35/docs/open-questions.md); 5" [`docs/bom.md`](../aircraft/fpv-5/docs/bom.md); transmitter invoice read 2026-09-17 |
| Video | Walksnail Avatar HD on the Bee35. Goggles: Fat Shark Dominator Avatar HD, HobbyRC #231336, 2023-06-29, £504.00 — the only goggles purchase in the mail. Whether the 5" carries Walksnail is TBC (candidates in its [`docs/bom.md`](../aircraft/fpv-5/docs/bom.md)) | Bee35 `docs/bom.md`; goggles invoice read 2026-09-17 |
| Battery packs | Bee35 and 5" are both 4S. 3× self-built 4S1P Molicel P45B 21700 packs (owner), which the Bee35 was kept 4S to share. **Only 8 cells are on an invoice** — Fogstar #270653, 2023-07-31, £87.92, enough for two 4S1P packs; the source of a third pack's cells is unknown. Pack materials: Fogstar #270917 (insulators, nickel strip) and a spot welder from Amazon, 2023-08; the 5" flies 4S1P 1300 mAh LiPos. Whether the 5" also flies the P45Bs, TBC. 3× GNB 1300 mAh 4S 120C LiHV were ordered 2025-08-07 (HobbyRC #303459, £67.82); whether those are the 5"'s packs is TBC. Holybro: none recorded | Bee35 [DEC-03](../aircraft/bee35/docs/decisions.md); 5" [`docs/bom.md`](../aircraft/fpv-5/docs/bom.md) |
| Firmware | Bee35: iNav. 5": Betaflight, version TBC. Holybro: none flashed, ArduPilot implied ([DEC-01](../aircraft/holybro-10/docs/decisions.md)). The Bee35's choice of iNav assumed the 5" ran it too; it does not. Switching the 5" to iNav is open (5" [OQ-01](../aircraft/fpv-5/docs/open-questions.md)) | Bee35 [DEC-01](../aircraft/bee35/docs/decisions.md) and its correction; 5" [`README.md`](../aircraft/fpv-5/README.md) |
| Charger | HOTA D6 Pro dual-channel AC/DC, ordered 2025-08-07 (£83.75). Also 1S whoop chargers: VIFLY WhoopStor 3 (HobbyRC #256755, 2024-03-24) and a VIFLY Whoop charging board (#231460, 2023-06-30) | HobbyRC invoices, read 2026-09-17 |
| Printed parts | Every printable part comes off the family printer; materials and profiles are in wk-robotics [`docs/common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#printing) | wk-robotics |

## Spares in hand

In hand and assigned to no aircraft (owner, 2026-09-17):

| Part | State | Source of the fact |
|---|---|---|
| T-Motor F2004 1700KV ×4 | Unused; the Bee35 mis-order ([DEC-03](../aircraft/bee35/docs/decisions.md)). Ordered 2026-09-07, £75.60. 1700KV is the 6S variant | Owner; Unmanned Tech #18596 invoice |
| SpeedyBee F405 | Used. Exact model and origin TBC; whether it is related to the 5"'s SpeedyBee F405 V3 stack is unknown. Candidates, inferred only: three SpeedyBee F405 WING boards were bought (HobbyRC #232315 with the Swordfish, #233536, #242930; 2023-07 to 2023-10, £35.90 each) | Owner; HobbyRC invoices |

## Bought, not assigned to any aircraft

On invoices read 2026-09-17; whether still in hand is unknown.

| Part | Order | Price |
|---|---|---|
| Matek M10Q-5883 GPS/compass (a third; two are on the Holybro BOM) | HobbyRC #262164, 2024-05-20 | £31.80 |
| Walksnail WS-M181 GPS (a second; one is on the 5") | HobbyRC #266365, 2024-07-01 | £16.99 |
| Radiomaster RP3 V2 ELRS Diversity receiver (likely the Phoenix's) | HobbyRC #303808, 2025-08-11, with the Phoenix | £22.99 |
| Walksnail Avatar HD Pro Micro Kit, 32 GB, ×2 (one may be on the 5") | HobbyRC #231336, 2023-06-29; #236190, 2023-08-16 | £159.00 each |
| Receivers: Matek R24-D ×2 (one with the Swordfish), Radiomaster ER6, ER8, ER5A ×2 | HobbyRC #232315, #235115, #268168, #231404 (2023-07 to 2024-07) | not totalled |

Everything else about the fleet, tooling, field procedures, is not yet recorded
([F-OQ-01](open-questions.md)).
