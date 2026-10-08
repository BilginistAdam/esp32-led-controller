"""Bilginier logo: circuit brain (brain outline + central chip + traces).

Single source for every target:
  python3 logo.py            -> writes SVGs (mono, color, banners) next to this file
Other scripts import `primitives()` / `filled()` for KiCad silkscreen and OpenSCAD.
Units: design canvas 240 x 100, y axis pointing down.
"""
import math
from shapely.geometry import Point, LineString, Polygon, box
from shapely.ops import unary_union

W, H = 240.0, 100.0
CX, CY = 120.0, 50.0
STROKE = 3.6


def _brain_outline():
    """Bumpy two-lobed brain silhouette as a closed point list."""
    lobes = []
    rx, ry = 47.0, 41.0
    for i in range(18):
        a = 2 * math.pi * i / 18
        x = CX + rx * math.cos(a)
        y = CY + ry * math.sin(a)
        lobes.append(Point(x, y).buffer(13.5, quad_segs=24))
    core = Point(CX, CY).buffer(1.0).buffer(0)
    core = Polygon([(CX + (rx - 6) * math.cos(t), CY + (ry - 6) * math.sin(t))
                    for t in [2 * math.pi * k / 120 for k in range(120)]])
    shape = unary_union(lobes + [core])
    # central fissure notches top and bottom
    notch = unary_union([Point(CX, CY - ry - 13).buffer(6.5), Point(CX, CY + ry + 13).buffer(6.5)])
    shape = shape.difference(notch).simplify(0.25)
    return list(shape.exterior.coords)


def primitives():
    """Return dict of drawing primitives (all stroked with STROKE unless noted)."""
    brain = _brain_outline()
    s = 34.0                       # chip size
    chip = [(CX - s / 2, CY - s / 2), (CX + s / 2, CY - s / 2), (CX + s / 2, CY + s / 2), (CX - s / 2, CY + s / 2)]
    core = (CX - 8.5, CY - 8.5, CX + 8.5, CY + 8.5)    # filled die
    pins = []
    for k in (-10, 0, 10):
        pins += [[(CX + k, CY - s / 2), (CX + k, CY - s / 2 - 6)],    # top
                 [(CX + k, CY + s / 2), (CX + k, CY + s / 2 + 6)]]    # bottom
    traces, rings = [], []
    for sx in (-1, 1):                                             # left / right
        x0 = CX + sx * s / 2
        for dy, bend in ((-10, -1), (0, 0), (10, 1)):
            y = CY + dy
            if bend == 0:
                pts = [(x0, y), (CX + sx * 96, y)]
            else:
                xb = CX + sx * 70
                pts = [(x0, y), (xb, y), (xb + sx * 12, y + bend * 12), (CX + sx * 92, y + bend * 12)]
            traces.append(pts)
            rings.append((pts[-1][0] + sx * 5.5, pts[-1][1], 5.0))
    # sulci inside the brain (short curved strokes), mirrored
    sulci = []
    for sx in (-1, 1):
        sulci.append([(CX + sx * 30, CY - 34), (CX + sx * 36, CY - 26), (CX + sx * 46, CY - 26)])
        sulci.append([(CX + sx * 30, CY + 34), (CX + sx * 36, CY + 26), (CX + sx * 46, CY + 26)])
    # central fissure: top notch -> chip, chip -> bottom notch
    sulci.append([(CX, CY - 41 - 6), (CX, CY - s / 2 - 10)])
    sulci.append([(CX, CY + s / 2 + 10), (CX, CY + 41 + 6)])
    return dict(brain=brain, chip=chip, core=core, pins=pins, traces=traces, rings=rings, sulci=sulci)


def filled(stroke_mul=1.0):
    """Union of all stroked primitives as shapely geometry (for engraving / silkscreen fills)."""
    p = primitives()
    w = STROKE * stroke_mul / 2
    geo = [LineString(p["brain"] + [p["brain"][0]]).buffer(w),
           LineString(p["chip"] + [p["chip"][0]]).buffer(w, join_style=2),
           box(*p["core"])]
    geo += [LineString(l).buffer(w) for l in p["pins"] + p["traces"] + p["sulci"]]
    geo += [Point(x, y).buffer(r + w).difference(Point(x, y).buffer(max(r - w, 0.4))) for x, y, r in p["rings"]]
    # keep traces from crossing the chip interior: clear chip body then redraw outline
    return unary_union(geo).simplify(0.1)


