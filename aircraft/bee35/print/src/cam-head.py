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
from the bottom for M3 self-tapping. They carry the camera-holding part.

Part 3 - `mount`: the whole head as one print. A box between the plates - two cheeks, a
floor, a roof - with the crossbar embedded flush in the roof, the camera hung on M2
screws through the cheeks, and the posts shortened under the floor. The crossbar's two
ends and the two post bottoms are the only mounting points.

Frame: x is across the aircraft, plate to plate, and the crossbar lies along it, centred
on the origin with its axis on z = 0. +y is forward (the nose), +z is up. The side plates'
inner faces are therefore at x = +/-PLATE_GAP/2.

Print: the bare crossbar on its side, so the screw threads run ACROSS the layers rather
than pulling them apart - a screw driven along the layer axis splits a printed part. The
one-piece mount face-down, front face on the bed (bee35-cam-mount-print.stl): bar and
posts then lie horizontal, but the arch's front half overhangs for its first ~5.5 mm and
needs supports from the bed there.
Material: PETG or similar rigid filament keeps the plate spacing under screw preload; TPU
gives a damped camera but makes the embedded crossbar the soft link. Owner's call.

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

# Camera pocket (part 3), 2026-09-25. Holds a standard 19 mm camera - the Walksnail Nano V3
# in its TPU adapter - facing forward, hung on its two side screws between two cheeks.
# UNMEASURED, all of it: these are the assumptions to check against the camera in hand.
POCKET_W = 19.0     # gap between the cheeks (owner, 2026-09-25). The camera sits in it
                    # with no side clearance; the cheeks' OUTER faces are fixed by the
                    # plates, so the cheeks are what is left: 2.85 mm
CAM_H = 19.0        # body height (standard micro-camera face)
CAM_PIVOT_D = 2.2   # clearance for the M2 screws into the camera's threaded side holes
CAM_PIVOT_BACK = 5.0  # pivot axis behind the camera's front face - the number most likely
                      # to be wrong; measure it on the adapter
POCKET_V_CLEAR = 1.0  # extra above and below the body, so it can tilt on its pivots
CAM_Z = -14.75      # pivot axis height. "About half way" down the 31.5 mm mounting area
                    # (-15.75), raised 1 mm so the body top clears the crossbar by 1.5
CAM_FACE_Y = POST_AHEAD + BAR_OD / 2.0   # front face flush with the posts' front (y = 11)
POCKET_DEPTH = 20.0  # cheeks and floor run this far aft of the face; the body passes
                     # under the crossbar and the back is open for the cable
PLATE_CLEAR = 0.4   # each cheek's outer face to the plate's inner face
FLOOR_T = 2.0       # floor under the pocket, joining the cheeks and carrying the posts
# The top, owner's sketch 2026-09-25: in side view each cheek is an ARCH over the crossbar,
# springing from part-way down the cheek at the front and back edges and cresting just
# above the bar. Modelled as a semi-ellipse centred mid-depth: half-width half the pocket
# depth, so it lands on both edges, and tall enough to clear the bar's top by ARCH_MARGIN
# at the bar's own y (the bar is not quite mid-depth). Between the cheeks the same arch
# forms a roof over the bar, solid down to the pocket ceiling, and is open where the arch
# drops below the ceiling toward the front and back.
ARCH_BASE = -16.0   # where the arch springs from, on the front and back edges (sketch:
                    # about -14 at the back, -18 at the front; taken symmetric)
ARCH_MARGIN = 0.3   # arch above the bar's top, at the bar


def _box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


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
    if depth <= 0:
        return bar
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


