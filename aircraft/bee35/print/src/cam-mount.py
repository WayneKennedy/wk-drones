"""Bee35 camera mount: the whole head as one print, replacing the mislaid CNC hardware (OQ-04).

FreeCAD script (fleet F-DEC-09, F-DEC-10). It builds `cam-mount.FCStd` beside itself - a
`Params` spreadsheet and a PartDesign body bound to it by expression - and exports the
STL, STEP and SVG views to `../stl/`. This script is the source; the FCStd is what it
emits. Change a value in the spreadsheet to try it; put the agreed value back HERE and
rebuild. Remodelled 2026-09-29 from `mount()` in cam-head.py (CadQuery, last at
`fef5c14`), which still holds the loose crossbar and posts.

The aircraft keeps its two aluminium head side plates; what is missing is the 25.5 mm
aluminium standoff and the four camera vibration damping balls (SpeedyBee's O4 Air Unit
Pro aluminium head module tutorial, ../sources.md). This part replaces them: two arched
cheeks joined by a floor, a crossbar embedded in the arch's crown and a roof between the
cheeks where the arch stands above the pocket's ceiling, and two posts under the floor.
The camera hangs on M2 screws through the cheeks; front and back are open. The
crossbar's two ends and the two post bottoms are the only mounting points: M3
self-tapping through the plates into the bar, and up into the posts.

Frame: x is across the aircraft, plate to plate, and the crossbar lies along it, centred
on the origin with its axis on z = 0. +y is forward (the nose), +z is up. The side
plates' inner faces are at x = +/-PLATE_GAP/2.

The top, owner 2026-09-29: in side view each cheek is rounded over the crossbar. A cap,
a circle about the bar's own axis and ARCH_MARGIN outside the bar, is met on each side
by an arc that springs from ARCH_BASE on the front or back edge, leaving the edge
vertically and running tangent into the cap. So the rim round the bar's end is even.
Until then the top was one semi-ellipse over the whole depth (owner's sketch,
2026-09-25), which fitted the bar only while the bar was near mid-depth.

Print: front face on the bed (owner, 2026-09-25; `bee35-cam-mount-print.stl`). Bar and
posts then lie horizontal, so their screws thread across the layers. The arch springs
from the front edge tangentially, so the front of the top overhangs for its first ~4.8 mm
(where its slope reaches 45 deg, on the cap). In TPU that prints without supports: the
first print did, 2026-09-29 (../sources.md). Not tried in a rigid filament.

Build: run this file as __main__ inside FreeCAD, with __file__ set (rules and the reasons
for this form: /AGENTS.md "CAD in FreeCAD").
    RUN="p='$PWD/cam-mount.py'; exec(compile(open(p).read(), p, 'exec'), {'__file__': p, '__name__': '__main__'})"
  in the GUI, so the part is seen being made: paste the quoted Python into the Python
    console, or send it through the FreeCAD MCP;
  headless:  flatpak run --command=FreeCADCmd org.freecad.FreeCAD -c "$RUN"
Needs: FreeCAD 1.1 (built and checked on 1.1.3); /fleet/cad/fcpart.py.
"""

import importlib
import math
import os
import sys

import Part
import Sketcher
from FreeCAD import Vector as V

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "../../../../fleet/cad")))
import fcpart                                                          # noqa: E402
importlib.reload(fcpart)
from fcpart import X, Y, Z, add_circle, add_rect, at_x, at_y, dim, new_sketch, val  # noqa: E402

DOC = "cam_mount"
PART = "bee35-cam-mount"

