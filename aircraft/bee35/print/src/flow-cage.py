"""Bee35 flow-sensor cage: a TPU strap over the MTF-01P, taped to the VTX heatsink (OQ-05).

FreeCAD script (fleet F-DEC-09, F-DEC-10). It builds `flow-cage.FCStd` beside itself - a
`Params` spreadsheet and a PartDesign body whose sketches and features are bound to it by
expression - and exports the STL, STEP and SVG views to `../stl/`. This script is the
source; the FCStd is what it emits, checked in so the part opens directly. Change a value
in the spreadsheet to try it; put the agreed value back HERE and rebuild.

Owner's scheme, 2026-09-26: the sensor is stuck to the heatsink's face with strong gel
tape, dead centre, long axis across the aircraft, face down. This TPU part goes over it
and is screwed to the sink's FORE and AFT M2 holes only - the two on the centreline -
because the sensor's 33 mm length covers the other two. The tape locates the sensor and
carries flight loads; the cage carries landing and peel loads, which tape is bad at,
and stops a failed bond costing the sensor.

Shape: a ring around the sensor's 9.25 mm rectangular body, a narrow lip turned in over
the edges of its face - the two lens cylinders stand through the window, whose top edge
is rounded - a notch in the foot of the ring on the connector side for the cable, a
notch in the foot of each short end over the screws that fasten the VTX to the sink, and
a tab fore and aft lying on the sink with an M2 clearance hole. The tabs are square
where they join the ring and rounded at their outer corners; the connector-side tab runs
on past the notch, so it joins the ring on both sides of it. The M2 heads sit on the
tabs against the ring's plain face.

Frame: sensor centre on the sink at the origin; x across the aircraft (the sensor's
long axis), y fore-aft, z = 0 the sink's face, +z away from the sink - down in flight.
The sink's M2s are on a 20 x 20 square set as a diamond, so the fore and aft ones are
at (0, +/-14.14).

Print: sink side down, tabs on the bed, ring rising, lip last. TPU 95A, the fleet's
calibrated `tpu` profile. The lip's underside is FLAT: a LIP-wide overhang at z = Z_FACE
(see ../sources.md `flow-cage`, "Known defect").

Build: run this file as __main__ inside FreeCAD, with __file__ set (rules and the reasons
for this form: /AGENTS.md "CAD in FreeCAD").
    RUN="p='$PWD/flow-cage.py'; exec(compile(open(p).read(), p, 'exec'), {'__file__': p, '__name__': '__main__'})"
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
from fcpart import (X, Y, Z, add_rect, add_rounded_rect, at_x, at_y,  # noqa: E402
                    centre_on_origin, dim, new_sketch, pad, pocket, val)

DOC = "flow_cage"
PART = "bee35-flow-cage"

# Which long edge the lens cylinders crowd (+1 = +y); the connector is on the other.
# Script-level, not in the spreadsheet: they pick which way constraints are drawn.
CYL_SIDE = +1
CONN_SIDE = -CYL_SIDE

# (alias, value or formula, note). Every value carries its unit; formulas start with "=".
PARAMS = [
    # ------------------------------------------------------------ measured / stated
    ("SINK_PITCH", "20 mm", "MEASURED (owner): 4 x M2 tapped on a 20 x 20 square, set as a "
                            "diamond (45 deg) to the airframe (owner, underside photo)"),
    ("M2_HOLE", "2.2 mm", "M2 clearance"),
    # MTF-01P, MicoAir's product page (read 2026-09-25) and product photos (2026-09-27):
    ("SENSOR_L", "33.2 mm", "MicoAir: sensor length, across the aircraft"),
    ("SENSOR_W", "20.8 mm", "MicoAir: sensor width, fore-aft"),
    ("BODY_T", "9.25 mm", "MEASURED (owner, 2026-09-27): the rectangular body, sink side to "
                          "face; the two lens cylinders rise above it to the 16.8 overall"),
    # From MicoAir's TOP photo, scaled by the 33.2 x 20.8 body (+/-0.5 mm): lens and ToF
    # cylinders ~dia 8, centres at x -5.8 and +4.2, both offset +3.4 toward one long edge;
    # a third dia ~4 window at (-0.8, -4.4). The corner screws are countersunk in the face.
    ("CYL_GAP", "1.75 mm", "MEASURED (owner, 2026-09-29): lens cylinders' edge to the "
                           "body's nearest long edge; decides the lip. Photo gave 2.7"),
    # From the SIDE and BOTTOM photos: the 4-pin JST is on a long SIDE face, near the middle.
    ("CONN_X", "3 mm", "connector centre along the long axis: scaled off a photo, and the "
                       "notch it places 'works perfectly' (owner, 2026-09-29, first print)"),
    ("CONN_W", "7 mm", "notch width in the ring for connector and cable; as CONN_X"),
    # ------------------------------------------------------------ chosen
    ("TAPE_T", "1 mm", "ASSUMED: gel tape between sink and sensor - measure the tape"),
    ("FACE_TRIM", "2.5 mm", "taken off the face's height (owner, 2026-09-29, off the first "
                            "print: the cage stood 2.5 mm too tall). Which of BODY_T and "
                            "TAPE_T it corrects is not known"),
    ("FIT", "0.05 mm", "cage to sensor, each side (owner, 2026-09-29, off the first print, "
                       "a loose-ish fit at 0.3: walls in 0.5 mm in all)"),
    ("WALL", "1.5 mm", "ring wall"),
    ("LIP", "1.25 mm", "how far the lip turns in from the wall. The WINDOW is where the "
                       "owner agreed it on 2026-09-29 (1.5 from walls 0.25 further out), "
                       "which clears the measured CYL_GAP; 2 before that did not"),
    ("LIP_T", "1.5 mm", "lip thickness, above the face"),
    ("LIP_EDGE_R", "1 mm", "round on the window's top edge, all round (owner, 2026-09-29, "
                           "tried at 1 mm in FreeCAD). Below LIP_T and below LIP"),
    ("TAB_W", "8 mm", "tab width on the cylinder side"),
    ("TAB_W_CONN", "14 mm", "least tab width on the connector side, centred on the hole; "
                            "the cable exits over this tab"),
    ("TAB_PAST_NOTCH", "4 mm", "connector-side tab runs this far past the notch's edge, to "
                               "join the ring beyond it (owner, 2026-09-29)"),
    ("TAB_T", "1.5 mm", "tab thickness, on the sink"),
    ("TAB_END", "2 mm", "tab material beyond the M2 hole's centre (owner, 2026-09-29, off "
                        "the first print: 1 mm less, to clear the VTX's screws fore and "
                        "aft; 3 until then)"),
    ("TAB_R", "2 mm", "tab corner radius, OUTER corners only; square at the ring "
                      "(owner, 2026-09-29)"),
    ("CORNER_R", "2 mm", "ring's outer vertical corners"),
    ("NOTCH_OVER", "1 mm", "notch overcut past the wall, inward and outward"),
    ("NOTCH_H", "5 mm", "notch height up from the sink; the ring is whole above it "
                        "(owner, 2026-09-29, set in FreeCAD; was full height)"),
    ("END_NOTCH_W", "6 mm", "notch in the foot of each short end, over a VTX screw, centred "
                            "on the end (owner, 2026-09-29, off the first print; the 6 "
                            "and the 2.5 below are the assistant's figures, and the "
                            "second print clears the screws with them)"),
    ("END_NOTCH_H", "2.5 mm", "its height up from the sink"),
    ("M2_HEAD_D", "3.8 mm", "M2 button/socket head; no recess for it in the ring "
                            "(owner, 2026-09-29)"),
    # ------------------------------------------------------------ derived
    ("M2_Y", "=SINK_PITCH / 2 * sqrt(2)", "fore and aft holes on x = 0 (the diamond's points)"),
    ("IX", "=SENSOR_L / 2 + FIT", "inside of the ring, half-length"),
    ("IY", "=SENSOR_W / 2 + FIT", "inside of the ring, half-width"),
    ("OX", "=IX + WALL", "outside of the ring, half-length"),
    ("OY", "=IY + WALL", "outside of the ring, half-width"),
    ("Z_FACE", "=TAPE_T + BODY_T - FACE_TRIM", "the lip's underside, on the body's face"),
    ("Z_TOP", "=Z_FACE + LIP_T", "top of the lip"),
    ("CYL_Y_MAX", "=SENSOR_W / 2 - CYL_GAP", "cylinders' far edge from the body's centreline"),
    ("TAB_LEN", "=M2_Y + TAB_END - OY", "tab length, out from the ring's face"),
    ("NOTCH_X0", "=CONN_X - CONN_W / 2", "notch, low-x edge"),
    ("NOTCH_X1", "=CONN_X + CONN_W / 2", "notch, high-x edge"),
    ("TAB_CONN_X0", "=min(-TAB_W_CONN / 2; NOTCH_X0 - TAB_PAST_NOTCH)",
     "connector-side tab, low-x end"),
    ("TAB_CONN_X1", "=max(TAB_W_CONN / 2; NOTCH_X1 + TAB_PAST_NOTCH)",
     "connector-side tab, high-x end"),
    # ------------------------------------------------------------ checks (see CHECKS)
    ("RING_TO_HOLE", "=M2_Y - M2_HOLE / 2 - OY", "CHECK >= 0.8: ring face to the M2 hole"),
    ("LIP_TO_CYL", "=IY - LIP - CYL_Y_MAX", "CHECK >= 0.5: lip window edge to the cylinders"),
    ("HEAD_TO_RING", "=M2_Y - M2_HEAD_D / 2 - OY", "CHECK >= 0: M2 head edge to the ring's face"),
    ("LIP_EDGE_LAND", "=min(LIP_T; LIP) - LIP_EDGE_R",
     "CHECK >= 0.2: what the round leaves of the lip's thickness and width"),
    ("TAB_PAST_HOLE", "=TAB_END - M2_HOLE / 2", "CHECK >= 0.8: tab left beyond the M2 hole"),
    ("RING_OVER_NOTCH", "=Z_FACE - max(NOTCH_H; END_NOTCH_H)",
     "CHECK >= 2: ring wall left between the tallest notch and the lip"),
    ("TAB_JOIN_MIN", "=min(NOTCH_X0 - TAB_CONN_X0; TAB_CONN_X1 - NOTCH_X1)",
     "CHECK >= 3: connector-side tab's shorter join to the ring, beside the notch"),
]
CHECKS = {"RING_TO_HOLE": 0.8, "LIP_TO_CYL": 0.5, "HEAD_TO_RING": 0.0, "TAB_JOIN_MIN": 3.0,
          "LIP_EDGE_LAND": 0.2, "TAB_PAST_HOLE": 0.8, "RING_OVER_NOTCH": 2.0}


# -------------------------------------------------------------------- sketch helper
def add_tab(sk, tag, x0, x1, root, length, r, side, x0_expr, w_expr):
    """A tab out from the ring's face on the given side (+1 = +y): square at the root,
    where it joins the ring, its two outer corners rounded. Drawn counter-clockwise.
    x0, x1, root, length, r are numbers for the first placement; all are bound here."""
    i = sk.GeometryCount
    yr, yo = side * root, side * (root + length)            # root and outer edge
    yc = yo - side * r                                       # the arcs' centres
    if side > 0:
        a, b = (x0, x1), (x1, x0)                            # root runs +x, outer edge -x
        arcs = [(V(x1 - r, yc), 0), (V(x0 + r, yc), 90)]
    else:
        a, b = (x1, x0), (x0, x1)                            # root runs -x, outer edge +x
        arcs = [(V(x0 + r, yc), 180), (V(x1 - r, yc), 270)]
    e = r if a[0] < a[1] else -r                             # the root's direction, r long
    lines = [(V(a[0], yr), V(a[1], yr)),                     # 0 root
             (V(a[1], yr), V(a[1], yc)),                     # 1 side, root to first arc
             (V(b[0] - e, yo), V(b[1] + e, yo)),             # 2 outer edge, between the arcs
             (V(b[1], yc), V(b[1], yr))]                     # 3 side, second arc to root
    root_l, side1, arc1, outer, arc2, side2 = range(i, i + 6)
    sk.addGeometry(Part.LineSegment(*lines[0]), False)
    sk.addGeometry(Part.LineSegment(*lines[1]), False)
    sk.addGeometry(Part.ArcOfCircle(Part.Circle(arcs[0][0], V(0, 0, 1), r),
                                    math.radians(arcs[0][1]), math.radians(arcs[0][1] + 90)), False)
    sk.addGeometry(Part.LineSegment(*lines[2]), False)
    sk.addGeometry(Part.ArcOfCircle(Part.Circle(arcs[1][0], V(0, 0, 1), r),
                                    math.radians(arcs[1][1]), math.radians(arcs[1][1] + 90)), False)
    sk.addGeometry(Part.LineSegment(*lines[3]), False)
    sk.addConstraint(Sketcher.Constraint("Coincident", root_l, 2, side1, 1))
    sk.addConstraint(Sketcher.Constraint("Coincident", side2, 2, root_l, 1))
    sk.addConstraint(Sketcher.Constraint("Tangent", side1, 2, arc1, 1))
    sk.addConstraint(Sketcher.Constraint("Tangent", arc1, 2, outer, 1))
    sk.addConstraint(Sketcher.Constraint("Tangent", outer, 2, arc2, 1))
    sk.addConstraint(Sketcher.Constraint("Tangent", arc2, 2, side2, 1))
    for g, kind in ((root_l, "Horizontal"), (outer, "Horizontal"),
                    (side1, "Vertical"), (side2, "Vertical")):
        sk.addConstraint(Sketcher.Constraint(kind, g))
    sk.addConstraint(Sketcher.Constraint("Equal", arc1, arc2))
    dim(sk, "Radius", (arc1,), tag + "_r", "Params.TAB_R")
    low, high = ((root_l, 1), (root_l, 2)) if side > 0 else ((root_l, 2), (root_l, 1))
    at_x(sk, low, tag + "_x0", x0_expr)
    dim(sk, "DistanceX", low + high, tag + "_w", w_expr)
    at_y(sk, (root_l, 1), tag + "_root", "Params.OY", side)
    span = (root_l, 1) + (outer, 1) if side > 0 else (outer, 1) + (root_l, 1)
    dim(sk, "DistanceY", span, tag + "_len", "Params.TAB_LEN")


# -------------------------------------------------------------------- the part
def build(doc):
    fcpart.make_params(doc, PARAMS)
    body = doc.addObject("PartDesign::Body", "FlowCage")
    body.Label = PART

    # 1. ring: a solid block, vertical corners rounded
    sk = new_sketch(body, "RingSketch")
    ox, oy, r = val(sk, "Params.OX"), val(sk, "Params.OY"), val(sk, "Params.CORNER_R")
    g = add_rounded_rect(sk, "ring", -ox, -oy, 2 * ox, 2 * oy, r,
                         "Params.OX * 2", "Params.OY * 2", "Params.CORNER_R")
    centre_on_origin(sk, g["left"], g["right"])
    pad(body, "Ring", sk, "Params.Z_TOP")

    # 2. cavity for the sensor body, from the sink up to the body's face
    sk = new_sketch(body, "CavitySketch")
    ix, iy = val(sk, "Params.IX"), val(sk, "Params.IY")
    g = add_rect(sk, "cavity", -ix, -iy, 2 * ix, 2 * iy)
    centre_on_origin(sk, g["bl"], g["tr"])
    dim(sk, "DistanceX", g["bl"] + g["br"], "cavity_w", "Params.IX * 2")
    dim(sk, "DistanceY", g["br"] + g["tr"], "cavity_h", "Params.IY * 2")
    pocket(body, "Cavity", sk, "Params.Z_FACE")

    # 3. window in the lip; the lens cylinders stand through it
    sk = new_sketch(body, "WindowSketch")
    lip = val(sk, "Params.LIP")
    g = add_rect(sk, "window", -(ix - lip), -(iy - lip), 2 * (ix - lip), 2 * (iy - lip))
    centre_on_origin(sk, g["bl"], g["tr"])
    dim(sk, "DistanceX", g["bl"] + g["br"], "window_w", "(Params.IX - Params.LIP) * 2")
    dim(sk, "DistanceY", g["br"] + g["tr"], "window_h", "(Params.IY - Params.LIP) * 2")
    pocket(body, "Window", sk)

    # 4. notch in the foot of the ring for the connector and cable, connector side
    sk = new_sketch(body, "NotchSketch")
    cx, cw, over = val(sk, "Params.CONN_X"), val(sk, "Params.CONN_W"), val(sk, "Params.NOTCH_OVER")
    depth = oy - iy + 2 * over
    y_near = CONN_SIDE * (iy - over)                      # the edge inside the cavity
    g = add_rect(sk, "notch", cx - cw / 2, min(y_near, y_near + CONN_SIDE * depth), cw, depth)
    dim(sk, "DistanceX", g["bl"] + g["br"], "notch_w", "Params.CONN_W")
    dim(sk, "DistanceY", g["br"] + g["tr"], "notch_depth", "Params.WALL + Params.NOTCH_OVER * 2")
    at_x(sk, g["bl"], "notch_x0", "Params.NOTCH_X0")
    at_y(sk, g["tl"] if CONN_SIDE < 0 else g["bl"], "notch_inner",
         "Params.IY - Params.NOTCH_OVER", CONN_SIDE)
    pocket(body, "Notch", sk, "Params.NOTCH_H")

    # 4b. a notch in the foot of each short end, over the VTX's screws, through the wall
    sk = new_sketch(body, "EndNotchSketch")
    ew = val(sk, "Params.END_NOTCH_W")
    for side, tag in ((+1, "right"), (-1, "left")):
        x0 = ix - over if side > 0 else -(ox + over)
        g = add_rect(sk, tag, x0, -ew / 2, ox - ix + 2 * over, ew)
        at_x(sk, g["bl"], f"end_notch_{tag}_x0",
             "Params.IX - Params.NOTCH_OVER" if side > 0 else "-Params.OX - Params.NOTCH_OVER")
        at_y(sk, g["tl"], f"end_notch_{tag}_y1", "Params.END_NOTCH_W / 2")
        dim(sk, "DistanceX", g["bl"] + g["br"], f"end_notch_{tag}_depth",
            "Params.WALL + Params.NOTCH_OVER * 2")
        dim(sk, "DistanceY", g["br"] + g["tr"], f"end_notch_{tag}_w", "Params.END_NOTCH_W")
    pocket(body, "EndNotches", sk, "Params.END_NOTCH_H")

    # 5. tabs fore and aft, on the sink, square at the ring; added after the notch, and
    #    the connector-side one runs past it, so it closes the notch's foot and joins
    #    the ring on both sides
    sk = new_sketch(body, "TabSketch")
    tl, tr_ = val(sk, "Params.TAB_LEN"), val(sk, "Params.TAB_R")
    for side in (+1, -1):
        if side == CONN_SIDE:
            add_tab(sk, "tab_conn", val(sk, "Params.TAB_CONN_X0"), val(sk, "Params.TAB_CONN_X1"),
                    oy, tl, tr_, side, "Params.TAB_CONN_X0",
                    "Params.TAB_CONN_X1 - Params.TAB_CONN_X0")
        else:
            w = val(sk, "Params.TAB_W")
            add_tab(sk, "tab_cyl", -w / 2, w / 2, oy, tl, tr_, side,
                    "-Params.TAB_W / 2", "Params.TAB_W")
    pad(body, "Tabs", sk, "Params.TAB_T")

    # 6. M2 clearance holes on the sink's fore and aft holes
    sk = new_sketch(body, "HoleSketch")
    m2y = val(sk, "Params.M2_Y")
    for side, tag in ((+1, "fore"), (-1, "aft")):
        c = sk.addGeometry(Part.Circle(V(0, side * m2y, 0), V(0, 0, 1),
                                       val(sk, "Params.M2_HOLE") / 2), False)
        sk.addConstraint(Sketcher.Constraint("PointOnObject", c, 3, -2))
        dim(sk, "Diameter", (c,), f"hole_{tag}_d", "Params.M2_HOLE")
        at_y(sk, (c, 3), f"hole_{tag}_y", "Params.M2_Y", side)
    holes = pocket(body, "Holes", sk)

    # 7. round the window's top edge, all round. Last, so nothing later renumbers the
    #    edges it names; they are found by where they are, not by number
    doc.recompute()
    z_top, wx, wy = val(sk, "Params.Z_TOP"), ix - lip, iy - lip
    near = lambda a, b: abs(a - b) < 1e-6

    def window_top(e):
        m = e.CenterOfMass
        return (all(near(v.Z, z_top) for v in e.Vertexes)
                and ((near(abs(m.x), wx) and abs(m.y) < wy)
                     or (near(abs(m.y), wy) and abs(m.x) < wx)))

    edges = fcpart.edges_where(holes, window_top, 4, "the window's top edge")
    fcpart.dress(body, "Fillet", "LipEdge", holes, edges, "Radius", "Params.LIP_EDGE_R")

    doc.recompute()
    return body


VIEWS = {
    "plan": (),                                # from +z: the face side
    "front": ((X, -90), (Y, 180)),
    "side": ((Z, -90), (X, -90)),
    "iso": ((Y, -30), (X, -55)),
}
PRINT_TURNS = ()                               # modelled bed-down already


def summary(g):
    return (f"ring outside {2*g('OX'):.1f} x {2*g('OY'):.1f}, "
            f"window {2*(g('IX')-g('LIP')):.1f} x {2*(g('IY')-g('LIP')):.1f}, face at z "
            f"{g('Z_FACE'):.2f}, top {g('Z_TOP'):.2f}; M2 at y +/-{g('M2_Y'):.2f}, "
            f"{g('RING_TO_HOLE'):.2f} mm clear of the ring; M2 head "
            f"{g('HEAD_TO_RING'):.2f} mm clear of the ring's face; lip window edge "
            f"{g('LIP_TO_CYL'):.2f} mm from the cylinders; notch {g('NOTCH_H'):.1f} high, end "
            f"notches {g('END_NOTCH_W'):.1f} wide x {g('END_NOTCH_H'):.1f} high; tabs "
            f"{g('TAB_LEN'):.2f} out from the ring, {g('TAB_PAST_HOLE'):.2f} beyond the hole; "
            f"connector-side tab x {g('TAB_CONN_X0'):.1f}..{g('TAB_CONN_X1'):.1f}, joined "
            f"{g('TAB_JOIN_MIN'):.1f} mm or more each side of the notch")


if __name__ == "__main__":
    fcpart.run(__file__, DOC, PART, build, CHECKS, VIEWS, PRINT_TURNS, summary)