def mount():
    """The whole thing as one printed part: crossbar, camera pocket, floor and posts.

    Two arched cheeks joined by a floor, with the crossbar embedded in the arch's crown
    and a roof between the cheeks where the arch stands above the pocket ceiling. The
    camera hangs on M2 screws through the cheeks. The posts are shortened to sit under the
    floor - at their original 10 mm their tops would be inside the camera body.
    """
    cheek_out = PLATE_GAP / 2.0 - PLATE_CLEAR
    cheek_in = POCKET_W / 2.0
    if cheek_out - cheek_in < 1.5:
        print(f"WARNING: cheeks only {cheek_out - cheek_in:.2f} mm thick", file=sys.stderr)
    y_face = CAM_FACE_Y
    y_back = y_face - POCKET_DEPTH
    z_floor_top = CAM_Z - CAM_H / 2.0 - POCKET_V_CLEAR
    z_floor_bot = z_floor_top - FLOOR_T
    z_ceil = CAM_Z + CAM_H / 2.0 + POCKET_V_CLEAR   # pocket ceiling, the roof's underside
    post_len = z_floor_bot + POST_DROP           # from the mounting face up to the floor
    pilot_depth = min(POST_PILOT_DEPTH, post_len + FLOOR_T - 2.0)

    # side profile: a rectangle up to the arch base, with a semi-ellipse on top. The
    # ellipse is sized so that at the bar's y (0) it clears the bar's top by ARCH_MARGIN.
    y_c = (y_back + y_face) / 2.0
    a = POCKET_DEPTH / 2.0
    top_at_bar = BAR_OD / 2.0 + ARCH_MARGIN
    b = (top_at_bar - ARCH_BASE) / (1.0 - (y_c / a) ** 2) ** 0.5
    width = 2 * cheek_out
    rect = (cq.Workplane("YZ").center(y_c, (z_floor_bot + ARCH_BASE) / 2.0)
            .rect(POCKET_DEPTH, ARCH_BASE - z_floor_bot).extrude(width / 2.0, both=True))
    arch = (cq.Workplane("YZ").center(y_c, ARCH_BASE).ellipse(a, b)
            .extrude(width / 2.0, both=True))
    body = rect.union(arch).intersect(
        _box(-cheek_out, cheek_out, y_back, y_face, z_floor_bot, ARCH_BASE + b + 1))
    # the pocket: open front and back, ceiling at z_ceil - so the roof exists only where
    # the arch stands above the ceiling, over the bar
    body = body.cut(_box(-cheek_in, cheek_in, y_back - 1, y_face + 1, z_floor_top, z_ceil))
    body = body.union(crossbar())
    x_post = PLATE_GAP / 2.0 - POST_INSET
    for sx in (-1, 1):
        body = body.union(post(post_len, depth=0, chamfer=0)
                          .translate((sx * x_post, POST_AHEAD, -POST_DROP)))
        # post pilots, blind from the mounting face, cut after the union so they are
        # not filled in by the floor
        body = body.cut(cq.Workplane("XY").circle(PILOT_D / 2.0).extrude(pilot_depth)
                        .translate((sx * x_post, POST_AHEAD, -POST_DROP)))
    # camera pivots: one M2 clearance hole through each cheek, on the camera's axis
    body = body.cut(cq.Workplane("YZ").center(y_face - CAM_PIVOT_BACK, CAM_Z)
                    .circle(CAM_PIVOT_D / 2.0).extrude(PLATE_GAP, both=True))
    # the crossbar's own pilot, re-cut through the cheeks it now passes through
    body = body.cut(cq.Workplane("YZ").circle(PILOT_D / 2.0).extrude(PLATE_GAP, both=True))
    return body


PARTS = {"crossbar": crossbar, "post": post, "posts": posts, "assembly": assembly,
         "mount": mount}


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
    # print-oriented STL: front face on the bed (owner, 2026-09-25). Rotating -90 about x
    # puts +y (the nose) at -z; shifted so the bed is z = 0. NOTE the arch's front half
    # then overhangs - it springs from the front edge tangentially, so its surface starts
    # nearly parallel to the bed and only steepens to 45 deg about 5.5 mm up. Slice with
    # supports from the bed on that slope, or spring the arch at an angle (widen it).
    printed = mount().rotate((0, 0, 0), (1, 0, 0), -90)
    printed = printed.translate((0, 0, -printed.val().BoundingBox().zmin))
    cq.exporters.export(printed, f"{outdir}/bee35-cam-mount-print.stl")
    bb = printed.val().BoundingBox()
    print(f"mount-print (front face down): {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm,"
          f" z {bb.zmin:.2f}..{bb.zmax:.2f}")
    for name in ("assembly", "mount"):
        a = PARTS[name]()
        views = {
            "front": a.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 1, 0), 180),
            "side": a.rotate((0, 0, 0), (0, 0, 1), -90).rotate((0, 0, 0), (1, 0, 0), -90),
            "iso": a.rotate((0, 0, 0), (1, 0, 0), -90).rotate((0, 0, 0), (0, 1, 0), 180)
                    .rotate((0, 0, 0), (0, 1, 0), -30).rotate((0, 0, 0), (1, 0, 0), 25),
        }
        for view, solid in views.items():
            cq.exporters.export(
                solid, f"{outdir}/bee35-cam-{name}-{view}.svg",
                opt={"projectionDir": (0, 0, 1), "showAxes": False, "strokeWidth": 0.25,
                     "width": 500, "height": 500, "marginLeft": 20, "marginTop": 20},
            )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