# (alias, value or formula, note). Every value carries its unit; formulas start with "=".
PARAMS = [
    # ------------------------------------------------------------ measured
    ("PLATE_GAP", "25.5 mm", "MEASURED (owner, callipers, 2026-09-25): inner face to inner "
                             "face of the two side plates; the missing standoff's length"),
    ("POST_DROP", "31.5 mm", "MEASURED (owner, 2026-09-25): post bottoms below the crossbar axis"),
    ("POST_AHEAD", "4 mm", "post axis forward of the crossbar axis (owner, 2026-09-29, off "
                           "the first print: posts 3.5 mm aft). 7.5 until then, the "
                           "2026-09-25 measurement read as an axis position"),
    ("POST_INSET", "4.5 mm", "MEASURED (owner, 2026-09-25): post axis inboard of each plate's "
                             "inner face. Read as an AXIS position, as POST_AHEAD"),
    ("POCKET_W", "19 mm", "gap between the cheeks (owner, 2026-09-25); the camera sits in it "
                          "with no side clearance"),
    # ------------------------------------------------------------ assumed: the camera
    ("CAM_H", "19 mm", "ASSUMED: camera body height (standard micro-camera face)"),
    ("CAM_PIVOT_BACK", "5 mm", "ASSUMED: pivot axis behind the camera's front face - the "
                               "number most likely to be wrong"),
    ("CAM_Z", "-14.75 mm", "pivot axis height: about half way down the 31.5 mm mounting area, "
                           "raised 1 mm so the body's top clears the crossbar"),
    # ------------------------------------------------------------ chosen
    ("BAR_OD", "7 mm", "crossbar and post diameter (owner)"),
    ("PILOT_D", "2.5 mm", "pilot for an M3 self-tapping screw into plastic; right through "
                          "the bar, blind up the posts"),
    ("END_CHAMFER", "0.3 mm", "on the bar's ends: eases it between the plates"),
    ("POST_PILOT_DEPTH", "8 mm", "post pilot, up from the bottom face, at most"),
    ("PILOT_ROOF", "2 mm", "least material left between a post pilot and the pocket floor"),
    ("CAM_PIVOT_D", "2.2 mm", "clearance for the M2 screws into the camera's side holes"),
    ("POCKET_V_CLEAR", "1 mm", "above and below the camera body, so it can tilt on its pivots"),
    ("POCKET_DEPTH", "16.5 mm", "cheeks and floor run this far aft of the camera's face "
                                "(owner, 2026-09-29: front face 3.5 mm aft, back face "
                                "where it was; 20 until then)"),
    ("PLATE_CLEAR", "0.4 mm", "each cheek's outer face to the plate's inner face"),
    ("FLOOR_T", "2 mm", "floor under the pocket, joining the cheeks and carrying the posts"),
    ("ARCH_BASE", "-16 mm", "where the top's arcs spring from, front and back (owner's "
                            "sketch, 2026-09-25: about -14 at the back, -18 at the front; "
                            "taken symmetric)"),
    ("ARCH_MARGIN", "0.3 mm", "cap outside the bar, all round its top"),
    # ------------------------------------------------------------ derived
    ("CHEEK_OUT", "=PLATE_GAP / 2 - PLATE_CLEAR", "cheeks' outer faces, +/-x"),
    ("CHEEK_IN", "=POCKET_W / 2", "cheeks' inner faces, +/-x"),
    ("Y_FACE", "=POST_AHEAD + BAR_OD / 2", "front face, flush with the posts' front"),
    ("Y_BACK", "=Y_FACE - POCKET_DEPTH", "back face"),
    ("Z_FLOOR_TOP", "=CAM_Z - CAM_H / 2 - POCKET_V_CLEAR", "pocket floor"),
    ("Z_FLOOR_BOT", "=Z_FLOOR_TOP - FLOOR_T", "underside of the floor"),
    ("Z_CEIL", "=CAM_Z + CAM_H / 2 + POCKET_V_CLEAR", "pocket ceiling, the roof's underside"),
    ("POCKET_H", "=Z_CEIL - Z_FLOOR_TOP", "pocket height"),
    ("POST_H", "=Z_FLOOR_BOT + POST_DROP", "post height, mounting face up to the floor"),
    ("PILOT_DEPTH", "=min(POST_PILOT_DEPTH; POST_H + FLOOR_T - PILOT_ROOF)", "post pilot depth"),
    ("X_POST", "=PLATE_GAP / 2 - POST_INSET", "post axes, +/-x"),
    ("PIVOT_Y", "=Y_FACE - CAM_PIVOT_BACK", "camera pivot axis, y"),
    ("CAP_R", "=BAR_OD / 2 + ARCH_MARGIN", "the cap over the bar, about the bar's axis"),
    ("ARC_R_FRONT", "=(Y_FACE ^ 2 + ARCH_BASE ^ 2 - CAP_R ^ 2) / (2 * (Y_FACE - CAP_R))",
     "front arc: vertical at the front edge at ARCH_BASE, tangent into the cap. For "
     "reference; the sketch finds it by tangency"),
    ("ARC_R_BACK", "=(Y_BACK ^ 2 + ARCH_BASE ^ 2 - CAP_R ^ 2) / (2 * (-Y_BACK - CAP_R))",
     "back arc, the same at the back edge. For reference"),
    ("Z_TOP", "=CAP_R", "the crown"),
    # ------------------------------------------------------------ checks (see CHECKS)
    ("CHEEK_T", "=CHEEK_OUT - CHEEK_IN", "CHECK >= 1.5: cheek thickness"),
    ("BAR_TO_CEIL", "=-BAR_OD / 2 - Z_CEIL", "CHECK >= 0.5: roof between the bar and the pocket"),
    ("CHAMFER_ROOM", "=PLATE_CLEAR - END_CHAMFER", "CHECK >= 0: the bar's chamfer stays "
                                                   "outside the cheeks"),
    ("FRONT_PAST_CAP", "=Y_FACE - CAP_R", "CHECK >= 0.5: the front edge is outside the cap"),
    ("BACK_PAST_CAP", "=-Y_BACK - CAP_R", "CHECK >= 0.5: the back edge is outside the cap"),
]
CHECKS = {"CHEEK_T": 1.5, "POST_H": 1.0, "BAR_TO_CEIL": 0.5, "CHAMFER_ROOM": 0.0,
          "FRONT_PAST_CAP": 0.5, "BACK_PAST_CAP": 0.5}

