# Printed parts

Upstream sources and licences for every STL. Local copies of what was actually
printed go in [`stl/`](stl/). Licences are TBC until checked at each source. This repo is public and MIT-licensed;
only commit an upstream STL to `stl/` if its licence permits redistribution, and
record that licence here.

## Parts designed here

### `cam-head` — printed replacements for the mislaid CNC head hardware ([OQ-04](../docs/open-questions.md))

**The one-piece mount is a FreeCAD model:** source [`src/cam-mount.py`](src/cam-mount.py),
which emits [`src/cam-mount.FCStd`](src/cam-mount.FCStd) — a `Params` spreadsheet driving
a PartDesign body — and every `stl/bee35-cam-mount*` file (FreeCAD 1.1; how to run it is
in its header, the rules in [`AGENTS.md`](../../../AGENTS.md#cad-in-freecad)).
**Remodelled 2026-09-29, geometry unchanged**, from `mount()` in the CadQuery script as
it stood at `fef5c14`: the two solids' skins agree to under 0.000001 mm at some 870
points sampled each way, and neither has volume outside the other. The loose crossbar,
posts and their assembly are still built by [`src/cam-head.py`](src/cam-head.py)
(CadQuery ≥ 2.4), which no longer builds the mount. MIT, like the rest of this repo. The aircraft keeps its two aluminium side plates; these parts replace
the 25.5 mm standoff and the four damping balls. Parts are added as geometry is measured.

| Part | Size | What it does |
|---|---|---|
| `bee35-cam-mount` | 25.5 × 16.5 × 35.3 mm | **The whole head as one print** — two cheeks **rounded over the crossbar** (owner, 2026-09-29: a cap R3.8 about the bar's own axis, 0.3 mm outside the bar all round its top, met on each side by an arc that leaves the front or back edge vertically at z = −16 and runs tangent into the cap — R40.24 in front, R31.02 behind), a 2 mm floor, and a roof between the cheeks where the top stands above the pocket ceiling; the crossbar is embedded in the crown. **Pocket 19.0 mm wide** (owner). The camera hangs on M2 screws through the 2.85 mm cheeks; the two posts are shortened to 4.25 mm under the floor (at 10 mm their tops would sit inside the camera body). Front and back open. **`bee35-cam-mount-print.stl` is the same part laid front-face-down for printing** (owner's orientation, 2026-09-25); the front of the top overhangs for its first ~4.8 mm, its slope below 45° that far. **In TPU it needs no supports:** the first print, whose top overhung the same way for ~5.5 mm, was sliced with supports off and "came out perfect" (owner, 2026-09-29: "TPU is pretty sticky when it prints up a hanging slope"). Not tried in a rigid filament. **Designed 2026-09-25 on unmeasured camera assumptions, listed in the source: 19 × 19 body, pivots 5 mm behind the face on the mid-height line, face flush with the posts' front, axis at z = −14.75.** **Printed once, 2026-09-29, in TPU 95A** (print host job `bee35_cam_mount_tpu_orca.gcode`, OrcaSlicer 2.4.2, 0.2 mm layers, supports off, 61 min, 2.22 m of filament); **Revised 2026-09-29 off that print (owner): 3.5 mm shorter fore-aft from the front** — posts, front face and camera pivots all 3.5 mm aft, back face where it was (20 → 16.5 mm deep; post axes 7.5 → 4.0 mm ahead of the crossbar; pivots y 6.0 → 2.5). **The top redrawn the same day (owner)**, as above: the first print's top was one semi-ellipse over the whole depth (owner's sketch, 2026-09-25), which on the shorter part let the bar come 0.18 mm through it. **The revision was printed 2026-09-29 in TPU 95A and fits: "This latest camera mount is perfect"** (owner, fitted between the side plates with the camera in; print host job `bee35_cam_mount_rev2_tpu_orca.gcode`, from `bee35-cam-mount-print-rev2.stl`, 0.2 mm layers, supports off, 50 min, 1.84 m of filament) — [DEC-09](../docs/decisions.md). |
| `bee35-cam-crossbar` | Ø7.0 × 25.5 mm, 2.5 mm hole through | Spans the two side plates and sets their spacing — the standoff's job. An **M3 self-tapping** screw at each end passes through the plate's own M3-clearance hole (one of the four the damping balls would have used) into the bar. **Designed 2026-09-25, not printed, not offered up to the hardware.** |

- **Measured, 2026-09-25 (owner, callipers):** 25.5 mm plate face to plate face; the posts'
  bottoms 31.5 mm below the crossbar axis, 7.5 mm ahead of it and 4.5 mm inboard of each
  plate face, taken as axis positions — **the 7.5 was superseded on 2026-09-29**, when
  the owner moved the posts 3.5 mm aft off the first print (axes now 4.0 ahead; 3.5 is
  the posts' radius, so the 7.5 fits their front surface, which is the assistant's
  reading and not confirmed; the 4.5 inboard was read the same way, is unchanged, and the part fits with it); the pocket 19.0 mm between the cheeks. **The rest
  of the camera is assumed** and is the first thing to check: height, and where the side
  pivots sit behind the front face.
- **The mounting points are the crossbar's two ends and the two posts' bottoms:** M3
  self-tapping through the plates into the bar, and M3 self-tapping up into the posts.
- **Print on its side, no supports.** The screw then threads *across* the layers; driven
  along the layer axis a printed part splits.
- **PETG or similar rigid filament, not TPU.** This part holds a spacing under screw
  preload and TPU creeps. Damping belongs in the camera-holding part, still to be designed.

### `flow-cage` — TPU strap over the MTF-01P, taped to the VTX heatsink ([OQ-05](../docs/open-questions.md))

Source [`src/flow-cage.py`](src/flow-cage.py), a FreeCAD script (FreeCAD 1.1; how to run
it is in its header, the rules in [`AGENTS.md`](../../../AGENTS.md#cad-in-freecad)). It
emits [`src/flow-cage.FCStd`](src/flow-cage.FCStd) — a `Params` spreadsheet driving a
PartDesign body, for opening directly — and into `stl/`: `bee35-flow-cage.stl`/`.step`,
`bee35-flow-cage-print.stl` (the same part; it is modelled sink-side-down, so the tabs
lie on the bed, the ring rises and the lip prints last) and four drawings,
`bee35-flow-cage-{plan,front,side,iso}.svg`, hidden edges dashed.
**Designed 2026-09-26. First print 2026-09-29** in TPU 95A (print host job
`bee35_flow_cage_tpu_orca.gcode`, supports off, 28 min, 0.97 m of filament), tried on the
aircraft the same day (owner, with photos):

| Finding off the first print | Change made, 2026-09-29 |
|---|---|
| The cage stood **2.5 mm too tall** | Face height cut by 2.5 (`FACE_TRIM`): 11.75 → **9.25 mm tall**. Which of the 9.25 mm body and the assumed 1 mm tape was out is not known |
| Its short ends sat on the screws that fasten the VTX to the sink | **A notch in the foot of each short end**, centred, through the wall: 6 wide × 2.5 high (the assistant's figures, not confirmed) |
| The tabs' ends reached the same screws fore and aft | Tabs **1 mm shorter outwards**: 0.9 mm left beyond the M2 hole, tabs end at y = ±16.14 |
| "A loose-ish fit" | Walls **in 0.5 mm in all**: fit 0.3 → 0.05 mm each side. The window is where it was |
| "The cable notch works perfectly" | None |

**The revision's print started 2026-09-29 22:09 UTC** in TPU 95A (print host job
`bee35_flow_cage_rev2_tpu_orca.gcode`, from `bee35-flow-cage-print-rev2.stl`, 0.2 mm
layers, supports off); outcome not yet recorded.

**Remodelled in FreeCAD 2026-09-29** ([F-DEC-09](../../../fleet/decisions.md)) from the
CadQuery model (last at `5fbd1ac`), geometry unchanged at that step (`fef5c14`: boolean
difference between the two solids 0.000000 mm³). **Revised the same day** from a calliper
measurement and the owner's changes, and again off the first print; now
36.30 × 32.28 × 9.25 mm, 1774.2 mm³.

Owner's scheme (2026-09-26): the sensor is stuck to the heatsink's face with strong gel
tape, dead centre, long axis across the aircraft; this cage goes over it and screws to the
sink's **fore and aft M2 holes only** — the sensor's 33 mm covers the other two. The tape
locates and carries flight loads; the cage carries landing and peel loads.

| | |
|---|---|
| Ring | 36.3 × 23.9 mm outside, 1.5 mm wall, 0.05 mm fit each side round the sensor's body, **9.25 mm tall**; corners R2 |
| Lip | **1.25 mm** in from the wall (1.2 mm over the body's face), 1.5 thick, leaving a **30.8 × 18.4 mm window**; the two lens cylinders stand up through it, the window's edge 0.55 mm from them on their side; the window's **top edge rounded R1** all round (owner, 2026-09-29), which opens the top face to 32.8 × 20.4 and leaves the window itself as it was; **flat underneath** (known defect below). 2 mm until 2026-09-29; the window's size was proposed by the assistant and agreed by the owner that day, as a 1.5 mm lip from walls then 0.25 mm further out |
| Notch | 7 mm wide, **5 mm high from the sink** (owner, 2026-09-29; was full height), in the connector-side wall at x = +3 for the JST and cable; the ring and lip are whole above it. **Proved on the first print** |
| End notches | One in the foot of each short end, centred: 6 wide × 2.5 high, through the wall, over the screws that fasten the VTX to the sink |
| Tabs | On the sink fore and aft, 1.5 thick, Ø2.2 holes at **y = ±14.14** (the diamond's points), **square where they join the ring, R2 on the outer corners only** (owner, 2026-09-29). Cylinder side 8 mm wide, joined over all 8. Connector side **x −7 to +10.5** (17.5 mm): it runs 4 mm past the notch (owner, 2026-09-29: longer, to cover the notch; 4 mm proposed by the assistant and agreed), joining the ring over 6.5 mm on one side of the notch and 4 mm on the other. The cable exits over this tab, dressed sideways past the M2 head |
| M2 heads | **No recess in the ring** (owner, 2026-09-29). A Ø3.8 head on the tab clears the ring's face by 0.29 mm |
| Tape | 1.0 mm assumed (`TAPE_T`); measure the tape and set it, it moves the lip |
| Material | TPU 95A on the fleet's `tpu` profile |

**No STEP or other CAD of the MTF-01P exists to be had** (searched 2026-09-27): MicoAir
publish none — the "drawing" on their product page is the wiring diagram — and GrabCAD's
community remodels need a login. Beyond the 33.2 × 20.8 × 16.8 spec and the owner's
measurements, the geometry is **scaled off MicoAir's product photos, ±0.5 mm**: lens and
ToF cylinders ~Ø8 at x −5.8 and +4.2; a Ø~4 third window near the centreline; corner
screws countersunk in the face; the 4-pin JST on the long side face opposite the
cylinders, near the middle, at sink level.

**Measured off the sensor (owner, callipers):**

| What | Value | Date | Replaces |
|---|---|---|---|
| Rectangular body, sink side to face | 9.25 mm | 2026-09-27 | — |
| Lens cylinders' edge to the body's nearest long edge (`CYL_GAP`), taken as the smallest such gap | 1.75 mm | 2026-09-29 | 2.7 mm scaled off the photo; with the 2 mm lip it left 0.05 mm to the cylinders |

**Still to check with callipers before printing:** the body's length and width (the
cylinders' position is worked out from the width), the cylinder diameters, the
connector's position along the edge and its height off the sink (they set the notch),
and the tape thickness. Also unchecked: whether the side M2 hardware under the sensor's
footprint stands proud of the sink, which would stop the sensor sitting flat on the tape.

**Known defect, found 2026-09-29 by measuring the solid in FreeCAD; not fixed, the fix
is the owner's choice** ([OQ-05](../docs/open-questions.md)): **the lip's underside is
flat, not 45°.** The CadQuery model cut its 45° slope from inside the sensor cavity,
where there was nothing left to cut, so the solid never had a sloped face: the lip is an
overhang printed over air, 1.25 mm wide now, 2 mm then. **The first print's lip, 1.5 mm
wide and printed without supports, is whole in the owner's photo**, and the owner
raised nothing against it. This file said
"45° underneath" and "no supports" until 2026-09-29; neither was true of the STL. A real
45° slope has to sit above the sensor's face, which makes the lip thicker than its
1.5 mm and the part taller.

**Fixed 2026-09-29:** the tabs were necked where they joined the ring, because the corner
radius was applied at the ring too — 4 mm of joint on the 8 mm tab, and the
connector-side tab joined on one side of the notch only, over 4.5 mm. Figures above are
the repaired joints.

Earlier passes, both dropped the day before: a plate on the sink's own M2s with corner
legs as feet (`f4b3763`, `223e6c5`; too low) and a three-point plate under the nose
(`fb1ca05`; in the front ducts' downwash).

## SpeedyBee documents

- [Bee35 Quick Start Manual](https://spcdn.speedybee.cn/cdn/117883962633752576.pdf)
  (2024-04) — binding, modes, motor directions, pre-flight checks. **No camera-mount or
  assembly detail.**
- [O4 Air Unit Pro aluminium head module installation tutorial](https://support.speedybee.cn/pdf?f=hg2h&l=en)
  (2025-08-06) — the head's full fastener schedule, including the 25.5 mm aluminium
  standoff and the four camera vibration damping balls of
  [OQ-04](../docs/open-questions.md).

Neither is committed here: SpeedyBee's copyright, and this repo is public.

## SpeedyBee official Bee35 files

<https://docs.speedybee.cn/en/fpv/fpv-drones/bee35-drone/bee35-3d-print-files.html>

**Measured by bounding box from the downloaded STLs, 2026-09-25** (not printed):

| File | Size (mm) | What it actually is |
|---|---|---|
| `19mmCamera-mount-bracket.stl` | 13.2 × 13.2 × 4.25 | **Not a bracket — a lens damping insert.** Byte-identical geometry to `20mm.stl` in the Lens Damping archive. For a standard-body camera's lens, nothing to do with the O4 CNC head (owner, 2026-09-25) |
| `35-1.stl` | 31.0 × 29.0 × 17.9 | Four-hole plate with three curved flexure arms — a soft mount. The only damping-part prior art on this frame |
| `35-2.stl` | 23.0 × 44.0 × 35.8 | Antenna mount with tube clips |
| `35-3.stl` | 10.0 × 10.0 × 4.0 | Small spacer |
| `35-4.stl` | 17.1 × 55.2 × 9.0 | Strip |
| `35-5.stl` | 18.0 × 6.0 × 14.5 | Small block |
| `35-6.stl` | 13.2 × 13.2 × 4.25 | Same as the "19 mm bracket" above |
| `35-7（14mm）.stl` | 7.3 × 13.4 × 13.4 | Same as `14mm.stl` below |

**Lens Damping archive** (`Lens Damping.7z`, frame download page) holds `14mm.stl`
(7.3 × 13.4 × 13.4), `19mm.stl` (13.2 × 13.2 × 4.4) and `20mm.stl` (13.2 × 13.2 × 4.25) —
inserts by camera body size. The Nano V3 on this aircraft is adapted to 19/20 mm, so the
matching insert exists.

**No CAD is published.** Both SpeedyBee download pages carry STL and PDF only — no STEP or
DXF for the CNC head parts (checked 2026-09-25). GrabCAD's SpeedyBee tag has stacks and
ESCs, no Bee35 frame.

Relevant files:

- `19mmCamera-mount-bracket.stl`
- GPS mounts: `121.stl`, `181.stl`, `220.stl`, `251.stl`, `880.stl`
- `bee35-2sma.stl` — dual SMA for Walksnail antennas
- `35-TX.stl`

Lens damping inserts are on the separate speedybee.com Bee35 frame download page.

### GPS mount for the Matek M10Q-5883 (2026-09-19)

The GM10 is mislaid ([`../docs/bom.md`](../docs/bom.md)); the spare M10Q-5883 does not fit
the frame's supplied TPU mount, which is ~12 × 16 (owner). The M10Q-5883 PCB is 20 × 20 mm (owner, and Matek:
20 × 20 × 12.4 mm, 8 g, JST-GH 6-pin; STEP in `M10Q-5883_step.zip` on Matek's product page).

SpeedyBee's page says nothing about which module each file is for. SpeedyBee sells the
same set as "BEE35 Master 5 V2 GPS 3D TPU Mount 121/181/220/251/880". Measured from the
STLs by slicing (2026-09-19, not printed; the reading of the geometry is inferred):

| File | Overall (mm) | Board pocket (mm) |
|---|---|---|
| `121.stl` | 16.0 × 20.0 × 16.7 | ~13 wide. The frame's supplied mount is ~12 × 16 (owner, 2026-09-19), so probably this one |
| `181.stl` | 22.0 × 26.3 × 21.7 | 18.0 wide: fits an 18 × 18 module — the GM10 Mini V3 (18 × 18 × 4.8 mm, [Flywoo](https://flywoo.net/products/goku-gm10-mini-v3-gps-w-compass)) or the BN-180 stand-in. **The GM10 never fitted the supplied ~12 × 16 mount either**; the Bee35 needs a printed GPS mount whichever unit flies |
| `220.stl` | 24.4 × 26.4 × 16.0 | 20.4 × 22.4, ~4–5 deep, open on one face, closed by a solid plate on the other |
| `251.stl` | 28.4 × 30.5 × 24.6 | ~25 wide |
| `880.stl` | 32.5 × 32.5 × 20.0 | 28.5 × 28.5 |

`220.stl` is the closest: snug on one 20 mm axis, ~2.4 mm slack on the other. It also
carries the Bee35 frame interface, so it is the first thing to test-print (3.4 cm³ TPU).
Unchecked: whether the M10Q's JST-GH connector clears the pocket wall, and whether the
corner clips hold a 20 mm board.

Community alternatives (not printed):

- [Printables 999201](https://www.printables.com/model/999201-speedybee35-gps-mount),
  Bee35 remix for a 22 × 22 mm GEPRC M10; TPU, push-fit with four edge holders.
  CC BY-NC.
- [Printables 1485002](https://www.printables.com/model/1485002-speedybee-maser-5-v2-mateksys-m10q-5883-gps-compas),
  made for the M10Q-5883 but on the **Master 5 V2**, rear-mounted with that frame's
  screws. Whether it fits the Bee35 is unverified. CC BY-NC-SA.

If none fits, design one parametrically, the way the Holybro deck was done
([`../../holybro-10/print/src/h743-deck.py`](../../holybro-10/print/src/h743-deck.py)),
from Matek's STEP and the frame interface in `220.stl`.

## MTF-01P case

**Sensor, from [MicoAir's product page](https://micoair.com/optical_range_sensor_mtf-01p/)
(read 2026-09-25, not measured on the unit):** 33.2 × 20.8 × 16.8 mm, 8 g. Mounting
**24.3 × 12 mm, Ø2.5 mm** holes. Optical flow lens **42° FOV**; ToF 808 nm, 1.5° emission.
UART 115200, LVTTL 3.3 V.

**Clearance the 42° cone needs:** half-angle 21°, so the flow footprint is 0.38 × height —
77 mm across at 100 mm off the ground. No part of a bracket may enter it.

**No STL or CAD is published by MicoAir** (their page links neither, checked 2026-09-25).
Community cases: [Printables](https://www.printables.com/model/1060101-mtf-01-mtf-01p-optical-flow-lidar-sensor-cover/user-gcodes),
[Thingiverse 6319409](https://www.thingiverse.com/thing:6319409),
[Robofusion](https://docs.robofusion.net/projects/sensor-cases-and-mounts). Licences
unchecked; none is committed here.

Community alternatives exist on Printables and Cults. The design worth copying
splits it into a TPU body with a rigid cup, so the sensor is vibration-isolated
without being free to wobble.

Constraints for the flow sensor mount:

- Fully unobstructed downward view: no duct lip, strap or landing pad edge in the cone
- Minimum 8 cm ground clearance in operation
- Needs 60+ lux
- The Pro's alloy bottom plate can be drilled and tapped M2 directly. Alloy is
  non-magnetic, so it is irrelevant to the compass.

## Camera tilt inserts

Low-tilt inserts (0/5/10°) to try before any servo tilt axis. See
[`../docs/setup-ardupilot.md`](../docs/setup-ardupilot.md). Source TBC.

## Materials

- TPU 95A for damping and impact-facing parts
- PETG or PLA for rigid brackets
