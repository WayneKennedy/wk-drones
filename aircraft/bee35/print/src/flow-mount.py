"""Bee35 flow-sensor mount: the MicoAir MTF-01P under the VTX heatsink (OQ-05).

The heatsink is the CNC cooling bottom plate of the frame's aluminium head, dead centre
underneath; with no landing gear it is the aircraft's belly (owner, 2026-09-25). It offers
4 x M2 tapped holes on a 20 x 20 mm square with 2 mm free behind them. The sensor hangs
under a plate screwed to those holes, facing straight down, and four corner legs stand a
little proud of its face so the sensor is not what the aircraft lands on.

Frame: z = 0 is the heatsink's face, +z up (into the aircraft), so the whole part is at
z <= 0. x and y are the plate's own axes, and the sensor's long axis is x. The sink's
20 x 20 square sits as a diamond to the airframe, so in the plate it is rotated 45 deg:
one hole on each plate axis, 14.14 mm out. The rotated pattern is still square, so the
plate goes on the sink either way round - that is how the sensor's long axis is set
fore-aft or across, and with it FLOW_ORIENT_YAW.

Assembly: plate to sink first (M2 up into the sink, heads recessed in the plate's
underside), then the sensor up into the plate (M2.5 self-tapping through the sensor's
own holes into the plate's pilots) - the sensor covers the M2 heads once fitted.

Print: plate top face on the bed, legs up (flow-mount-print.stl): every hole is vertical,
nothing overhangs, no supports. PETG: the sensor's alignment is what the flow reads, so
the mount wants to be rigid, and it sits on the heatsink.

Build:  uv run --python 3.12 --with "cadquery>=2.4" python flow-mount.py [outdir]
"""

import sys
import cadquery as cq

# ---------------------------------------------------------------- measured / stated
SINK_PITCH = 20.0     # MEASURED (owner, 2026-09-25): 4 x M2 tapped, 20 x 20 mm square
SINK_ROT_DEG = 45.0   # the square sits as a DIAMOND to the airframe (owner, 2026-09-25,
                      # and the underside photo): one hole forward, one aft, one each
                      # side, 14.14 mm out along each axis. The sensor's long axis is
                      # taken along a plate axis, so the pattern is rotated in the plate
SINK_BEHIND = 2.0     # owner: 2 mm free behind the tapped holes - caps screw protrusion
# MTF-01P, MicoAir's product page (read 2026-09-25), not measured on the unit:
SENSOR_L = 33.2
SENSOR_W = 20.8
SENSOR_H = 16.8       # face to top; the face is the lens/ToF side, pointing down
SENSOR_PITCH = (24.3, 12.0)   # mounting holes, dia 2.5 (clearance), through the sensor
FLOW_FOV_DEG = 42.0   # nothing may enter the cone: half-angle 21 deg

# ---------------------------------------------------------------- chosen
PLATE_T = 3.0         # plate under the sink
M2_CLEAR = 2.2        # clearance for the M2 screws into the sink
M2_HEAD_D = 4.0       # counterbore for a socket/button head, from the plate's underside
M2_HEAD_DEPTH = 2.0   # leaves 1 mm of plate under the head
M25_PILOT = 2.1       # M2.5 self-tapping into plastic, for the sensor's screws
SENSOR_GAP = 1.0      # sensor top held off the plate on four bosses, for its cable and
                      # anything proud of its top face
BOSS_D = 5.0
SENSOR_CLEAR = 0.6    # sensor body to leg, each side
LEG = 4.0             # square legs at the plate's corners
FOOT_PROUD = 3.0      # legs stand this far below the sensor's face
FOOT_CHAMFER = 1.0

import math
SINK_HOLES = [(SINK_PITCH / 2.0 * (math.cos(math.radians(SINK_ROT_DEG + 90 * i))
                                  - math.sin(math.radians(SINK_ROT_DEG + 90 * i))),
               SINK_PITCH / 2.0 * (math.sin(math.radians(SINK_ROT_DEG + 90 * i))
                                  + math.cos(math.radians(SINK_ROT_DEG + 90 * i))))
              for i in range(4)]            # the 20 x 20 square's corners, rotated
