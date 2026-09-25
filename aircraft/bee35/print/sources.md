# Printed parts

Upstream sources and licences for every STL. Local copies of what was actually
printed go in [`stl/`](stl/). Licences are TBC until checked at each source. This repo is public and MIT-licensed;
only commit an upstream STL to `stl/` if its licence permits redistribution, and
record that licence here.

## Parts designed here

### `cam-head` — printed replacements for the mislaid CNC head hardware ([OQ-04](../docs/open-questions.md))

Source of truth is the parametric model [`src/cam-head.py`](src/cam-head.py)
(CadQuery ≥ 2.4); `stl/` holds what it emits, alongside a STEP of each part. MIT, like the
rest of this repo. The aircraft keeps its two aluminium side plates; these parts replace
the 25.5 mm standoff and the four damping balls. Parts are added as geometry is measured.

| Part | Size | What it does |
|---|---|---|
| `bee35-cam-mount` | 25.5 × 20.1 × 35.5 mm | **The whole head as one print** — two **arched** cheeks (owner's sketch, 2026-09-25: a semi-ellipse springing from z = −16 at the front and back edges, cresting over the crossbar), a 2 mm floor, and a roof between the cheeks where the arch stands above the pocket ceiling; the crossbar is embedded in the crown. **Pocket 19.0 mm wide** (owner). The camera hangs on M2 screws through the 2.85 mm cheeks; the two posts are shortened to 5 mm under the floor (at 10 mm their tops would sit inside the camera body). Front and back open. **Designed 2026-09-25 on unmeasured camera assumptions, listed in the source: 19 × 19 body, pivots 5 mm behind the face on the mid-height line, face flush with the posts' front, axis at z = −14.75.** Not printed. |
| `bee35-cam-crossbar` | Ø7.0 × 25.5 mm, 2.5 mm hole through | Spans the two side plates and sets their spacing — the standoff's job. An **M3 self-tapping** screw at each end passes through the plate's own M3-clearance hole (one of the four the damping balls would have used) into the bar. **Designed 2026-09-25, not printed, not offered up to the hardware.** |

- **Measured, 2026-09-25 (owner, callipers):** 25.5 mm plate face to plate face; the posts'
  bottoms 31.5 mm below the crossbar axis, 7.5 mm ahead of it and 4.5 mm inboard of each
  plate face, taken as axis positions; the pocket 19.0 mm between the cheeks. **The rest
  of the camera is assumed** and is the first thing to check: height, and where the side
  pivots sit behind the front face.
- **The mounting points are the crossbar's two ends and the two posts' bottoms:** M3
  self-tapping through the plates into the bar, and M3 self-tapping up into the posts.
- **Print on its side, no supports.** The screw then threads *across* the layers; driven
  along the layer axis a printed part splits.
- **PETG or similar rigid filament, not TPU.** This part holds a spacing under screw
  preload and TPU creeps. Damping belongs in the camera-holding part, still to be designed.

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
