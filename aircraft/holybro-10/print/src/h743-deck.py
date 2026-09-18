"""Raised deck carrying a Matek H743-WING V3 on the Holybro X500 V2 upper plate.

Every dimension below is measured from the two vendor STEP files, not from a ruler;
the measurements and their provenance are in ../sources.md.

Geometry, in the plate's own frame: origin at the centre of the upper plate, z = 0 at
its top face, +z up. The deck's long axis (the one carrying the M3 anchors at y = +/-43)
is the axis the board's 54 mm dimension runs along.

Build:  python h743-deck.py [outdir] [--template]
        --template emits a 3 mm flat fit-check plate: same footprint, same twelve hole
        positions, no deck. Prints in minutes and proves the patterns against the
        airframe and the board before the full deck is committed to.
Needs:  cadquery >= 2.8
"""

import sys
import cadquery as cq

# ---------------------------------------------------------------- measured inputs
# Holybro X500 V2 upper plate: the only anchors inside |x|<50, |y|<43.
M3_ANCHORS = [(x, y) for x in (-13.5, 13.5) for y in (-43.0, 43.0)]  # plate holes 3.4
M2_ANCHORS = [(x, y) for x in (-29.0, 29.0) for y in (-21.5, 21.5)]  # plate holes 2.2
# Matek H743-WING V3, 30.5 x 30.5 mounting (owner, from the board in hand, 2026-09-17):
# the board's four Ø4 holes carry silicone grommets, each wrapped round a brass standoff,
# and the bottom PD/ESC plate screws up into those standoffs with 4 x M2 countersunk.
# The board is fixed to this deck the same way — a longer M2 driven UP from under the
# deck into the same standoff — so the deck's bosses sit on that pattern and no grommet
# is consumed for the airframe mounting.
FC_PATTERN = (15.25, 15.25)
FC_BOSSES = [(x, y) for x in (-FC_PATTERN[0], FC_PATTERN[0])
             for y in (-FC_PATTERN[1], FC_PATTERN[1])]
FC_UNDERSIDE_CLEAR = 4.0  # tallest component under the bare PCB

# ---------------------------------------------------------------- design choices
DECK_Z = 15.0        # clear height under the deck, for cable runs and a second item
FLANGE_T = 3.0       # deck flange thickness; deck top face sits at DECK_Z + FLANGE_T
WALL_T = 2.4         # vertical rib thickness (6 perimeters at 0.4 mm)

# Every beam stops on the centre line of the anchor it reaches, and the anchor pillar
# caps it: pillar diameter equals flange width, so the cap is tangent and nothing
# protrudes past it.
RIB_LONG_X = 13.5    # longitudinal ribs sit under the M3 anchors
RIB_LONG_HALF_Y = 43.0
RIB_LAT_Y = 21.5     # lateral ribs sit under the M2 anchors
RIB_LAT_HALF_X = 29.0
FLANGE_LONG_W = 11.0
FLANGE_LAT_W = 11.0

BOSS_D = 6.0         # stays inside the flange width at x = +/-FC_PATTERN[0]
BOSS_H = 5.0         # the boss meets the FC's bottom plate; height is cable room
FC_BOLT_D = 2.4      # M2 clearance, driven up from below into the grommeted standoff
FC_HEAD_D = 5.0      # recess for the head, ceiling on the flange underside at DECK_Z
FC_HEAD_Z = 9.0      # floor of that recess: a clear column for the head and the driver
FC_HEAD_CSK = False  # True: 90 deg countersink for an M2 CSK head instead of a cap

PAD3_D = FLANGE_LONG_W   # anchor pillars; equal to the flange width, so they cap it
PAD2_D = FLANGE_LAT_W
BOLT3_D = 3.4
BOLT2_D = 2.4
CB3_D, CB3_H = 6.4, 3.2   # M3 cap head (3.0 tall) fully recessed, into the pad
CB2_D, CB2_H = 4.8, 2.2   # M2 cap head (2.0 tall) fully recessed

WIN_H = 9.0          # rib windows: lighten, and let cables cross between bays
WIN_Z = 3.0
WIN_CHAMFER = 4.0    # 45 deg corners, so the flat bridge over a window is ~L - 2*C
FLARE_MARGIN = 1.15  # rise / run of the rib-to-flange flare; > 1 keeps it inside 45 deg

TOP_Z = DECK_Z + FLANGE_T


