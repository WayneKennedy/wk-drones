# Fleet

Kit and facts shared by more than one aircraft. Anything true of one aircraft only
belongs in that aircraft's folder. Decisions: [`decisions.md`](decisions.md). Open:
[`open-questions.md`](open-questions.md).

## Shared kit

| Item | What is known | Source of the fact |
|---|---|---|
| RC link | ExpressLRS 2.4 GHz. Transmitter: Radiomaster TX16S MKII MAX (ELRS), HobbyRC #231404, 2023-06-30, £249.98, with a Radiomaster 6200 mAh transmitter battery (£29.99) — the only transmitter purchase in the mail, so taken to be this one. Receivers: Bee35 RadioMaster RP3 V2; 5" Happymodel EP1 Dual TCXO | Bee35 [`docs/bom.md`](../aircraft/bee35/docs/bom.md), [OQ-02](../aircraft/bee35/docs/open-questions.md); 5" [`docs/bom.md`](../aircraft/fpv-5/docs/bom.md); transmitter invoice read 2026-09-17 |
| Video | Walksnail Avatar HD. Goggles: Fat Shark Dominator Avatar HD. Every Walksnail purchase is listed under [Walksnail kit bought](#walksnail-kit-bought). The 5" carries a Pro Micro Kit (owner, 2026-09-17) | Invoices read 2026-09-17 |
| Battery packs | Bee35 and 5" are both 4S. 3× self-built 4S1P Molicel P45B 21700 packs, 12 cells, all working (owner, 2026-09-17), which the Bee35 was kept 4S to share. Only 8 of the cells are on an invoice — Fogstar #270653, 2023-07-31, £87.92; the mail holds no other cell purchase (Fogstar's only other order, #270917, is pack materials), so where the other 4 came from is unknown. Pack materials: Fogstar #270917 (insulators, nickel strip) and a spot welder from Amazon, 2023-08; the 5" flies 4S1P 1300 mAh LiPos. Whether the 5" also flies the P45Bs, TBC. 3× GNB 1300 mAh 4S 120C LiHV were ordered 2025-08-07 (HobbyRC #303459, £67.82); whether those are the 5"'s packs is TBC. Holybro: none recorded. **6S is the large-plane standard** ([F-DEC-03](decisions.md)): GNB 6000 mAh ×2 (2024-03-24, the day the Twin Otter was ordered) and 5000 mAh ×3 (2024-06-05, three days after the Avanti S) — likely the Otter's and the jet's respectively (owner, 2026-09-17, "likely"); a GNB 3500 mAh 6S (2023-06) was bought for the Seagull 40's electric conversion, which never happened; it and that power set are in hand, in wk-inventory stock (owner, 2026-09-17). Larger 4S on invoices, aircraft unrecorded: GNB 5500 mAh ×2 (2023-07), 2300 mAh ×1 (2023-06). Full lines: private wk-inventory `docs/purchases/hobbyrc.md` | Bee35 [DEC-03](../aircraft/bee35/docs/decisions.md); 5" [`docs/bom.md`](../aircraft/fpv-5/docs/bom.md) |
| Firmware | Bee35: ArduPilot Copter ([DEC-08](../aircraft/bee35/docs/decisions.md), 2026-09-19; it replaced an iNav plan whose commonality premise proved false). 5": Betaflight, version TBC. Holybro: none flashed, ArduPilot implied ([DEC-01](../aircraft/holybro-10/docs/decisions.md)). Switching the 5" to iNav is open (5" [OQ-01](../aircraft/fpv-5/docs/open-questions.md)) | Bee35 [DEC-08](../aircraft/bee35/docs/decisions.md); 5" [`README.md`](../aircraft/fpv-5/README.md) |
| Charger | HOTA D6 Pro dual-channel AC/DC, ordered 2025-08-07 (£83.75). Also 1S whoop chargers: VIFLY WhoopStor 3 (HobbyRC #256755, 2024-03-24) and a VIFLY Whoop charging board (#231460, 2023-06-30) | HobbyRC invoices, read 2026-09-17 |
| Ground station | QGroundControl on Linux for ArduPilot setup; install steps in [`ground-station.md`](ground-station.md) | Installed 2026-09-22 |
| Printed parts | Every printable part comes off the family printer; materials and profiles are in wk-robotics [`docs/common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#printing) | wk-robotics |

## Battery health

**Unknown for every pack, 2026-09-17.** Nothing has been cycled or load-tested and the
fleet's packs have sat for up to a year. **Pending task, owner:** for every pack — balance
charge, leave standing, check for cell sag, return to storage charge, and record the result
here. Blocked on finding the battery tester. It runs alongside the stock take
([wk-inventory `docs/stock.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/docs/stock.md)).
Treat every pack as unproven until its row says otherwise.

## Flying status

Owner, 2026-09-17:

- **BMFA membership: active** — insured to fly.
- **CAA Operator ID: active.** Registration numbers are not recorded in this public repo.
- **No club.** The owner has not joined a local flying club since moving house, so there is
  no runway for the large planes. This is why the Twin Otter's recommissioning is low
  priority. Renewal dates for both registrations are unrecorded.

## Spares and written-off aircraft

Parts and aircraft owned but assigned to no aircraft — the 1700KV motors, the spare
the Cockroach frame, the written-off Moblite7 and Seagull 40, and receivers and GPS
units found only on invoices — are in the owner's private stock list,
[wk-inventory `docs/stock.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/docs/stock.md) (moved there 2026-09-17). An aircraft that takes one moves it into its
own BOM.

## Walksnail kit bought

Every Walksnail-related purchase in the owner's mailbox, searched 2026-09-17. Prices are
line prices inc VAT; HobbyRC's 2023 orders also carried a 5% order discount. Where each
item is now is unrecorded unless a row says so.

| Item | Order | Price |
|---|---|---|
| Fat Shark Dominator Avatar HD goggles (Walksnail) | HobbyRC #231336, 2023-06-29 | £504.00 |
| Walksnail Avatar HD Pro Micro Kit, 32 GB | HobbyRC #231336, 2023-06-29 | £159.00 |
| Walksnail Avatar HD Pro Micro Kit, 32 GB | HobbyRC #236190, 2023-08-16 | £159.00 |
| Happymodel Moblite7 75 mm Walksnail whoop, ELRS — a complete aircraft with Walksnail built in; written off, kept as parts ([spares](#spares-and-written-off-aircraft)) | HobbyRC #231460, 2023-06-30 | £195.95 |
| Walksnail Avatar HD Mini VTX V3 module, 32 GB — Bee35; VTX only, a mis-order | Flying Tech #118823, 2026-09-07 | £79.00 |
| Walksnail Avatar HD Nano Camera V3 — Bee35; not the camera intended, expected to work | HobbyRC #344663, 2026-09-11 | £40.00 |
| Walksnail Avatar HD VTX V2 antenna — Bee35 | HobbyRC #344663, 2026-09-11 | £7.80 |
| Goggle antennas: Menace RC DigiPack (DJI/Walksnail/Fatshark) + 2 × Thrasher | Menace RC #6731, 2023-06-29 | £45.90 paid |
| Walksnail/Fatshark Avatar goggle foam; NordFPV goggle strap | NordFPV #5110, 2023-07-10 | £13.00; £11.00 |
| XT60 to DC 2.5 mm goggle power adapter | Drone Authority #21757, 2023-07 | £6.69 paid |

Walksnail-branded GPS (WS-M181, not video): the 5"'s, and a second in [spares](#spares-and-written-off-aircraft).

Placement (owner, 2026-09-17): **both Pro Micro Kits are accounted for** — one is on the 5",
the other is **fitted to the ATOMRC Swordfish's canopy**, with its matching camera and antenna,
found 2026-09-17 ([Swordfish `README.md`](../aircraft/swordfish/README.md)). **Which of the two
orders is which remains unknown and does not matter**: same item, £159.00 either way. The
Bee35's VTX was ordered without a camera or
antenna by mistake; the Nano camera bought to fill the gap is not what the owner meant to
order but is expected to work ([Bee35 `bom.md`](../aircraft/bee35/docs/bom.md)).

Everything else about the fleet, tooling, field procedures, is not yet recorded
([F-OQ-01](open-questions.md)).
