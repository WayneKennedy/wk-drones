# wk-drones — agent / contributor onboarding

Read this first. It is provider-neutral: every AI assistant or human working here reads
this same file.

## What this repository is

The build, configuration and maintenance record for a fleet of DIY aircraft, multirotors
and planes. See
[`README.md`](README.md) for the fleet table. Most of the fleet is human-piloted; **only
the Holybro 10" is a robot in the wk-robotics sense**, and the criterion that decides
that is defined in wk-robotics, not here.

## Relationship to wk-robotics

The Holybro is indexed as a project in
[wk-robotics](https://github.com/WayneKennedy/wk-robotics); this repo is indexed there as
a supporting record. The 4Cs standard and the placement rule from
[wk-robotics `AGENTS.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/AGENTS.md)
apply here in full: correct, complete, coherent, concise; a fact lives in exactly one
place; the repo is the memory and nothing durable lives only in chat or in one
assistant's private memory. Facts true of more than one *robot* in the family live in
wk-robotics `docs/common.md`. Facts true of more than one *aircraft* live in `fleet/`.

## Layout and the placement rule

| The fact is… | It lives… |
|---|---|
| True of one aircraft | `aircraft/<name>/` — its `README.md`, `docs/`, `config/`, `print/`, `logs/`, `maintenance.md` |
| True of more than one aircraft | [`fleet/`](fleet/README.md) — link, video, packs, tooling, procedures |
| A decision | Per aircraft: `aircraft/<name>/docs/decisions.md` as `DEC-nn`. Fleet-wide: [`fleet/decisions.md`](fleet/decisions.md) as `F-DEC-nn` |
| Still open | Per aircraft: `docs/open-questions.md` as `OQ-nn`. Fleet-wide: [`fleet/open-questions.md`](fleet/open-questions.md) as `F-OQ-nn` |

`DEC-nn` and `OQ-nn` numbers are scoped to their aircraft folder; two aircraft may both
have a `DEC-01`. Cite them with the folder when linking from outside it.

Each aircraft folder follows the same shape. The Bee35 is the complete example:
[`aircraft/bee35/README.md`](aircraft/bee35/README.md) lists every file and what it is
for. New aircraft copy that shape; empty folders are not created ahead of content.

## Conventions

- **Never state an open question as settled.** Decisions and open questions are separate
  files at both levels.
- **Check what is owned before suggesting a purchase.** Read the private
  [wk-inventory `docs/stock.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/docs/stock.md) and search the owner's invoices, and say what was found. Full rule and
  the owner's goal (fewer unused parts, more finished projects):
  [wk-inventory `AGENTS.md`](https://github.com/WayneKennedy/wk-inventory/blob/main/AGENTS.md#before-anything-is-bought).
- **TBC means TBC.** Do not fill in a value that has not been confirmed against hardware,
  an invoice or a datasheet. **Unknown** is a valid entry in the fleet table.
- **Config discipline.** Every `config/diff/` file is `YYYY-MM-DD-description.txt` with a
  matching line in that aircraft's `docs/tuning.md`. An untested config is marked untested.
- **Measured beats plausible.** Performance figures carry the date and conditions.
- **This repo is public.** No credentials, host names, network addresses or tailnet
  identifiers. Prices and suppliers are fine.
- Blackbox logs, firmware binaries and large STL archives are gitignored.

## History

Until 2026-09-13 this repository was `wk-drone-bee35` and held the Bee35 alone; that
record moved unchanged to `aircraft/bee35/`. GitHub redirects the old name.