HOLE_WALL = 1.0       # plate material outside a counterbore
_reach = max(max(abs(x), abs(y)) for x, y in SINK_HOLES) + M2_HEAD_D / 2.0 + HOLE_WALL
PX = max(SENSOR_L / 2.0 + SENSOR_CLEAR + LEG, _reach)   # plate half-size, x
PY = max(SENSOR_W / 2.0 + SENSOR_CLEAR + LEG, _reach)   # plate half-size, y
Z_PLATE_BOT = -PLATE_T
Z_SENSOR_TOP = Z_PLATE_BOT - SENSOR_GAP
Z_SENSOR_FACE = Z_SENSOR_TOP - SENSOR_H
Z_FOOT = Z_SENSOR_FACE - FOOT_PROUD


def _box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def mount():
    body = _box(-PX, PX, -PY, PY, Z_PLATE_BOT, 0.0)
    # sensor bosses on the underside, at the sensor's pattern
    hx, hy = SENSOR_PITCH[0] / 2.0, SENSOR_PITCH[1] / 2.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.union(cq.Workplane("XY").circle(BOSS_D / 2.0)
                              .extrude(SENSOR_GAP).translate((sx * hx, sy * hy, Z_SENSOR_TOP)))
    # legs at the four corners, down past the sensor's face
    for sx in (-1, 1):
        for sy in (-1, 1):
            x0, x1 = sorted((sx * PX, sx * (PX - LEG)))
            y0, y1 = sorted((sy * PY, sy * (PY - LEG)))
            body = body.union(_box(x0, x1, y0, y1, Z_FOOT, Z_PLATE_BOT))
    if FOOT_CHAMFER:
        body = body.faces("<Z").chamfer(FOOT_CHAMFER)
    # M2 through the plate into the sink, heads recessed from below
    for x, y in SINK_HOLES:
        body = body.cut(cq.Workplane("XY").circle(M2_CLEAR / 2.0).extrude(PLATE_T + 1)
                        .translate((x, y, Z_PLATE_BOT - 0.5)))
        body = body.cut(cq.Workplane("XY").circle(M2_HEAD_D / 2.0).extrude(M2_HEAD_DEPTH)
                        .translate((x, y, Z_PLATE_BOT)))
    # M2.5 pilots for the sensor, up through the bosses into the plate
    for sx in (-1, 1):
        for sy in (-1, 1):
            body = body.cut(cq.Workplane("XY").circle(M25_PILOT / 2.0)
                            .extrude(SENSOR_GAP + PLATE_T - 0.8)
                            .translate((sx * hx, sy * hy, Z_SENSOR_TOP)))
    return body


def main(outdir="."):
    m = mount()
    cq.exporters.export(m, f"{outdir}/bee35-flow-mount.stl")
    cq.exporters.export(m, f"{outdir}/bee35-flow-mount.step")
    bb = m.val().BoundingBox()
    print(f"flow-mount: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm, z {bb.zmin:.2f}..{bb.zmax:.2f};"
          f" sensor face at z {Z_SENSOR_FACE:.1f}, feet at {Z_FOOT:.1f}")
    print("sink holes:", [(round(x, 2), round(y, 2)) for x, y in SINK_HOLES])
    cone_r = FOOT_PROUD * math.tan(math.radians(FLOW_FOV_DEG / 2.0))
    print(f"flow cone radius at the feet: {cone_r:.2f} mm; nearest leg face "
          f"{min(SENSOR_L / 2.0, SENSOR_W / 2.0) + SENSOR_CLEAR:.1f} mm from the sensor centre")
    # print orientation: top face on the bed, legs up
    printed = m.rotate((0, 0, 0), (1, 0, 0), 180)
    printed = printed.translate((0, 0, -printed.val().BoundingBox().zmin))
    cq.exporters.export(printed, f"{outdir}/bee35-flow-mount-print.stl")
    # elevations, z up: front = looking along -y; side = looking along -x; and an iso
    views = {
        "front": m.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 1, 0), 180),
        "side": m.rotate((0, 0, 0), (0, 0, 1), -90).rotate((0, 0, 0), (1, 0, 0), -90),
        "iso": m.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 1, 0), 180)
                .rotate((0, 0, 0), (0, 1, 0), -30).rotate((0, 0, 0), (1, 0, 0), 25),
        "below": m.rotate((0, 0, 0), (1, 0, 0), 180),
    }
    for view, solid in views.items():
        cq.exporters.export(
            solid, f"{outdir}/bee35-flow-mount-{view}.svg",
            opt={"projectionDir": (0, 0, 1), "showAxes": False, "strokeWidth": 0.25,
                 "width": 500, "height": 500, "marginLeft": 20, "marginTop": 20},
        )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
