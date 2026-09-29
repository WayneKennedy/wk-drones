"""Shared helpers for the fleet's FreeCAD part scripts (fleet F-DEC-09, F-DEC-10).

A part script holds the part: its PARAMS, its CHECKS and a build(doc) that returns the
PartDesign body. Everything that is the same for every part is here: the `Params`
spreadsheet, sketches bound to it by expression, pads and pockets, the checks a document
must pass before it is saved, the exports, and the run that ties them together. Rules
and the reasons behind them: /AGENTS.md "CAD in FreeCAD".

Use from a part script in aircraft/<name>/print/src/:
    HERE = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.normpath(os.path.join(HERE, "../../../../fleet/cad")))
    import fcpart; importlib.reload(fcpart)     # the GUI's interpreter outlives an edit
Worked examples: aircraft/bee35/print/src/flow-cage.py, cam-mount.py.
"""

import math
import os
import sys

import FreeCAD as App
import Part
import Sketcher
from FreeCAD import Vector as V

X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


# -------------------------------------------------------------------- spreadsheet
def make_params(doc, params):
    """The `Params` sheet from (alias, value or formula, note) rows. Every value carries
    its unit; all are written as expressions, which is what keeps a negative one a number."""
    sh = doc.addObject("Spreadsheet::Sheet", "Params")
    for col, head in zip("ABC", ("name", "value", "source / note")):
        sh.set(f"{col}1", head)
    sh.setStyle("A1:C1", "bold")
    for row, (alias, value, note) in enumerate(params, start=2):
        sh.set(f"A{row}", alias)
        sh.set(f"B{row}", value if value.startswith("=") else "=" + value)
        sh.setAlias(f"B{row}", alias)
        sh.set(f"C{row}", note)
    sh.setColumnWidth("A", 120)
    sh.setColumnWidth("B", 90)
    sh.setColumnWidth("C", 700)
    doc.recompute()
    return sh


# -------------------------------------------------------------------- sketches
def new_sketch(body, name, z_expr=None, plane="XY"):
    """A sketch on one of the body's origin planes, optionally lifted along the plane's
    normal to z_expr. Sketch axes in the part's frame: XY -> (x, y), normal +z;
    XZ -> (x, z), normal -y; YZ -> (y, z), normal +x."""
    base = [o for o in body.Origin.OriginFeatures if o.Role == plane + "_Plane"][0]
    sk = body.newObject("Sketcher::SketchObject", name)
    sk.AttachmentSupport = (base, [""])
    sk.MapMode = "FlatFace"
    if z_expr:
        sk.setExpression("AttachmentOffset.Base.z", z_expr)
    return sk


def val(obj, expr):
    """The number an expression has now, in mm or degrees."""
    q = obj.evalExpression(expr)
    return float(getattr(q, "Value", q))


def dim(sk, kind, refs, name, expr):
    """A named dimensional constraint bound to a spreadsheet expression."""
    i = sk.addConstraint(Sketcher.Constraint(kind, *refs, val(sk, expr)))
    sk.renameConstraint(i, name)
    sk.setExpression("Constraints." + name, expr)


def at_x(sk, point, name, expr):
    """Put a point at sketch x = expr, which may be negative."""
    dim(sk, "DistanceX", (-1, 1) + point, name, expr)


def at_y(sk, point, name, expr, side=+1):
    """Put a point at sketch y = side * expr. With side = -1 the constraint is drawn the
    other way round, so an expression that is a positive length stays positive."""
    refs = (-1, 1) + point if side > 0 else point + (-1, 1)
    dim(sk, "DistanceY", refs, name, expr)


def add_rect(sk, tag, x0, y0, w, h):
    """Sharp rectangle, lines bottom-right-top-left. Returns corner points bl, br, tr, tl.
    x0, y0, w, h are numbers for the first placement only; the caller binds width,
    height and position."""
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


def add_circle(sk, tag, x, y, d_expr, x_expr=None, y_expr=None):
    """A circle of bound diameter. Its centre is bound to x_expr and y_expr; where one is
    None the centre is put on that axis of the sketch instead (x = 0 or y = 0).
    Returns the centre point."""
    c = sk.addGeometry(Part.Circle(V(x, y, 0), V(0, 0, 1), val(sk, d_expr) / 2), False)
    dim(sk, "Diameter", (c,), tag + "_d", d_expr)
    if x_expr is None and y_expr is None:
        sk.addConstraint(Sketcher.Constraint("Coincident", c, 3, -1, 1))
        return (c, 3)
    if x_expr is None:
        sk.addConstraint(Sketcher.Constraint("PointOnObject", c, 3, -2))
    else:
        at_x(sk, (c, 3), tag + "_x", x_expr)
    if y_expr is None:
        sk.addConstraint(Sketcher.Constraint("PointOnObject", c, 3, -1))
    else:
        at_y(sk, (c, 3), tag + "_y", y_expr)
    return (c, 3)


def centre_on_origin(sk, a, b):
    """Two diagonal points symmetric about the origin POINT: centres in x and y at once,
    and is not redundant with Horizontal/Vertical the way an axis symmetry is."""
    sk.addConstraint(Sketcher.Constraint("Symmetric", *a, *b, -1, 1))


# -------------------------------------------------------------------- features
def _both_sides(f):
    if hasattr(f, "SideType"):
        f.SideType = "Symmetric"
    else:
        f.Midplane = True


def pad(body, name, sketch, length_expr, both=False):
    """Pad along the sketch normal; both=True pads the length symmetrically about it."""
    f = body.newObject("PartDesign::Pad", name)
    f.Profile = sketch
    f.setExpression("Length", length_expr)
    if both:
        _both_sides(f)
    sketch.Visibility = False
    return f


