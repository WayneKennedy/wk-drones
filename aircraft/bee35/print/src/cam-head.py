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

Frame: the bar lies along x, centred on the origin, axis on z = 0.

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


PARTS = {"crossbar": crossbar}


def main(outdir="."):
    for name, build in PARTS.items():
        solid = build()
        cq.exporters.export(solid, f"{outdir}/bee35-cam-{name}.stl")
        cq.exporters.export(solid, f"{outdir}/bee35-cam-{name}.step")
        bb = solid.val().BoundingBox()
        print(f"{name}: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
