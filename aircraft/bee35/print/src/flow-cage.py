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
the edges of its face - the two lens cylinders stand through the window - a notch in the
ring on the connector side for the cable, and a tab fore and aft lying on the sink with
an M2 clearance hole.

Frame: sensor centre on the sink at the origin; x across the aircraft (the sensor's
long axis), y fore-aft, z = 0 the sink's face, +z away from the sink - down in flight.
The sink's M2s are on a 20 x 20 square set as a diamond, so the fore and aft ones are
at (0, +/-14.14).

Print: sink side down, tabs on the bed, ring rising, lip last. TPU 95A, the fleet's
calibrated `tpu` profile. The lip's underside is FLAT: a LIP-wide overhang at z = Z_FACE
(see ../sources.md `flow-cage`, "Known defects").

Build: run this file as __main__ inside FreeCAD, with __file__ set (rules and the reasons
for this form: /AGENTS.md "CAD in FreeCAD").
    RUN="p='$PWD/flow-cage.py'; exec(compile(open(p).read(), p, 'exec'), {'__file__': p, '__name__': '__main__'})"
  in the GUI, so the part is seen being made: paste the quoted Python into the Python
    console, or send it through the FreeCAD MCP;
  headless:  flatpak run --command=FreeCADCmd org.freecad.FreeCAD -c "$RUN"
Needs: FreeCAD 1.1 (built and checked on 1.1.3).
"""

import math
import os
import sys

import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector as V

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
    ("CYL_Y_MAX", "7.7 mm", "PHOTO +/-0.5: cylinders' far edge from the body's centreline; "
                            "decides the lip"),
    # From the SIDE and BOTTOM photos: the 4-pin JST is on a long SIDE face, near the middle.
    ("CONN_X", "3 mm", "PHOTO +/-0.5: connector centre along the long axis"),
    ("CONN_W", "7 mm", "notch width in the ring for connector and cable"),
    # ------------------------------------------------------------ chosen
    ("TAPE_T", "1 mm", "ASSUMED: gel tape between sink and sensor - measure the tape"),
    ("FIT", "0.3 mm", "cage to sensor, each side; TPU stretches, keep it snug"),
    ("WALL", "1.5 mm", "ring wall"),
    ("LIP", "2 mm", "how far the lip turns in over the face's edges"),
    ("LIP_T", "1.5 mm", "lip thickness, above the face"),
    ("TAB_W", "8 mm", "tab width on the cylinder side"),
    ("TAB_W_CONN", "14 mm", "tab width on the connector side: wider, so it bridges the ring "
                            "either side of the notch; the cable exits over it"),
    ("TAB_T", "1.5 mm", "tab thickness, on the sink"),
    ("TAB_END", "3 mm", "tab material beyond the M2 hole's centre"),
    ("TAB_R", "2 mm", "tab corner radius, all four corners (see Known defects)"),
    ("CORNER_R", "2 mm", "ring's outer vertical corners"),
    ("NOTCH_OVER", "1 mm", "notch overcut past the wall, inward and outward"),
    ("M2_HEAD_D", "3.8 mm", "M2 button/socket head"),
    ("M2_HEAD_H", "2 mm", "M2 head height"),
    ("HEAD_ROOM", "0.6 mm", "recess into the ring's outer face at each tab, so the head seats"),
    ("HEAD_FIT", "0.3 mm", "recess half-width beyond the head's radius"),
    ("HEAD_OVER", "0.5 mm", "recess height above the head"),
    # ------------------------------------------------------------ derived
    ("M2_Y", "=SINK_PITCH / 2 * sqrt(2)", "fore and aft holes on x = 0 (the diamond's points)"),
    ("IX", "=SENSOR_L / 2 + FIT", "inside of the ring, half-length"),
    ("IY", "=SENSOR_W / 2 + FIT", "inside of the ring, half-width"),
    ("OX", "=IX + WALL", "outside of the ring, half-length"),
    ("OY", "=IY + WALL", "outside of the ring, half-width"),
    ("Z_FACE", "=TAPE_T + BODY_T", "the body's face; the cylinders rise past it"),
    ("Z_TOP", "=Z_FACE + LIP_T", "top of the lip"),
    ("TAB_LEN", "=M2_Y + TAB_END - OY", "tab length, out from the ring's face"),
    ("HEAD_HW", "=M2_HEAD_D / 2 + HEAD_FIT", "head recess half-width"),
    # ------------------------------------------------------------ checks (see CHECKS)
    ("RING_TO_HOLE", "=M2_Y - M2_HOLE / 2 - OY", "CHECK >= 0.8: ring face to the M2 hole"),
    ("LIP_TO_CYL", "=IY - LIP - CYL_Y_MAX", "CHECK >= 0.5: lip window edge to the cylinders"),
    ("HEAD_TO_FACE", "=M2_Y - M2_HEAD_D / 2 - (OY - HEAD_ROOM)",
     "CHECK >= 0: M2 head edge to the recessed face"),
]
CHECKS = {"RING_TO_HOLE": 0.8, "LIP_TO_CYL": 0.5, "HEAD_TO_FACE": 0.0}


# -------------------------------------------------------------------- spreadsheet
def make_params(doc):
    sh = doc.addObject("Spreadsheet::Sheet", "Params")
    for col, head in zip("ABC", ("name", "value", "source / note")):
        sh.set(f"{col}1", head)
    sh.setStyle("A1:C1", "bold")
    for row, (alias, value, note) in enumerate(PARAMS, start=2):
        sh.set(f"A{row}", alias)
        sh.set(f"B{row}", value if value.startswith("=") else "=" + value)
        sh.setAlias(f"B{row}", alias)
        sh.set(f"C{row}", note)
    sh.setColumnWidth("A", 120)
    sh.setColumnWidth("B", 90)
    sh.setColumnWidth("C", 700)
    doc.recompute()
    return sh


# -------------------------------------------------------------------- sketch helpers
def new_sketch(body, name, z_expr=None):
    """A sketch on the body's XY plane, optionally lifted to z = z_expr."""
    xy = [o for o in body.Origin.OriginFeatures if o.Role == "XY_Plane"][0]
    sk = body.newObject("Sketcher::SketchObject", name)
    sk.AttachmentSupport = (xy, [""])
    sk.MapMode = "FlatFace"
    if z_expr:
        sk.setExpression("AttachmentOffset.Base.z", z_expr)
    return sk


