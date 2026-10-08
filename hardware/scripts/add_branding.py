"""Add Bilginier logo + product name to the top silkscreen (run after finish.py).

Usage (from hardware/):  python3 scripts/add_branding.py
"""
import os, sys, pcbnew
HERE = os.path.dirname(os.path.abspath(__file__))
import json, subprocess
LOGO = os.path.join(HERE, "..", "..", "docs", "logo", "logo.py")
# shapely and KiCad's SWIG bindings clash in one process, so the logo is computed in a child process
POLYS = json.loads(subprocess.check_output([sys.executable, LOGO, "--json"]))

MM = pcbnew.FromMM
PCB = "ledctl.kicad_pcb"
CENTER = (134.0, 114.0)      # logo center on the board (mm)
HEIGHT = 6.4                 # logo height (mm); stroke ~0.25 mm at this size
KEEPOUT = (125.5, 110.6, 142.5, 121.6)   # no stitch vias under the artwork

b = pcbnew.LoadBoard(PCB)

# 1) drop the old placeholder text and earlier branding (idempotent)
for d in list(b.GetDrawings()):
    if d.GetLayer() == pcbnew.F_SilkS:
        if isinstance(d, pcbnew.PCB_TEXT) and ("LED CTRL" in d.GetText() or "LED Controller" in d.GetText()
                                               or "BILGINIER" in d.GetText()):
            b.Delete(d)
        elif isinstance(d, pcbnew.PCB_SHAPE) and d.GetShape() == pcbnew.SHAPE_T_POLY:
            b.Delete(d)

# 2) remove GND stitching vias (4 mm grid) inside the artwork area
x0, y0, x1, y1 = KEEPOUT
removed = 0
for t in list(b.GetTracks()):
    if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND":
        x, y = pcbnew.ToMM(t.GetPosition().x), pcbnew.ToMM(t.GetPosition().y)
        on_grid = abs((x - 102) % 4) < 1e-3 and abs((y - 102) % 4) < 1e-3
        if on_grid and x0 <= x <= x1 and y0 <= y <= y1:
            b.Delete(t); removed += 1

# 3) logo polygons
xs = [x for p in POLYS for x, _ in p["ext"]]; ys = [y for p in POLYS for _, y in p["ext"]]
bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
sc = HEIGHT / (by1 - by0)
ox, oy = CENTER[0] - (bx0 + bx1) / 2 * sc, CENTER[1] - (by0 + by1) / 2 * sc
polys = POLYS
for pg in polys:
    ps = pcbnew.SHAPE_POLY_SET()
    ps.NewOutline()
    for x, y in pg["ext"]:
        ps.Append(MM(ox + x * sc), MM(oy + y * sc))
    for hi, hole in enumerate(pg["holes"]):
        ps.NewHole()
        for x, y in hole:
            ps.Append(MM(ox + x * sc), MM(oy + y * sc), -1, hi)
    ps.Fracture(pcbnew.SHAPE_POLY_SET.PM_FAST)
    s = pcbnew.PCB_SHAPE(b)
    s.SetShape(pcbnew.SHAPE_T_POLY)
    s.SetPolyShape(ps)
    s.SetFilled(True)
    s.SetWidth(0)
    s.SetLayer(pcbnew.F_SilkS)
    b.Add(s)

# 4) text
def text(t, x, y, size, bold=False):
    tx = pcbnew.PCB_TEXT(b)
    tx.SetText(t); tx.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    tx.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
    tx.SetTextThickness(MM(size * (0.2 if bold else 0.15)))
    tx.SetLayer(pcbnew.F_SilkS); b.Add(tx)

text("LED Controller", CENTER[0], CENTER[1] + HEIGHT / 2 + 1.4, 1.2, bold=True)
text("BILGINIER  rev A", CENTER[0], CENTER[1] + HEIGHT / 2 + 3.2, 0.9)

pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(PCB, b)
print(f"branding added ({len(polys)} polygons, {removed} stitch vias removed under artwork)")