def _slab(w, d, h, at=(0.0, 0.0), z0=0.0):
    return (
        cq.Workplane("XY")
        .box(w, d, h, centered=(True, True, False))
        .translate((at[0], at[1], z0))
    )


def _flare(long_axis, half_len, at, rib_t, flange_w):
    """Flare from rib thickness up to flange width, steeper than 45 deg everywhere."""
    half_r, half_f = rib_t / 2.0, flange_w / 2.0
    z0 = DECK_Z - (half_f - half_r) * FLARE_MARGIN
    pts = [(-half_r, z0), (half_r, z0), (half_f, DECK_Z), (-half_f, DECK_Z)]
    plane = "XZ" if long_axis == "y" else "YZ"
    w = cq.Workplane(plane).polyline(pts).close().extrude(half_len, both=True)
    if long_axis == "y":
        return w.translate((at[0], 0, 0))
    return w.translate((0, at[1], 0))


def _window(long_axis, length, at, centre, rib_t):
    """Hexagonal slot: 45 deg top and bottom corners, so the bridge is short."""
    c = min(WIN_CHAMFER, length / 2.0 - 0.5, WIN_H / 2.0)
    z0, z1 = WIN_Z, WIN_Z + WIN_H
    h = length / 2.0
    pts = [(-h, z0 + c), (-h + c, z0), (h - c, z0), (h, z0 + c),
           (h, z1 - c), (h - c, z1), (-h + c, z1), (-h, z1 - c)]
    plane = "XZ" if long_axis == "y" else "YZ"
    w = cq.Workplane(plane).polyline(pts).close().extrude(rib_t / 2 + 2, both=True)
    if long_axis == "y":
        return w.translate((at, centre, 0))
    return w.translate((centre, at, 0))


def _stadium(width, length, h, at=(0.0, 0.0), z0=0.0, angle=0.0):
    """Flat bar with semicircular ends, the end radii centred on the anchor holes."""
    return (
        cq.Workplane("XY")
        .slot2D(length, width, angle)
        .extrude(h)
        .translate((at[0], at[1], z0))
    )


def _rounded(w, d, h, at=(0.0, 0.0), z0=0.0, r=4.0):
    return (
        cq.Workplane("XY")
        .rect(w, d)
        .extrude(h)
        .edges("|Z")
        .fillet(r)
        .translate((at[0], at[1], z0))
    )


def build_template():
    """Flat fit-check plate: the deck's footprint and hole positions, 3 mm thick."""
    t = FLANGE_T
    parts = []
    for sx in (-1, 1):
        parts.append(_stadium(FLANGE_LONG_W, 2 * RIB_LONG_HALF_Y + FLANGE_LONG_W, t,
                              (sx * RIB_LONG_X, 0), 0.0, angle=90.0))
    for sy in (-1, 1):
        parts.append(_stadium(FLANGE_LAT_W, 2 * RIB_LAT_HALF_X + FLANGE_LAT_W, t,
                              (0, sy * RIB_LAT_Y), 0.0, angle=0.0))
    body = parts[0]
    for q in parts[1:]:
        body = body.union(q)
    holes = ([(x, y, BOLT3_D) for (x, y) in M3_ANCHORS]
             + [(x, y, BOLT2_D) for (x, y) in M2_ANCHORS]
             + [(x, y, FC_BOLT_D) for (x, y) in FC_BOSSES])
    for (x, y, d) in holes:
        body = body.cut(
            cq.Workplane("XY").circle(d / 2).extrude(t + 2).translate((x, y, -1))
        )
    return body


