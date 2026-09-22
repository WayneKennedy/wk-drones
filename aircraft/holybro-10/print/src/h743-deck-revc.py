"""h743-deck rev C: the Matek H743-WING V3 on a floating TPU platform, X500 V2 upper plate.

Rev C replaces rev A/B's rigid '#' ribs with isolation: the FC rides on a 38 x 56 platform
hung from two anchor blocks by four Z-shaped flexure arms, which bend in every axis. Target
natural frequency 25-40 Hz, tuned from flight logs; arm width and thickness are the knobs.
Geometry is the owner-reviewed 2D drawing of 2026-09-21 (draw_revC.py, a scratch script
that was never committed), transcribed here, with two corrections from the TPU calibration
coupon printed that day (3d-printing docs/open-questions.md, "TPU 95A"):
  - arms drawn 1.9 wide, because 2.0 printed 2.10 (edge spread ~+0.1 mm), and width^3
    sets stiffness - the drawing's intent is a 2.0 mm printed arm;
  - hex holes 4.85 AF, because 4.55 AF would not take the brass standoff and 4.65 needed
    a press. 4.85 VERIFIED on the printed deck 2026-09-22: a standoff pushes in by hand and
    needs pliers to pull out (owner, one pillar tried).

Frame, as rev A: origin at the centre of the upper plate, z = 0 at its top face, +z up,
x fore-aft, y side to side. The M3 anchors (plate holes 3.4) are rev A's, at (+/-13.5,
+/-43). Prints UPSIDE DOWN - the z = TOP plane on the bed, so platform, arms and bars are
first layers and nothing needs support: slice with --rotate-x 180.

Build:  uv run --python 3.12 --with "cadquery>=2.4" python h743-deck-revc.py [outdir]
Needs:  cadquery >= 2.4 (built with 2.8.0)
"""

import math
import sys
import cadquery as cq

# ---------------------------------------------------------------- measured inputs
M3_ANCHORS = [(x, y) for x in (-13.5, 13.5) for y in (-43.0, 43.0)]  # plate holes 3.4, as rev A
FC_PATTERN = 15.25   # Matek H743-WING V3, 30.5 x 30.5 (rev A)
STANDOFF_L = 20.0    # M3 x 20 brass hex standoff, 4.55 AF (owner, 2026-09-21)

# ---------------------------------------------------------------- design (drawing, 2026-09-21)
TOP = 19.8           # pillar height: 0.2 under the standoff, so the top screw clamps brass only
PLAT_T = 5.0         # platform and arm thickness (vertical) - a tuning knob
PLAT_X, PLAT_Y = 56.0, 38.0   # FC footprint 54 x 36 plus 1 mm each side
PLAT_R = 3.0
FC_HOLE_D = 2.4      # M2 through-bolt from below, locknut on top of the stack
PILLAR_D = 11.0
BAR_T = 6.0          # anchor top bar joining each pair of pillars
HEX_AF = 4.85        # drawing 4.55; verified 2026-09-22 - hand press-in, pliers to remove
ARM_W = 1.9          # drawing 2.0; coupon correction - prints ~2.0 - a tuning knob
ARM_KNEE_Y = 29.0    # the arm's fore-aft leg runs at |y| = 29
ARM_JOIN_X = 24.0    # the arm meets the platform side at |x| = 24
OVERLAP = 1.0        # arm ends run this far into bar and platform, so the union is solid

BAR_Y = 43.0
BAR_X = 13.5
PLAT_Z0 = TOP - PLAT_T


def _prism(pts, z0, h):
    return cq.Workplane("XY").polyline(pts).close().extrude(h).translate((0, 0, z0))


def _arm(sx, sy):
    """Z-arm: inward from the anchor bar at x = +/-13.5, a fore-aft leg at |y| = 29, then
    inward again to the platform side at |x| = 24. Coordinates as in the drawing."""
    h = ARM_W / 2
    root = BAR_Y - PILLAR_D / 2 + OVERLAP
    tip = PLAT_Y / 2 - OVERLAP
    kx, ky, ax = ARM_KNEE_Y, ARM_JOIN_X, BAR_X
    pts_hv = [(root, ax - h), (kx - h, ax - h), (kx - h, ky - h), (tip, ky - h),
              (tip, ky + h), (kx + h, ky + h), (kx + h, ax + h), (root, ax + h)]
    pts = [(sx * v, sy * hh) for (hh, v) in pts_hv]     # drawing (H, V) -> CAD (x=V, y=H)
    return _prism(pts, PLAT_Z0, PLAT_T)


def build():
    parts = []
    for (x, y) in M3_ANCHORS:
        parts.append(cq.Workplane("XY").circle(PILLAR_D / 2).extrude(TOP).translate((x, y, 0)))
    for sy in (-1, 1):
        parts.append(
            cq.Workplane("XY").slot2D(2 * BAR_X + PILLAR_D, PILLAR_D, 0)
            .extrude(BAR_T).translate((0, sy * BAR_Y, TOP - BAR_T))
        )
    parts.append(
        cq.Workplane("XY").rect(PLAT_X, PLAT_Y).extrude(PLAT_T)
        .edges("|Z").fillet(PLAT_R).translate((0, 0, PLAT_Z0))
    )
    for sx in (-1, 1):
        for sy in (-1, 1):
            parts.append(_arm(sx, sy))

    body = parts[0]
    for p in parts[1:]:
        body = body.union(p)

    # Hex bores for the standoffs, right through: a vertex fore-aft, as drawn.
    for (x, y) in M3_ANCHORS:
        body = body.cut(
            cq.Workplane("XY").polygon(6, 2 * HEX_AF / math.sqrt(3))
            .extrude(TOP + 1).translate((x, y, -0.5))
        )
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.cut(
                cq.Workplane("XY").circle(FC_HOLE_D / 2).extrude(PLAT_T + 1)
                .translate((sx * FC_PATTERN, sy * FC_PATTERN, PLAT_Z0 - 0.5))
            )
    return body


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    out = args[0] if args else "."
    r = build()
    name = "h743-deck-revc"
    cq.exporters.export(r, f"{out}/{name}.stl", tolerance=0.03, angularTolerance=0.25)
    cq.exporters.export(r, f"{out}/{name}.step")
    bb = r.val().BoundingBox()
    print("bbox  X %.2f..%.2f  Y %.2f..%.2f  Z %.2f..%.2f"
          % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    print("volume %.2f cm3, solids %d, valid %s"
          % (r.val().Volume() / 1000.0, len(r.solids().vals()), r.val().isValid()))