def val(sk, expr):
    q = sk.evalExpression(expr)
    return float(getattr(q, "Value", q))


def dim(sk, kind, refs, name, expr):
    """A named dimensional constraint bound to a spreadsheet expression."""
    i = sk.addConstraint(Sketcher.Constraint(kind, *refs, val(sk, expr)))
    sk.renameConstraint(i, name)
    sk.setExpression("Constraints." + name, expr)


def at_y(sk, point, name, expr, side):
    """Put a point at y = side * expr (expr > 0), drawn so the value stays positive."""
    refs = (-1, 1) + point if side > 0 else point + (-1, 1)
    dim(sk, "DistanceY", refs, name, expr)


def add_rect(sk, tag, x0, y0, w, h):
    """Sharp rectangle, lines bottom-right-top-left. Returns corner points bl, br, tr, tl.
    x0, y0, w, h are numbers for the first placement only; width and height are bound
    to expressions here by the caller, position by the caller too."""
    i = sk.GeometryCount
    p = [V(x0, y0, 0), V(x0 + w, y0, 0), V(x0 + w, y0 + h, 0), V(x0, y0 + h, 0)]
    for k in range(4):
        sk.addGeometry(Part.LineSegment(p[k], p[(k + 1) % 4]), False)
    for k in range(4):
        sk.addConstraint(Sketcher.Constraint("Coincident", i + k, 2, i + (k + 1) % 4, 1))
    for k, kind in ((0, "Horizontal"), (2, "Horizontal"), (1, "Vertical"), (3, "Vertical")):
        sk.addConstraint(Sketcher.Constraint(kind, i + k))
    return {"bl": (i, 1), "br": (i + 1, 1), "tr": (i + 2, 1), "tl": (i + 3, 1)}