def build():
    parts = []

    # Vertical ribs: a '#' of walls standing on the plate. Printable with no support.
    for sx in (-1, 1):
        parts.append(_slab(WALL_T, 2 * RIB_LONG_HALF_Y, DECK_Z, (sx * RIB_LONG_X, 0)))
    for sy in (-1, 1):
        parts.append(_slab(2 * RIB_LAT_HALF_X, WALL_T, DECK_Z, (0, sy * RIB_LAT_Y)))

    # Deck flanges on top of the ribs.
    for sx in (-1, 1):
        parts.append(
            _stadium(FLANGE_LONG_W, 2 * RIB_LONG_HALF_Y + FLANGE_LONG_W, FLANGE_T,
                     (sx * RIB_LONG_X, 0), DECK_Z, angle=90.0)
        )
    for sy in (-1, 1):
        parts.append(
            _stadium(FLANGE_LAT_W, 2 * RIB_LAT_HALF_X + FLANGE_LAT_W, FLANGE_T,
                     (0, sy * RIB_LAT_Y), DECK_Z, angle=0.0)
        )

    # 45 deg flares from each rib up to its flange.
    for sx in (-1, 1):
        parts.append(_flare("y", RIB_LONG_HALF_Y, (sx * RIB_LONG_X, 0), WALL_T, FLANGE_LONG_W))
    for sy in (-1, 1):
        parts.append(_flare("x", RIB_LAT_HALF_X, (0, sy * RIB_LAT_Y), WALL_T, FLANGE_LAT_W))

    # Anchor pads: full-height columns merged into the ribs, so the bolt head bears on
    # solid material rather than on a 3 mm flange.
    for (x, y) in M3_ANCHORS:
        parts.append(
            cq.Workplane("XY").circle(PAD3_D / 2).extrude(TOP_Z).translate((x, y, 0))
        )
    for (x, y) in M2_ANCHORS:
        parts.append(
            cq.Workplane("XY").circle(PAD2_D / 2).extrude(TOP_Z).translate((x, y, 0))
        )

    # Flight-controller bosses.
    for (x, y) in FC_BOSSES:
        parts.append(
            cq.Workplane("XY")
            .circle(BOSS_D / 2)
            .extrude(BOSS_H)
            .translate((x, y, TOP_Z))
        )

    body = parts[0]
    for p in parts[1:]:
        body = body.union(p)

    # Rib windows.
    wins = []
    for sx in (-1, 1):
        for (cy, ln) in ((0.0, 12.0), (14.0, 12.0), (-14.0, 12.0),
                         (30.5, 12.0), (-30.5, 12.0)):
            wins.append(_window("y", ln, sx * RIB_LONG_X, cy, WALL_T))
    for sy in (-1, 1):
        for (cx, ln) in ((0.0, 12.0), (19.0, 7.0), (-19.0, 7.0)):
            wins.append(_window("x", ln, sy * RIB_LAT_Y, cx, WALL_T))
    for w in wins:
        body = body.cut(w)

    # Anchor bores, counterbored from the deck top.
    for (x, y) in M3_ANCHORS:
        body = body.cut(
            cq.Workplane("XY").circle(BOLT3_D / 2).extrude(TOP_Z + 1).translate((x, y, -0.5))
        )
        body = body.cut(
            cq.Workplane("XY").circle(CB3_D / 2).extrude(CB3_H + 1)
            .translate((x, y, TOP_Z - CB3_H))
        )
    for (x, y) in M2_ANCHORS:
        body = body.cut(
            cq.Workplane("XY").circle(BOLT2_D / 2).extrude(TOP_Z + 1).translate((x, y, -0.5))
        )
        body = body.cut(
            cq.Workplane("XY").circle(CB2_D / 2).extrude(CB2_H + 1)
            .translate((x, y, TOP_Z - CB2_H))
        )

    # Board fixings: clearance right through, head and driver recessed under the deck.
    for (x, y) in FC_BOSSES:
        body = body.cut(
            cq.Workplane("XY").circle(FC_BOLT_D / 2)
            .extrude(TOP_Z + BOSS_H + 1 - FC_HEAD_Z)
            .translate((x, y, FC_HEAD_Z))
        )
        if FC_HEAD_CSK:
            body = body.cut(
                cq.Workplane("XY").circle(FC_HEAD_D / 2).workplane(offset=1.4)
                .circle(FC_BOLT_D / 2).loft()
                .translate((x, y, DECK_Z - 1.4))
            )
            body = body.cut(
                cq.Workplane("XY").circle(FC_HEAD_D / 2)
                .extrude(DECK_Z - 1.4 - FC_HEAD_Z)
                .translate((x, y, FC_HEAD_Z))
            )
        else:
            body = body.cut(
                cq.Workplane("XY").circle(FC_HEAD_D / 2)
                .extrude(DECK_Z - FC_HEAD_Z)
                .translate((x, y, FC_HEAD_Z))
            )

    return body


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    out = args[0] if args else "."
    if "--template" in sys.argv:
        name, r = "h743-deck-fitcheck", build_template()
    else:
        name, r = "h743-deck", build()
    cq.exporters.export(r, f"{out}/{name}.stl", tolerance=0.03, angularTolerance=0.25)
    cq.exporters.export(r, f"{out}/{name}.step")
    bb = r.val().BoundingBox()
    print("bbox  X %.2f..%.2f  Y %.2f..%.2f  Z %.2f..%.2f"
          % (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    print("volume %.1f cm3" % (r.val().Volume() / 1000.0))
