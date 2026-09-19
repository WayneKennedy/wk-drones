# Printed parts

Upstream sources and licences for every STL. Local copies of what was actually
printed go in [`stl/`](stl/). Licences are TBC until checked at each source. This repo is public and MIT-licensed;
only commit an upstream STL to `stl/` if its licence permits redistribution, and
record that licence here.

## SpeedyBee official Bee35 files

<https://docs.speedybee.cn/en/fpv/fpv-drones/bee35-drone/bee35-3d-print-files.html>

Relevant files:

- `19mmCamera-mount-bracket.stl`
- GPS mounts: `121.stl`, `181.stl`, `220.stl`, `251.stl`, `880.stl`
- `bee35-2sma.stl` — dual SMA for Walksnail antennas
- `35-TX.stl`

Lens damping inserts are on the separate speedybee.com Bee35 frame download page.

### GPS mount for the Matek M10Q-5883 (2026-09-19)

The GM10 is mislaid ([`../docs/bom.md`](../docs/bom.md)); the spare M10Q-5883 does not fit
the frame's supplied TPU mount (owner). The M10Q-5883 PCB is 20 × 20 mm (owner, and Matek:
20 × 20 × 12.4 mm, 8 g, JST-GH 6-pin; STEP in `M10Q-5883_step.zip` on Matek's product page).

SpeedyBee's page says nothing about which module each file is for. SpeedyBee sells the
same set as "BEE35 Master 5 V2 GPS 3D TPU Mount 121/181/220/251/880". Measured from the
STLs by slicing (2026-09-19, not printed; the reading of the geometry is inferred):

| File | Overall (mm) | Board pocket (mm) |
|---|---|---|
| `181.stl` | 22.0 × 26.3 × 21.7 | 18.0 wide: the GM10's 18 × 18 |
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

Official STL on MicoAir's MTF-01P product page. Mounting is 24.3 × 12 mm with
Ø2.5 mm holes.

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