def add_rounded_rect(sk, tag, x0, y0, w, h, r, w_expr, h_expr, r_expr):
    """Rectangle with four equal corner arcs, drawn counter-clockwise from the bottom
    edge. Width, height and radius are bound; the caller places it. Returns a point on
    each side: left (x0, y1 - r), right (x1, y0 + r), bottom (x0 + r, y0), top (x1 - r, y1)."""
    i = sk.GeometryCount
    x1, y1 = x0 + w, y0 + h
    lines = [(V(x0 + r, y0), V(x1 - r, y0)), (V(x1, y0 + r), V(x1, y1 - r)),
             (V(x1 - r, y1), V(x0 + r, y1)), (V(x0, y1 - r), V(x0, y0 + r))]
    arcs = [(V(x1 - r, y0 + r), -90), (V(x1 - r, y1 - r), 0),
            (V(x0 + r, y1 - r), 90), (V(x0 + r, y0 + r), 180)]
    for (a, b), (c, start) in zip(lines, arcs):
        sk.addGeometry(Part.LineSegment(a, b), False)
        sk.addGeometry(Part.ArcOfCircle(Part.Circle(c, V(0, 0, 1), r),
                                        math.radians(start), math.radians(start + 90)), False)
    ln = [i, i + 2, i + 4, i + 6]          # bottom, right, top, left
    ar = [i + 1, i + 3, i + 5, i + 7]      # bottom-right, top-right, top-left, bottom-left
    for k in range(4):
        sk.addConstraint(Sketcher.Constraint("Tangent", ln[k], 2, ar[k], 1))
        sk.addConstraint(Sketcher.Constraint("Tangent", ar[k], 2, ln[(k + 1) % 4], 1))
    for k, kind in ((0, "Horizontal"), (2, "Horizontal"), (1, "Vertical"), (3, "Vertical")):
        sk.addConstraint(Sketcher.Constraint(kind, ln[k]))
    for k in range(3):
        sk.addConstraint(Sketcher.Constraint("Equal", ar[k], ar[k + 1]))
    dim(sk, "Radius", (ar[0],), tag + "_r", r_expr)
    dim(sk, "DistanceX", (ln[3], 1, ln[1], 1), tag + "_w", w_expr)
    dim(sk, "DistanceY", (ln[0], 1, ln[2], 1), tag + "_h", h_expr)
    return {"left": (ln[3], 1), "right": (ln[1], 1), "bottom": (ln[0], 1), "top": (ln[2], 1)}


def centre_on_origin(sk, a, b):
    sk.addConstraint(Sketcher.Constraint("Symmetric", *a, *b, -1, 1))


def pad(body, name, sketch, length_expr):
    f = body.newObject("PartDesign::Pad", name)
    f.Profile = sketch
    f.setExpression("Length", length_expr)
    sketch.Visibility = False
    return f


def pocket(body, name, sketch, length_expr=None):
    """Cut upward (+z) from the sketch: a set length, or through all when none is given."""
    f = body.newObject("PartDesign::Pocket", name)
    f.Profile = sketch
    f.Reversed = True
    if length_expr:
        f.Type = 0
        f.setExpression("Length", length_expr)
    else:
        f.Type = 1
    sketch.Visibility = False
    return f


