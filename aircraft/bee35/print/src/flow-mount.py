"""Bee35 flow-sensor mount: the MicoAir MTF-01P under the nose on three screws (OQ-05).

Three fastenings (owner, 2026-09-25): two M3 at the front, 24 mm apart, and the VTX
heatsink's forward M2 behind them, 41 mm from each front hole. The sensor faces straight
down from a plate on those three.

Frame (owner's datum): origin midway between the two front holes; x along the line
through them, so they sit at (+/-12, 0); z = 0 is the surface they bear on, +z AWAY from
the airframe - down in flight, up on the inverted bench. y is perpendicular in that
plane, +y toward the third hole, which is aft: sqrt(41^2 - 12^2) = 39.2 mm. All three
holes are taken as coplanar for now (owner: "say it's z = 0 too").

Sensor: long axis across (x), centred behind the front holes so their heads stay clear
of it, on four 1 mm bosses at its 24.3 x 12 pattern, M2.5 self-tapping through its own
holes. Its face ends up PLATE_T + SENSOR_GAP + SENSOR_H = 20.8 mm off the mounting
surface. FLOW_POS_X/Y follow from where this surface is relative to the CG.

Print: mounting face on the bed, bosses up. Every hole vertical, no overhangs, no
supports. PETG - alignment is what the flow reads.

Build:  uv run --python 3.12 --with "cadquery>=2.4" python flow-mount.py [outdir]
"""

import math
import sys
import cadquery as cq

# ---------------------------------------------------------------- measured / stated
FRONT_PITCH = 24.0    # MEASURED (owner, 2026-09-25): the two front holes, centres
FRONT_HOLE = 3.4      # M3 clearance (owner: M3 clearance holes in the frame)
THIRD_REACH = 41.0    # MEASURED (owner): third hole to each front hole
THIRD_HOLE = 2.2      # M2 clearance - the heatsink's forward tapped M2 (owner, earlier)
THIRD_Z = 0.0         # owner: coplanar with the front two, for now
# MTF-01P, MicoAir's product page (read 2026-09-25), not measured on the unit:
SENSOR_L = 33.2
SENSOR_W = 20.8
SENSOR_H = 16.8       # face to top; the face is the lens/ToF side
SENSOR_PITCH = (24.3, 12.0)   # mounting holes, dia 2.5 (clearance), through the sensor
FLOW_FOV_DEG = 42.0

# ---------------------------------------------------------------- chosen
PLATE_T = 3.0
EDGE = 2.5            # plate material outside any hole or the sensor body
SENSOR_Y = 18.5       # sensor centre, aft of the front holes: its front edge sits
                      # SENSOR_W/2 + EDGE + FRONT_HOLE/2 + ... clear of the M3 heads
SENSOR_GAP = 1.0      # sensor top held off the plate on bosses, for cable and connector
BOSS_D = 5.0
M25_PILOT = 2.1
CORNER_R = 3.0

FRONT_HOLES = [(-FRONT_PITCH / 2.0, 0.0), (FRONT_PITCH / 2.0, 0.0)]
THIRD_Y = math.sqrt(THIRD_REACH ** 2 - (FRONT_PITCH / 2.0) ** 2)
THIRD = (0.0, THIRD_Y)


def _outline():
    """Plate outline: full width over the sensor, front holes in the corners, a tab aft
    to the third hole."""
    hw = SENSOR_L / 2.0 + EDGE                 # half-width where the sensor is
    hw = max(hw, FRONT_PITCH / 2.0 + FRONT_HOLE / 2.0 + EDGE)
    y_front = -(FRONT_HOLE / 2.0 + EDGE)
    y_sensor_aft = SENSOR_Y + SENSOR_W / 2.0 + EDGE
    tab = THIRD_HOLE / 2.0 + EDGE + 1.0
    pts = [(-hw, y_front), (hw, y_front), (hw, y_sensor_aft),
           (tab, THIRD_Y), (tab, THIRD_Y + tab), (-tab, THIRD_Y + tab), (-tab, THIRD_Y),
           (-hw, y_sensor_aft)]
    return cq.Workplane("XY").polyline(pts).close().extrude(PLATE_T)


def mount():
    body = _outline()
    if CORNER_R:
        body = body.edges("|Z").fillet(CORNER_R)
    # sensor bosses on the +z face
    hx, hy = SENSOR_PITCH[0] / 2.0, SENSOR_PITCH[1] / 2.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.union(cq.Workplane("XY").circle(BOSS_D / 2.0).extrude(SENSOR_GAP)
                              .translate((sx * hx, SENSOR_Y + sy * hy, PLATE_T)))
    # the three airframe holes, through
    for (x, y), d in [(h, FRONT_HOLE) for h in FRONT_HOLES] + [(THIRD, THIRD_HOLE)]:
        body = body.cut(cq.Workplane("XY").circle(d / 2.0).extrude(PLATE_T + SENSOR_GAP + 1)
                        .translate((x, y, -0.5)))
    # M2.5 pilots for the sensor, from the boss tops down into the plate
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.cut(cq.Workplane("XY").circle(M25_PILOT / 2.0)
                            .extrude(SENSOR_GAP + PLATE_T - 0.8)
                            .translate((sx * hx, SENSOR_Y + sy * hy, 0.8)))
    return body


def main(outdir="."):
    m = mount()
    cq.exporters.export(m, f"{outdir}/bee35-flow-mount.stl")
    cq.exporters.export(m, f"{outdir}/bee35-flow-mount.step")
    cq.exporters.export(m, f"{outdir}/bee35-flow-mount-print.stl")   # already bed-down
    bb = m.val().BoundingBox()
    print(f"flow-mount: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm;"
          f" x {bb.xmin:.1f}..{bb.xmax:.1f}, y {bb.ymin:.1f}..{bb.ymax:.1f}")
    print(f"third hole at (0, {THIRD_Y:.2f}); sensor centre (0, {SENSOR_Y}),"
          f" footprint x +/-{SENSOR_L/2:.1f}, y {SENSOR_Y - SENSOR_W/2:.1f}..{SENSOR_Y + SENSOR_W/2:.1f};"
          f" face {PLATE_T + SENSOR_GAP + SENSOR_H:.1f} mm off the mounting surface")
    views = {
        "plan": m.rotate((0, 0, 0), (1, 0, 0), 180).rotate((0, 0, 0), (0, 0, 1), 180),
                 # the mounting face, x to the right, aft (the third hole) up the page
        "front": m.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 1, 0), 180),
        "side": m.rotate((0, 0, 0), (0, 0, 1), -90).rotate((0, 0, 0), (1, 0, 0), -90),
        "iso": m.rotate((0, 0, 0), (0, 1, 0), -30).rotate((0, 0, 0), (1, 0, 0), -55),
    }
    for view, solid in views.items():
        cq.exporters.export(
            solid, f"{outdir}/bee35-flow-mount-{view}.svg",
            opt={"projectionDir": (0, 0, 1), "showAxes": False, "strokeWidth": 0.25,
                 "width": 500, "height": 500, "marginLeft": 20, "marginTop": 20},
        )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
