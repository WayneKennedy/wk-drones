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