# -------------------------------------------------------------------- the part
def build(doc):
    make_params(doc)
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

    # 4. notch in the ring for the connector and cable, full height, connector side
    sk = new_sketch(body, "NotchSketch")
    cx, cw, over = val(sk, "Params.CONN_X"), val(sk, "Params.CONN_W"), val(sk, "Params.NOTCH_OVER")
    depth = oy - iy + 2 * over
    y_near = CONN_SIDE * (iy - over)                      # the edge inside the cavity
    g = add_rect(sk, "notch", cx - cw / 2, min(y_near, y_near + CONN_SIDE * depth), cw, depth)
    dim(sk, "DistanceX", g["bl"] + g["br"], "notch_w", "Params.CONN_W")
    dim(sk, "DistanceY", g["br"] + g["tr"], "notch_depth", "Params.WALL + Params.NOTCH_OVER * 2")
    dim(sk, "DistanceX", (-1, 1) + g["bl"], "notch_x0", "Params.CONN_X - Params.CONN_W / 2")
    at_y(sk, g["tl"] if CONN_SIDE < 0 else g["bl"], "notch_inner",
         "Params.IY - Params.NOTCH_OVER", CONN_SIDE)
    pocket(body, "Notch", sk)

    # 5. tabs fore and aft, on the sink; added after the notch so the connector-side
    #    tab bridges it
    sk = new_sketch(body, "TabSketch")
    tl, tr_ = val(sk, "Params.TAB_LEN"), val(sk, "Params.TAB_R")
    for side in (+1, -1):
        conn = side == CONN_SIDE
        w_expr = "Params.TAB_W_CONN" if conn else "Params.TAB_W"
        tag = "tab_conn" if conn else "tab_cyl"
        w = val(sk, w_expr)
        g = add_rounded_rect(sk, tag, -w / 2, oy if side > 0 else -(oy + tl), w, tl, tr_,
                             w_expr, "Params.TAB_LEN", "Params.TAB_R")
        dim(sk, "DistanceX", (-1, 1) + g["left"], tag + "_x0", f"-{w_expr} / 2")
        at_y(sk, g["bottom"] if side > 0 else g["top"], tag + "_root", "Params.OY", side)
    pad(body, "Tabs", sk, "Params.TAB_T")

    # 6. M2 clearance holes on the sink's fore and aft holes
    sk = new_sketch(body, "HoleSketch")
    m2y, d = val(sk, "Params.M2_Y"), val(sk, "Params.M2_HOLE")
    for side, tag in ((+1, "fore"), (-1, "aft")):
        c = sk.addGeometry(Part.Circle(V(0, side * m2y, 0), V(0, 0, 1), d / 2), False)
        sk.addConstraint(Sketcher.Constraint("PointOnObject", c, 3, -2))
        dim(sk, "Diameter", (c,), f"hole_{tag}_d", "Params.M2_HOLE")
        at_y(sk, (c, 3), f"hole_{tag}_y", "Params.M2_Y", side)
    pocket(body, "Holes", sk)

    # 7. head recess: the ring's outer face, at each tab, thinned by HEAD_ROOM up to the
    #    head's height, so the screw head sits flat on the tab
    sk = new_sketch(body, "RecessSketch", "Params.TAB_T")
    hw, room, hover = val(sk, "Params.HEAD_HW"), val(sk, "Params.HEAD_ROOM"), val(sk, "Params.HEAD_OVER")
    for side, tag in ((+1, "fore"), (-1, "aft")):
        y0 = oy - room if side > 0 else -(oy + hover)
        g = add_rect(sk, tag, -hw, y0, 2 * hw, room + hover)
        dim(sk, "DistanceX", (-1, 1) + g["bl"], f"recess_{tag}_x0", "-Params.HEAD_HW")
        dim(sk, "DistanceX", g["bl"] + g["br"], f"recess_{tag}_w", "Params.HEAD_HW * 2")
        dim(sk, "DistanceY", g["br"] + g["tr"], f"recess_{tag}_d",
            "Params.HEAD_ROOM + Params.HEAD_OVER")
        at_y(sk, g["bl"] if side > 0 else g["tl"], f"recess_{tag}_face",
             "Params.OY - Params.HEAD_ROOM", side)
    pocket(body, "HeadRecess", sk, "Params.M2_HEAD_H + Params.HEAD_OVER")

    doc.recompute()
    return body


# -------------------------------------------------------------------- checks
def check(doc, body):
    """Every feature valid, every sketch fully constrained, one valid solid, and the
    clearances in CHECKS. Returns a list of problems; empty is a pass."""
    bad = []
    for o in doc.Objects:
        if "Invalid" in o.State or not o.isValid():
            bad.append(f"{o.Name}: {o.getStatusString()}")
        if o.TypeId == "Sketcher::SketchObject":
            o.solve()
            if o.DoF:
                bad.append(f"{o.Name}: {o.DoF} degrees of freedom left")
            for kind in ("ConflictingConstraints", "RedundantConstraints", "MalformedConstraints"):
                if getattr(o, kind):
                    bad.append(f"{o.Name}: {kind} {getattr(o, kind)}")
    s = body.Shape
    if s.isNull() or not s.isValid() or len(s.Solids) != 1:
        bad.append(f"body: not one valid solid ({0 if s.isNull() else len(s.Solids)} solids)")
    sheet = doc.getObject("Params")
    for alias, least in CHECKS.items():
        v = sheet.get(alias).Value
        if v < least - 1e-9:
            bad.append(f"{alias} = {v:.2f} mm, below {least}")
    return bad