VIEWS = {
    "front": ((X, -90), (Y, 180)),             # from ahead of the nose looking aft, z up
    "side": ((Z, -90), (X, -90)),              # from +x looking inboard, z up, nose right
    "iso": ((X, -90), (Y, 180), (Y, -30), (X, 25)),
}
PRINT_TURNS = ((X, -90),)                      # +y, the nose, down onto the bed


def add_profile(sk):
    """The cheeks' side profile in the YZ sketch (sketch x = y, sketch y = z): floor,
    front edge, front arc, cap over the bar, back arc, back edge - counter-clockwise.
    Each arc leaves its edge vertically and runs tangent into the cap; the sketch holds
    them by those tangencies, so the radii worked out here only place the first drawing."""
    yb, yf = val(sk, "Params.Y_BACK"), val(sk, "Params.Y_FACE")
    zf, z0, rc = (val(sk, "Params." + a) for a in ("Z_FLOOR_BOT", "ARCH_BASE", "CAP_R"))
    rf, rb = val(sk, "Params.ARC_R_FRONT"), val(sk, "Params.ARC_R_BACK")
    cf, cb = V(yf - rf, z0, 0), V(yb + rb, z0, 0)          # the arcs' centres
    tf = math.atan2(-cf.y, -cf.x)                           # front arc meets the cap here
    tb = math.atan2(-cb.y, -cb.x)                           # and the back arc here
    up = V(0, 0, 1)
    floor = sk.addGeometry(Part.LineSegment(V(yb, zf, 0), V(yf, zf, 0)), False)
    front = sk.addGeometry(Part.LineSegment(V(yf, zf, 0), V(yf, z0, 0)), False)
    arc_f = sk.addGeometry(Part.ArcOfCircle(Part.Circle(cf, up, rf), 0, tf), False)
    cap = sk.addGeometry(Part.ArcOfCircle(Part.Circle(V(0, 0, 0), up, rc), tf, tb), False)
    arc_b = sk.addGeometry(Part.ArcOfCircle(Part.Circle(cb, up, rb), tb, math.pi), False)
    back = sk.addGeometry(Part.LineSegment(V(yb, z0, 0), V(yb, zf, 0)), False)
    sk.addConstraint(Sketcher.Constraint("Coincident", floor, 2, front, 1))
    sk.addConstraint(Sketcher.Constraint("Coincident", back, 2, floor, 1))
    for g1, g2 in ((front, arc_f), (arc_f, cap), (cap, arc_b), (arc_b, back)):
        sk.addConstraint(Sketcher.Constraint("Tangent", g1, 2, g2, 1))
    sk.addConstraint(Sketcher.Constraint("Horizontal", floor))
    sk.addConstraint(Sketcher.Constraint("Vertical", front))
    sk.addConstraint(Sketcher.Constraint("Vertical", back))
    sk.addConstraint(Sketcher.Constraint("Coincident", cap, 3, -1, 1))
    dim(sk, "Radius", (cap,), "cap_r", "Params.CAP_R")
    at_x(sk, (front, 1), "front_face", "Params.Y_FACE")
    at_x(sk, (back, 1), "back_face", "Params.Y_BACK")
    at_y(sk, (front, 2), "front_spring", "Params.ARCH_BASE")
    at_y(sk, (back, 1), "back_spring", "Params.ARCH_BASE")
    at_y(sk, (floor, 1), "floor_underside", "Params.Z_FLOOR_BOT")
    return arc_f, arc_b


