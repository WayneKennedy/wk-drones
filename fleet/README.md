# Fleet

Kit and facts shared by more than one aircraft. Anything true of one aircraft only
belongs in that aircraft's folder. Decisions: [`decisions.md`](decisions.md). Open:
[`open-questions.md`](open-questions.md).

## Shared kit

| Item | What is known | Source of the fact |
|---|---|---|
| RC link | ExpressLRS 2.4 GHz. Transmitter is a RadioMaster with an internal ELRS module; model TBC. Receivers: Bee35 RadioMaster RP3 V2; 5" Happymodel EP1 Dual TCXO | Bee35 [`docs/bom.md`](../aircraft/bee35/docs/bom.md), [OQ-02](../aircraft/bee35/docs/open-questions.md); 5" [`docs/bom.md`](../aircraft/fpv-5/docs/bom.md) |
| Video | Walksnail Avatar HD on the Bee35. Goggles model, and whether the other aircraft share the system, TBC | Bee35 `docs/bom.md` |
| Battery packs | Bee35 and 5" are both 4S. 3× self-built 4S1P Molicel P45B 21700 packs, which the Bee35 was kept 4S to share; the 5" flies 4S1P 1300 mAh LiPos. Whether the 5" also flies the P45Bs, TBC. 3× GNB 1300 mAh 4S 120C LiHV were ordered 2025-08-07 (HobbyRC #303459, £67.82); whether those are the 5"'s packs is TBC. Holybro: none recorded | Bee35 [DEC-03](../aircraft/bee35/docs/decisions.md); 5" [`docs/bom.md`](../aircraft/fpv-5/docs/bom.md) |
| Firmware | Bee35: iNav. 5": Betaflight, version TBC. Holybro: none flashed, ArduPilot implied ([DEC-01](../aircraft/holybro-10/docs/decisions.md)). The Bee35's choice of iNav assumed the 5" ran it too; it does not. Switching the 5" to iNav is open (5" [OQ-01](../aircraft/fpv-5/docs/open-questions.md)) | Bee35 [DEC-01](../aircraft/bee35/docs/decisions.md) and its correction; 5" [`README.md`](../aircraft/fpv-5/README.md) |
| Charger | HOTA D6 Pro dual-channel AC/DC, ordered 2025-08-07 (£83.75) | HobbyRC #303459 invoice, read 2026-09-17 |
| Printed parts | Every printable part comes off the family printer; materials and profiles are in wk-robotics [`docs/common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#printing) | wk-robotics |

## Spare flight controllers

In hand and assigned to no aircraft (owner, 2026-09-17):

| Part | State | Source of the fact |
|---|---|---|
| Matek F405 Wing V2 | Unused. Ordered 2025-08-07, £39.95. Matek lists 10 PWM outputs and multirotor support, so it could fly a quad | HobbyRC #303459 invoice; [Matek](https://www.mateksys.com/?portfolio=f405-wing-v2) |
| SpeedyBee F405 | Used. Exact model and origin TBC; whether it is related to the 5"'s SpeedyBee F405 V3 stack is unknown | Owner |

Everything else about the fleet, tooling, field procedures, is not yet recorded
([F-OQ-01](open-questions.md)).
