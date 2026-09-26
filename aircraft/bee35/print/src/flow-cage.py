"""Bee35 flow-sensor cage: a TPU strap over the MTF-01P, taped to the VTX heatsink (OQ-05).

Owner's scheme, 2026-09-26: the sensor is stuck to the heatsink's face with strong gel
tape, dead centre, long axis across the aircraft, face down. This TPU part goes over it
and is screwed to the sink's FORE and AFT M2 holes only - the two on the centreline -
because the sensor's 33 mm length covers the other two. The tape locates the sensor and
carries flight loads; the cage carries landing and peel loads, which tape is bad at,
and stops a failed bond costing the sensor.

Shape: a ring around the sensor's four sides, a narrow lip turned in over the edges of
its face (the optics stay open), and a tab fore and aft lying on the sink with an M2
clearance hole. The lip's underside is a 45 deg slope so it prints without support.

Frame: sensor centre on the sink at the origin; x across the aircraft (the sensor's
long axis), y fore-aft, z = 0 the sink's face, +z away from the sink - down in flight.
The sink's M2s are on a 20 x 20 square set as a diamond, so the fore and aft ones are
at (0, +/-14.14).

Print: sink side down, tabs on the bed, ring rising, lip last. TPU 95A, the fleet's
calibrated `tpu` profile. No supports.

Build:  uv run --python 3.12 --with "cadquery>=2.4" python flow-cage.py [outdir]
"""

import math
import sys
import cadquery as cq

# ---------------------------------------------------------------- measured / stated
SINK_PITCH = 20.0        # MEASURED (owner): 4 x M2 tapped on a 20 x 20 square
SINK_ROT_DEG = 45.0      # set as a diamond to the airframe (owner, underside photo)
M2_HOLE = 2.2            # clearance
# MTF-01P, MicoAir's product page (read 2026-09-25), not measured on the unit:
SENSOR_L = 33.2          # across the aircraft
SENSOR_W = 20.8          # fore-aft
SENSOR_H = 16.8          # sink side to face

# ---------------------------------------------------------------- chosen
TAPE_T = 1.0             # gel tape between sink and sensor - measure the tape
FIT = 0.3                # cage to sensor, each side; TPU stretches, keep it snug
WALL = 1.5               # ring wall
LIP = 2.0                # how far the lip turns in over the face's edges
LIP_T = 1.5              # lip thickness, above the face
TAB_W = 8.0              # tab width, across
TAB_T = 1.5              # tab thickness, on the sink
TAB_END = 3.0            # tab material beyond the M2 hole
M2_HEAD_D = 3.8          # button/socket head, for the recess below
M2_HEAD_H = 2.0
HEAD_ROOM = 0.6          # recess into the ring's outer face at each tab, so the head
                         # seats: at y = 14.14 a 3.8 head reaches to 12.24 and the ring's
                         # outer face is at 12.2
CORNER_R = 2.0           # ring's outer vertical corners

M2_Y = SINK_PITCH / 2.0 * math.sqrt(2.0)          # 14.14: fore and aft holes on x = 0
IX, IY = SENSOR_L / 2.0 + FIT, SENSOR_W / 2.0 + FIT   # inside of the ring
OX, OY = IX + WALL, IY + WALL                          # outside of the ring
Z_FACE = TAPE_T + SENSOR_H                             # sensor's face
Z_TOP = Z_FACE + LIP_T


def _box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def cage():
    if M2_Y - M2_HOLE / 2.0 - OY < 0.8:
        print(f"WARNING: only {M2_Y - M2_HOLE/2 - OY:.2f} mm between the ring and the "
              f"M2 hole", file=sys.stderr)
    # ring with lip: a solid block, corners rounded, cavity for the sensor, window in the lip
    body = _box(-OX, OX, -OY, OY, 0.0, Z_TOP)
    if CORNER_R:
        body = body.edges("|Z").fillet(CORNER_R)
    body = body.cut(_box(-IX, IX, -IY, IY, -1.0, Z_FACE))              # sensor cavity
    body = body.cut(_box(-(IX - LIP), IX - LIP, -(IY - LIP), IY - LIP,  # lip window
                         Z_FACE - 1.0, Z_TOP + 1.0))
    # 45 deg under the lip: loft from the cavity outline up to the window outline
    slope = (cq.Workplane("XY").workplane(offset=Z_FACE - LIP)
             .rect(2 * IX, 2 * IY)
             .workplane(offset=LIP).rect(2 * (IX - LIP), 2 * (IY - LIP))
             .loft(combine=True))
    body = body.cut(slope)
    # tabs fore and aft, on the sink, with the M2 holes
    for sy in (-1, 1):
        y_in, y_out = sy * OY, sy * (M2_Y + TAB_END)
        tab = _box(-TAB_W / 2.0, TAB_W / 2.0, min(y_in, y_out), max(y_in, y_out), 0.0, TAB_T)
        if CORNER_R:
            tab = tab.edges("|Z").fillet(min(CORNER_R, TAB_W / 2.0 - 0.1))
        body = body.union(tab)
        body = body.cut(cq.Workplane("XY").circle(M2_HOLE / 2.0).extrude(TAB_T + 2)
                        .translate((0.0, sy * M2_Y, -1.0)))
        # head recess: the ring's outer face, at the tab, thinned by HEAD_ROOM up to the
        # head's height, so the screw head sits flat on the tab
        hr = M2_HEAD_D / 2.0 + 0.3
        y0, y1 = sorted((sy * (OY - HEAD_ROOM), sy * (OY + 0.5)))
        body = body.cut(_box(-hr, hr, y0, y1, TAB_T, TAB_T + M2_HEAD_H + 0.5))
    return body


def main(outdir="."):
    m = cage()
    for ext in ("stl", "step"):
        cq.exporters.export(m, f"{outdir}/bee35-flow-cage.{ext}")
    cq.exporters.export(m, f"{outdir}/bee35-flow-cage-print.stl")     # already bed-down
    bb = m.val().BoundingBox()
    print(f"flow-cage: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm; ring outside "
          f"{2*OX:.1f} x {2*OY:.1f}, window {2*(IX-LIP):.1f} x {2*(IY-LIP):.1f}, "
          f"face at z {Z_FACE:.1f}, top {Z_TOP:.1f}; M2 at y +/-{M2_Y:.2f}, "
          f"{M2_Y - M2_HOLE/2 - OY:.2f} mm clear of the ring; head edge at "
          f"{M2_Y - M2_HEAD_D/2:.2f} vs recessed face at {OY - HEAD_ROOM:.2f}")
    views = {
        "plan": m,                                                         # from +z: the face side
        "front": m.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 1, 0), 180),
        "side": m.rotate((0, 0, 0), (0, 0, 1), -90).rotate((0, 0, 0), (1, 0, 0), -90),
        "iso": m.rotate((0, 0, 0), (0, 1, 0), -30).rotate((0, 0, 0), (1, 0, 0), -55),
    }
    for view, solid in views.items():
        cq.exporters.export(
            solid, f"{outdir}/bee35-flow-cage-{view}.svg",
            opt={"projectionDir": (0, 0, 1), "showAxes": False, "strokeWidth": 0.25,
                 "width": 500, "height": 500, "marginLeft": 20, "marginTop": 20},
        )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