def bounds():
    return filled().bounds


# ------------------------------------------------------------------ SVG output
def _path(pts, closed=False):
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    return d + (" Z" if closed else "")


def svg_body(ink, brain_fill=None, chip_fill=None, die_fill=None):
    p = primitives()
    out = []
    a = f'stroke="{ink}" stroke-width="{STROKE}" stroke-linecap="round" stroke-linejoin="round"'
    out.append(f'<path d="{_path(p["brain"], True)}" fill="{brain_fill or "none"}" {a}/>')
    for l in p["sulci"]:
        out.append(f'<path d="{_path(l)}" fill="none" {a}/>')
    for l in p["traces"] + p["pins"]:
        out.append(f'<path d="{_path(l)}" fill="none" {a}/>')
    for x, y, r in p["rings"]:
        out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{chip_fill or "none"}" {a}/>')
    out.append(f'<path d="{_path(p["chip"], True)}" fill="{chip_fill or "none"}" {a.replace("round", "miter", 1)}/>')
    x0, y0, x1, y1 = p["core"]
    out.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{die_fill or ink}"/>')
    return "\n  ".join(out)


def logo_svg(ink="#1d2b3a", **fills):
    x0, y0, x1, y1 = bounds()
    m = 2
    vb = f"{x0 - m:.1f} {y0 - m:.1f} {x1 - x0 + 2 * m:.1f} {y1 - y0 + 2 * m:.1f}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">\n  {svg_body(ink, **fills)}\n</svg>\n'


def banner_svg(dark=False):
    bg = "#141413" if dark else "#ffffff"
    ink = "#ecebe6" if dark else "#1d2b3a"
    sub = "#9a9a92" if dark else "#6b6b66"
    x0, y0, x1, y1 = bounds()
    lw = x1 - x0
    sc = 150 / (y1 - y0)
    tx = 40 + lw * sc + 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 230" font-family="Segoe UI, Helvetica, Arial, sans-serif">
  <rect width="1000" height="230" rx="18" fill="{bg}"/>
  <g transform="translate({40 - x0 * sc:.1f} {40 - y0 * sc:.1f}) scale({sc:.3f})">
  {svg_body(ink, brain_fill="#f4a93b", chip_fill="#3ec1c9", die_fill=ink)}
  </g>
  <text x="{tx:.0f}" y="112" font-size="64" font-weight="700" fill="{ink}">LED Controller</text>
  <text x="{tx:.0f}" y="160" font-size="30" letter-spacing="9" font-weight="600" fill="{sub}">BILGINIER</text>
</svg>
'''


def polygons_json(stroke_mul=1.0):
    """[{'ext': [[x,y],...], 'holes': [[[x,y],...],...]}, ...] in design units."""
    g = filled(stroke_mul)
    gs = list(g.geoms) if hasattr(g, "geoms") else [g]
    return [{"ext": [list(c) for c in p.exterior.coords[:-1]],
             "holes": [[list(c) for c in h.coords[:-1]] for h in p.interiors]} for p in gs]


if __name__ == "__main__":
    import os, sys, json
    if "--json" in sys.argv:
        mul = float(sys.argv[sys.argv.index("--json") + 1]) if len(sys.argv) > sys.argv.index("--json") + 1 else 1.0
        print(json.dumps(polygons_json(mul)))
        sys.exit(0)
    here = os.path.dirname(os.path.abspath(__file__))
    files = {
        "bilginier-logo-mono.svg": logo_svg("#000000"),
        "bilginier-logo.svg": logo_svg("#1d2b3a", brain_fill="#f4a93b", chip_fill="#3ec1c9"),
        "banner-light.svg": banner_svg(False),
        "banner-dark.svg": banner_svg(True),
    }
    for n, s in files.items():
        open(os.path.join(here, n), "w").write(s)
    print("wrote", ", ".join(files), "bounds", [round(v, 1) for v in bounds()])
