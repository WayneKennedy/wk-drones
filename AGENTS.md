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

## CAD in FreeCAD

CAD is done in FreeCAD, in the GUI where the owner can watch
([F-DEC-09](fleet/decisions.md)); a part's source is a Python script with the `.FCStd`
it emits checked in beside it ([F-DEC-10](fleet/decisions.md)). Worked example:
[`aircraft/bee35/print/src/flow-cage.py`](aircraft/bee35/print/src/flow-cage.py). Every
rule below was learned from an error in FreeCAD 1.1.3 (2026-09-29); errors in the owner's
Report view are noise they have to read, so get it right before it runs in the GUI.

- **Spreadsheet values are written as expressions: `sheet.set(cell, "=-0.5 mm")`.**
  Without the `=`, a negative value with a unit is stored as text, and everything bound
  to it fails with `Failed to convert to Quantity in property binding`. Give every value
  its unit. Find a cell with `sheet.getCellFromAlias(alias)`, not by scanning column A.
- **One constraint per degree of freedom.** A `Symmetric` about an axis on the ends of a
  line that is already `Horizontal`/`Vertical` is redundant; so is `Symmetric` on arc
  centres whose radii are already `Equal`. A redundant constraint invalidates the sketch
  and every feature after it, and the body ends with no solid. Centre a profile with
  `Symmetric` about the origin **point** on two diagonal points, or with a signed
  `DistanceX` (`"-Params.W / 2"`); negative `DistanceX`/`DistanceY` values are accepted.
- **Check before saving:** every object `isValid()`, every sketch `DoF == 0` with empty
  `RedundantConstraints`, `ConflictingConstraints` and `MalformedConstraints`, and the
  body exactly one valid solid. The script refuses to save or export otherwise.
- **A `Pocket` cuts against the sketch normal.** From a sketch on the XY plane, cutting
  up into the part needs `Reversed = True`.
- **Bind, do not bake:** dimensions are `setExpression(...)` onto the `Params`
  spreadsheet, with `evalExpression` for the number the geometry is first drawn at, so
  the document stays editable from the spreadsheet.
- **Wrap anything sent through the FreeCAD MCP in `try/except` and print the
  traceback.** An uncaught exception discards all printed output and raises an error in
  the Report view. Prototype in a scratch document and close it afterwards.
- **Run the script as `__main__` with `__file__` set** — the `exec(compile(...))` line in
  the script's header, the same in the GUI and headless (`FreeCADCmd -c "..."`).
  `FreeCADCmd script.py` *imports* the file instead: `__name__` is not `__main__`,
  nothing runs, nothing is printed, and a `__pycache__` appears.
- **FreeCAD here is a flatpak and cannot see `/tmp`.** Scripts and outputs live under the
  home directory; a path it cannot see fails silently.
- **Delete the old `.FCStd` before `saveAs`,** or FreeCAD leaves a dated `.FCBak` beside
  it (gitignored, with `.FCStd1`).
- **`TechDraw.projectToSVG` takes one `type` string** (`"ShowHiddenLines"`; combining two
  is ignored) and its default hidden-line style is malformed SVG — pass all six style
  dicts.
- **A remodel is proved against the solid it replaces:** `a.cut(b).Volume +
  b.cut(a).Volume` is 0. Measure claims in the notes off the solid too; two in the
  `flow-cage` notes were false.

## History

Until 2026-09-13 this repository was `wk-drone-bee35` and held the Bee35 alone; that
record moved unchanged to `aircraft/bee35/`. GitHub redirects the old name.