def build(doc):
    fcpart.make_params(doc, PARAMS)
    body = doc.addObject("PartDesign::Body", "CamMount")
    body.Label = PART

    # 1. cheeks, floor and roof as one block: the arched side profile, plate to plate
    sk = new_sketch(body, "ProfileSketch", plane="YZ")
    add_profile(sk)
    fcpart.pad(body, "Block", sk, "Params.CHEEK_OUT * 2", both=True)

    # 2. the camera pocket between the cheeks, open front and back
    sk = new_sketch(body, "PocketSketch", plane="XZ")
    ci, zt, ph = val(sk, "Params.CHEEK_IN"), val(sk, "Params.Z_FLOOR_TOP"), val(sk, "Params.POCKET_H")
    g = add_rect(sk, "pocket", -ci, zt, 2 * ci, ph)
    at_x(sk, g["bl"], "pocket_x0", "-Params.CHEEK_IN")
    at_y(sk, g["bl"], "pocket_floor", "Params.Z_FLOOR_TOP")
    dim(sk, "DistanceX", g["bl"] + g["br"], "pocket_w", "Params.POCKET_W")
    dim(sk, "DistanceY", g["br"] + g["tr"], "pocket_h", "Params.POCKET_H")
    fcpart.pocket(body, "CameraPocket", sk, both=True)

    # 3. the crossbar, plate to plate, embedded in the arch's crown
    sk = new_sketch(body, "CrossbarSketch", plane="YZ")
    add_circle(sk, "bar", 0, 0, "Params.BAR_OD")
    fcpart.pad(body, "Crossbar", sk, "Params.PLATE_GAP", both=True)

    # 4. the posts, from the mounting face up to the floor
    sk = new_sketch(body, "PostSketch", "-Params.POST_DROP")
    xp, ya = val(sk, "Params.X_POST"), val(sk, "Params.POST_AHEAD")
    add_circle(sk, "post_l", -xp, ya, "Params.BAR_OD", "-Params.X_POST", "Params.POST_AHEAD")
    add_circle(sk, "post_r", xp, ya, "Params.BAR_OD", "Params.X_POST", "Params.POST_AHEAD")
    fcpart.pad(body, "Posts", sk, "Params.POST_H")

    # 5. post pilots, blind from the mounting face
    sk = new_sketch(body, "PostPilotSketch", "-Params.POST_DROP")
    add_circle(sk, "pilot_l", -xp, ya, "Params.PILOT_D", "-Params.X_POST", "Params.POST_AHEAD")
    add_circle(sk, "pilot_r", xp, ya, "Params.PILOT_D", "Params.X_POST", "Params.POST_AHEAD")
    fcpart.pocket(body, "PostPilots", sk, "Params.PILOT_DEPTH")

    # 6. camera pivots: one M2 clearance hole through each cheek, on the camera's axis
    sk = new_sketch(body, "PivotSketch", plane="YZ")
    add_circle(sk, "pivot", val(sk, "Params.PIVOT_Y"), val(sk, "Params.CAM_Z"),
               "Params.CAM_PIVOT_D", "Params.PIVOT_Y", "Params.CAM_Z")
    fcpart.pocket(body, "CameraPivots", sk, both=True)

    # 7. the crossbar's pilot, right through
    sk = new_sketch(body, "BarPilotSketch", plane="YZ")
    add_circle(sk, "bar_pilot", 0, 0, "Params.PILOT_D")
    pilot = fcpart.pocket(body, "BarPilot", sk, both=True)

    # 8. chamfer the bar's ends. Last, so nothing later renumbers the edges it names
    doc.recompute()
    r, x_end = val(sk, "Params.BAR_OD") / 2, val(sk, "Params.PLATE_GAP") / 2
    ends = fcpart.edges_where(
        pilot, lambda e: (isinstance(e.Curve, Part.Circle) and abs(e.Curve.Radius - r) < 1e-6
                          and abs(abs(e.Curve.Center.x) - x_end) < 1e-6),
        2, "the crossbar's two end rims")
    fcpart.dress(body, "Chamfer", "BarEnds", pilot, ends, "Size", "Params.END_CHAMFER")

    doc.recompute()
    return body


def summary(g):
    return (f"cap R{g('CAP_R'):.2f} about the bar, front arc R{g('ARC_R_FRONT'):.2f}, back arc "
            f"R{g('ARC_R_BACK'):.2f}, springing at z {g('ARCH_BASE'):.1f}; pocket {g('POCKET_W'):.1f} wide x {g('POCKET_H'):.1f} high, cheeks "
            f"{g('CHEEK_T'):.2f} thick; front face y {g('Y_FACE'):.1f}, back {g('Y_BACK'):.1f}; "
            f"floor z {g('Z_FLOOR_BOT'):.2f}..{g('Z_FLOOR_TOP'):.2f}, ceiling {g('Z_CEIL'):.2f}, "
            f"crown {g('Z_TOP'):.2f}; camera pivots at y {g('PIVOT_Y'):.1f}, z {g('CAM_Z'):.2f}; "
            f"posts {g('POST_H'):.2f} high at x +/-{g('X_POST'):.2f}, pilots "
            f"{g('PILOT_DEPTH'):.2f} deep")


if __name__ == "__main__":
    fcpart.run(__file__, DOC, PART, build, CHECKS, VIEWS, PRINT_TURNS, summary)
