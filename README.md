# wk-drones

> **The project record moved to Basic Memory on 2026-11-10** (project `main`, folder `drones/`; start at the
> *Drones* note). Fleet and per-aircraft READMEs, BOMs, decisions, open questions and maintenance are canonical there; the copies here were deleted on 2026-11-10 (git history keeps them). This repo keeps what is about the artefacts: `config/`, `print/`, `fleet/cad`,
> `fleet/tools`, and each aircraft's `setup-ardupilot.md`, `tuning.md` and `wiring.md`.

Build, configuration and maintenance records for a small fleet of DIY aircraft,
multirotors and planes, and the kit they share. Every aircraft flies ELRS into a flight
controller ([F-DEC-02](memory://main/drones/fleet-decisions)). One folder per aircraft; fleet-wide facts live once, in `fleet/`.

Config files are the source of truth for each aircraft: version-controlled, diffable,
restorable onto replacement hardware.

## The fleet

| Aircraft | Folder | What it is | Firmware | Family robot? | State |
|---|---|---|---|---|---|
| **Bee35** | [`aircraft/bee35/`](aircraft/bee35/README.md) | 3.5" ducted cinewhoop, SpeedyBee Bee35 Pro frame, built for a DJI-like hands-off FPV experience | ArduPilot ([DEC-08](memory://main/drones/bee35/bee35-decisions)) | No — [DEC-07](memory://main/drones/bee35/bee35-decisions) | Motors mounted on frame (2026-09-15); next: soldering. Not flashed or flown |
| **Holybro 10"** | [`aircraft/holybro-10/`](aircraft/holybro-10/README.md) | Holybro X500 V2, 10" props, bought to carry a Raspberry Pi or Jetson wired to its flight controller (Matek H743 Wing V3) | None flashed; ArduPilot implied | **Yes — the fleet's only candidate** | Parts identified from invoices 2026-09-17; build state unknown ([F-OQ-01](memory://main/drones/fleet-open-questions)) |
| **Swordfish** | [`aircraft/swordfish/`](aircraft/swordfish/README.md) | ATOMRC Swordfish V-tail plane, PNP | Unknown | No | Repaired after two hard crashes; not commissioned (2026-09-17) |
| **Phoenix** | [`aircraft/phoenix/`](aircraft/phoenix/README.md) | VolantexRC Phoenix 2400 mm glider, PNP; Matek F405 Wing V2 chosen | None | No | Unbuilt (2026-09-17) |
| **Twin Otter** | [`aircraft/twin-otter/`](aircraft/twin-otter/README.md) | XFLY Twin Otter, 1800 mm — the largest in the fleet | None (receiver only, no FC) | No | Flight ready, in storage; rebuild to F-DEC-02 is low priority (2026-09-17) |
| **Avanti S** | [`aircraft/avanti-s/`](aircraft/avanti-s/README.md) | Freewing Avanti S V2 80 mm EDF jet, PNP | None (receiver only, no FC) | No | Crashed on its maiden; repairable, in storage (2026-09-17) |
| **5" freestyle** | [`aircraft/fpv-5/`](aircraft/fpv-5/README.md) | Existing 5" freestyle quad, TBS Source One V5 frame; covers the acro use case | Betaflight | No | Flight ready; last flown about a year before 2026-09-15. Partly recorded ([F-OQ-01](memory://main/drones/fleet-open-questions)) |

**Family robot?** means: does it meet the wk-robotics criterion for an aerial robot, an
intent-tier computer commanding the flight controller. The criterion and its two
topologies (onboard, or off-board over radio) are defined once, in
[*Robotics Common*](memory://main/robotics/robotics-common),
and the fleet-level decision applying it is [F-DEC-01](memory://main/drones/fleet-decisions). The
wk-robotics index lists the Holybro as a project and this repo as a supporting record;
the other aircraft are human-piloted and appear nowhere in that index.

## Where things live

- [`AGENTS.md`](AGENTS.md) — onboarding for any assistant or contributor
- [`fleet/`](fleet/README.md) — kit shared by more than one aircraft: radio link, video,
  battery packs, tooling · [*Fleet Decisions*](memory://main/drones/fleet-decisions) (`F-DEC-nn`) ·
  [*Fleet Open Questions*](memory://main/drones/fleet-open-questions) (`F-OQ-nn`)
- `aircraft/<name>/` — one aircraft: `README.md`, `docs/`, `config/`, `print/`, `logs/`,
  `maintenance.md`. Decisions and open questions are per aircraft (`DEC-nn`, `OQ-nn`,
  scoped to the folder).

## Licence

[MIT](LICENSE), covering everything here that is mine. Not run as an open-source project,
but nothing restricts reuse. Third-party STLs under `aircraft/*/print/stl/` keep their
upstream licences, listed in each aircraft's `print/sources.md`.