def pocket(body, name, sketch, length_expr=None, both=False):
    """Cut ALONG the sketch normal (a Pocket's own default is against it): a set length,
    or through all when none is given. both=True cuts both ways from the sketch."""
    f = body.newObject("PartDesign::Pocket", name)
    f.Profile = sketch
    if length_expr:
        f.Type = 0
        f.setExpression("Length", length_expr)
    else:
        f.Type = 1
    if both:
        _both_sides(f)
    else:
        f.Reversed = True
    sketch.Visibility = False
    return f


def edges_where(feature, test, expect, what):
    """Names of the feature's edges that pass test(edge). Edges are found by where they
    are, never by number, and the count must be what is expected."""
    names = [f"Edge{n}" for n, e in enumerate(feature.Shape.Edges, start=1) if test(e)]
    if len(names) != expect:
        raise RuntimeError(f"expected {expect} edges for {what}, found {names}")
    return names


def dress(body, kind, name, base, edges, prop, expr):
    """A Fillet or Chamfer on named edges of `base`. Make it the last feature, so nothing
    later renumbers the edges it names."""
    f = body.newObject("PartDesign::" + kind, name)
    f.Base = (base, edges)
    f.setExpression(prop, expr)
    base.Visibility = False
    return f


# -------------------------------------------------------------------- checks
def check(doc, body, checks):
    """Every object valid, every sketch fully constrained with nothing redundant, one
    valid solid, and each alias in `checks` at or above its least value. Returns a list
    of problems; empty is a pass."""
    bad = []
    for o in doc.Objects:
        if "Invalid" in o.State or not o.isValid():
            bad.append(f"{o.Name}: {o.getStatusString()}")
        if o.TypeId == "Sketcher::SketchObject":
            o.solve()
            if o.DoF:
                bad.append(f"{o.Name}: {o.DoF} degrees of freedom left")
            for kind in ("ConflictingConstraints", "RedundantConstraints",
                         "PartiallyRedundantConstraints", "MalformedConstraints"):
                if getattr(o, kind):
                    bad.append(f"{o.Name}: {kind} {getattr(o, kind)}")
    s = body.Shape
    if s.isNull() or not s.isValid() or len(s.Solids) != 1:
        bad.append(f"body: not one valid solid ({0 if s.isNull() else len(s.Solids)} solids)")
    sheet = doc.getObject("Params")
    for alias, least in checks.items():
        v = sheet.get(alias).Value
        if v < least - 1e-9:
            bad.append(f"{alias} = {v:.2f} mm, below {least}")
    return bad


# -------------------------------------------------------------------- exports
def rotated(shape, *turns):
    """A copy turned about the origin by each (axis, degrees) in order."""
    s = shape.copy()
    for axis, deg in turns:
        s.rotate(V(0, 0, 0), V(*axis), deg)
    return s


def on_bed(shape, *turns):
    """A copy turned into its print orientation and dropped onto z = 0."""
    s = rotated(shape, *turns)
    s.translate(V(0, 0, -s.BoundBox.ZMin))
    return s


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


def write_stl(shape, path):
    import MeshPart
    MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.01, AngularDeflection=0.1).write(path)


def export(body, outdir, part, views, print_turns=()):
    """<part>.step and .stl as modelled, <part>-print.stl turned by print_turns and put on
    the bed, and <part>-<view>.svg for each view, a name and the turns that face it to +z."""
    s = body.Shape
    s.exportStep(f"{outdir}/{part}.step")
    write_stl(s, f"{outdir}/{part}.stl")
    write_stl(on_bed(s, *print_turns), f"{outdir}/{part}-print.stl")
    for name, turns in views.items():
        export_svg(rotated(s, *turns), f"{outdir}/{part}-{name}.svg")


# -------------------------------------------------------------------- run
def run(script, doc_name, part, build, checks, views, print_turns=(), summary=None):
    """Build the part in a fresh document, check it, and only then export to ../stl/ and
    save <script>.FCStd beside the script. A document of that name already open is the
    one the owner has been editing by hand: it is kept as <script>.replaced.FCStd
    before it is closed."""
    here = os.path.dirname(os.path.abspath(script))
    stem = os.path.splitext(os.path.basename(script))[0]
    outdir = os.path.normpath(os.path.join(here, "..", "stl"))
    if doc_name in App.listDocuments():
        App.getDocument(doc_name).saveCopy(os.path.join(here, stem + ".replaced.FCStd"))
        App.closeDocument(doc_name)
    doc = App.newDocument(doc_name)
    body = build(doc)
    problems = check(doc, body, checks)
    for p in problems:
        print("PROBLEM:", p, file=sys.stderr)
    if problems:
        raise RuntimeError(f"{stem}: {len(problems)} problem(s), nothing saved: {problems}")
    export(body, outdir, part, views, print_turns)
    fcstd = os.path.join(here, stem + ".FCStd")
    if os.path.exists(fcstd):
        os.remove(fcstd)                 # or FreeCAD leaves a dated .FCBak beside it
    doc.saveAs(fcstd)
    if App.GuiUp:
        import FreeCADGui as Gui
        Gui.setActiveDocument(doc.Name)
        Gui.ActiveDocument.ActiveView.viewIsometric()
        Gui.SendMsgToActiveView("ViewFit")
    bb = body.Shape.BoundBox
    p = doc.getObject("Params")
    print(f"{stem}: {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f} mm, "
          f"{body.Shape.Volume:.1f} mm3"
          + ("; " + summary(lambda a: p.get(a).Value) if summary else ""))
    return doc, body