# -------------------------------------------------------------------- exports
def export_svg(shape, path, size=500, margin=20):
    """Edges projected along -z, hidden ones grey and dashed, scaled to fit a
    size x size page."""
    import TechDraw
    edges = [e for e in TechDraw.project(shape, V(0, 0, 1))[:2] if not e.isNull()]
    bb = edges[0].BoundBox
    for e in edges[1:]:
        bb.add(e.BoundBox)
    scale = (size - 2 * margin) / max(bb.XLength, bb.YLength)
    line = {"stroke": "rgb(0, 0, 0)", "stroke-width": f"{1.0 / scale:.4f}"}
    dash = {"stroke": "rgb(150, 150, 150)", "stroke-width": f"{0.7 / scale:.4f}",
            "stroke-dasharray": f"{3 / scale:.4f},{3 / scale:.4f}"}
    # own styles throughout: FreeCAD 1.1.3's default hidden style is malformed SVG
    paths = TechDraw.projectToSVG(shape, V(0, 0, 1), "ShowHiddenLines", 0.01,
                                  line, line, line, dash, dash, dash)
    tx = margin - bb.XMin * scale + (size - 2 * margin - bb.XLength * scale) / 2
    ty = margin + bb.YMax * scale + (size - 2 * margin - bb.YLength * scale) / 2
    with open(path, "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
                f'viewBox="0 0 {size} {size}">\n'
                f'<g transform="translate({tx:.3f},{ty:.3f}) scale({scale:.4f})">\n'
                f'{paths}</g>\n</svg>\n')


def rotated(shape, *turns):
    s = shape.copy()
    for axis, deg in turns:
        s.rotate(V(0, 0, 0), V(*axis), deg)
    return s


def export(body, outdir):
    import MeshPart
    s = body.Shape
    s.exportStep(f"{outdir}/{PART}.step")
    mesh = MeshPart.meshFromShape(Shape=s, LinearDeflection=0.01, AngularDeflection=0.1)
    mesh.write(f"{outdir}/{PART}.stl")
    mesh.write(f"{outdir}/{PART}-print.stl")            # modelled bed-down already
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    views = {
        "plan": s,                                       # from +z: the face side
        "front": rotated(s, (X, -90), (Y, 180)),
        "side": rotated(s, (Z, -90), (X, -90)),
        "iso": rotated(s, (Y, -30), (X, -55)),
    }
    for name, shape in views.items():
        export_svg(shape, f"{outdir}/{PART}-{name}.svg")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.normpath(os.path.join(here, "..", "stl"))
    if DOC in App.listDocuments():
        App.closeDocument(DOC)
    doc = App.newDocument(DOC)
    body = build(doc)
    problems = check(doc, body)
    for p in problems:
        print("PROBLEM:", p, file=sys.stderr)
    if problems:
        raise RuntimeError(f"flow-cage: {len(problems)} problem(s), nothing saved: {problems}")
    export(body, outdir)
    fcstd = os.path.join(here, "flow-cage.FCStd")
    if os.path.exists(fcstd):
        os.remove(fcstd)                 # or FreeCAD leaves a dated .FCBak beside it
    doc.saveAs(fcstd)
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.setActiveDocument(doc.Name)
        Gui.ActiveDocument.ActiveView.viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")
    bb, p = body.Shape.BoundBox, doc.getObject("Params")
    g = lambda a: p.get(a).Value
    print(f"flow-cage: {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f} mm, "
          f"{body.Shape.Volume:.1f} mm3; ring outside {2*g('OX'):.1f} x {2*g('OY'):.1f}, "
          f"window {2*(g('IX')-g('LIP')):.1f} x {2*(g('IY')-g('LIP')):.1f}, face at z "
          f"{g('Z_FACE'):.2f}, top {g('Z_TOP'):.2f}; M2 at y +/-{g('M2_Y'):.2f}, "
          f"{g('RING_TO_HOLE'):.2f} mm clear of the ring; head edge "
          f"{g('HEAD_TO_FACE'):.2f} mm clear of the recessed face; lip window edge "
          f"{g('LIP_TO_CYL'):.2f} mm from the cylinders")


if __name__ == "__main__":
    main()
