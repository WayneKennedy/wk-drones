"""Bee35 camera head parts, printed, to replace the mislaid CNC hardware (OQ-04).

The aircraft keeps its two aluminium head side plates; what is missing is the 25.5 mm
aluminium standoff and the four camera vibration damping balls (SpeedyBee's O4 Air Unit
Pro aluminium head module tutorial, ../sources.md). This file builds the printed parts
that replace them. Parts are added as the geometry is measured off the airframe; each is
a function returning a solid, and every dimension that came off the hardware is marked
MEASURED.

Part 1 - `crossbar`: a plain round bar spanning the two side plates, taking an M3
self-tapping screw into each end through the plates' own M3-clearance holes (the ones the
damping balls would have used). It sets the plate spacing, which is the standoff's job.

Part 2 - `posts`: two vertical bars hanging below and ahead of the crossbar, pilot-holed
from the bottom for M3 self-tapping. They carry the camera-holding part, still to come.

Frame: x is across the aircraft, plate to plate, and the crossbar lies along it, centred
on the origin with its axis on z = 0. +y is forward (the nose), +z is up. The side plates'
inner faces are therefore at x = +/-PLATE_GAP/2.

Print: on its side, so the screw threads run ACROSS the layers rather than pulling them
apart - a screw driven along the layer axis splits a printed part. No supports.
Material: PETG or similar rigid filament, NOT TPU: this part sets a spacing under screw
preload, and TPU creeps. The damping belongs in the camera-holding part, not here.

Build:  uv run --python 3.12 --with "cadquery>=2.4" python cam-head.py [outdir]
Needs:  cadquery >= 2.4
"""

import sys
import cadquery as cq

# ---------------------------------------------------------------- measured inputs
PLATE_GAP = 25.5   # MEASURED (owner, callipers, 2026-09-25): inner face to inner face of
                   # the two aluminium side plates, and the length of the missing standoff

# ---------------------------------------------------------------- chosen
BAR_OD = 7.0       # owner's choice
PILOT_D = 2.5      # pilot for an M3 self-tapping screw into plastic; runs right through,
                   # so the bar prints without a bridge and takes any screw length
END_CHAMFER = 0.3  # eases the bar between the plates and kills the first-layer elephant's
                   # foot where it would hold the part off the plate face

# Posts (part 2), owner's geometry 2026-09-25. Both offsets are read as AXIS positions:
# the post axis sits POST_INSET inboard of a plate's inner face and POST_AHEAD forward of
# the crossbar's axis. If either was meant to the post's SURFACE instead, subtract BAR_OD/2.
POST_LEN = 10.0     # variable, starts here
POST_DROP = 31.5    # bottom face of each post, below the crossbar's centre line
POST_AHEAD = 7.5    # forward of the crossbar's axis
POST_INSET = 4.5    # inboard of each plate's inner face
POST_PILOT_DEPTH = 8.0   # blind, up from the bottom face; leaves 2 mm at POST_LEN = 10


def crossbar(length=PLATE_GAP, od=BAR_OD, pilot=PILOT_D, chamfer=END_CHAMFER):
    """Round bar, axis along x, centred on the origin."""
    bar = (
        cq.Workplane("YZ")
        .circle(od / 2.0)
        .extrude(length / 2.0, both=True)
    )
    if chamfer:
        bar = bar.faces(">X or <X").chamfer(chamfer)
    return bar.faces(">X").workplane().circle(pilot / 2.0).cutThruAll()


def post(length=POST_LEN, od=BAR_OD, pilot=PILOT_D, depth=POST_PILOT_DEPTH,
         chamfer=END_CHAMFER):
    """One vertical bar, axis along z, bottom face on z = 0, pilot blind from the bottom."""
    bar = cq.Workplane("XY").circle(od / 2.0).extrude(length)
    if chamfer:
        bar = bar.faces(">Z or <Z").chamfer(chamfer)
    return bar.faces("<Z").workplane().circle(pilot / 2.0).cutBlind(-min(depth, length))


def posts(length=POST_LEN, **kw):
    """Both posts, in place: bottoms POST_DROP below the crossbar axis, ahead and inboard."""
    x = PLATE_GAP / 2.0 - POST_INSET
    one = post(length, **kw)
    return (
        one.translate((-x, POST_AHEAD, -POST_DROP))
        .union(one.translate((x, POST_AHEAD, -POST_DROP)))
    )


def assembly(post_length=POST_LEN):
    """Crossbar and both posts in their flying positions - for checking geometry, not print."""
    return crossbar().union(posts(post_length))


PARTS = {"crossbar": crossbar, "post": post, "posts": posts, "assembly": assembly}


def main(outdir="."):
    for name, build in PARTS.items():
        solid = build()
        cq.exporters.export(solid, f"{outdir}/bee35-cam-{name}.stl")
        cq.exporters.export(solid, f"{outdir}/bee35-cam-{name}.step")
        bb = solid.val().BoundingBox()
        print(f"{name}: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm"
              f"  (x {bb.xmin:.2f}..{bb.xmax:.2f}, y {bb.ymin:.2f}..{bb.ymax:.2f},"
              f" z {bb.zmin:.2f}..{bb.zmax:.2f})")
    # Elevations. CadQuery's SVG export projects along the given direction with no say
    # over which way is "up", so the assembly is rotated into the default (+z) view
    # instead: front = viewer ahead of the nose looking aft, z up, +x to the viewer's
    # left; side = viewer on the +x side looking inboard, z up, nose to the right.
    a = assembly()
    views = {
        "front": a.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 1, 0), 180),
        "side": a.rotate((0, 0, 0), (0, 0, 1), -90).rotate((0, 0, 0), (1, 0, 0), -90),
    }
    for view, solid in views.items():
        cq.exporters.export(
            solid, f"{outdir}/bee35-cam-assembly-{view}.svg",
            opt={"projectionDir": (0, 0, 1), "showAxes": False, "strokeWidth": 0.25,
                 "width": 500, "height": 500, "marginLeft": 20, "marginTop": 20},
        )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
