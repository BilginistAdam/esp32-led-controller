import pcbnew, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from placement import BOARD
MM = pcbnew.FromMM
b = pcbnew.LoadBoard("ledctl.kicad_pcb")
from sexp import parse, find
ses = parse(open("ledctl.ses").read())
ro = find(ses, "routes")[0]
res = float(find(ro, "resolution")[0][2])          # units per um
U2MM = lambda v: pcbnew.FromMM(float(v) / res / 1000.0)
LAY = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}
for t in list(b.GetTracks()): b.Remove(t)
nt = nv = 0
for net in find(find(ro, "network_out")[0], "net"):
    ni = b.FindNet(net[1])
    for w in find(net, "wire"):
        path = find(w, "path")[0]
        lay, width, pts = path[1], path[2], path[3:]
        xy = [(U2MM(pts[i]), -U2MM(pts[i + 1])) for i in range(0, len(pts), 2)]
        for a, c in zip(xy, xy[1:]):
            t = pcbnew.PCB_TRACK(b)
            t.SetStart(pcbnew.VECTOR2I(*a)); t.SetEnd(pcbnew.VECTOR2I(*c))
            t.SetWidth(U2MM(width)); t.SetLayer(LAY[str(lay)]); t.SetNet(ni); b.Add(t); nt += 1
    for v in find(net, "via"):
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pcbnew.VECTOR2I(U2MM(v[2]), -U2MM(v[3])))
        via.SetWidth(pcbnew.FromMM(0.6)); via.SetDrill(pcbnew.FromMM(0.3)); via.SetNet(ni); b.Add(via); nv += 1
print("imported tracks", nt, "vias", nv)
gnd = b.FindNet("GND")
x0, y0, x1, y1, r = BOARD
for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
    z = pcbnew.ZONE(b)
    z.SetLayer(layer)
    z.SetNet(gnd)
    ol = z.Outline()
    ol.NewOutline()
    for x, y in [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]:
        ol.Append(MM(x), MM(y))
    z.SetLocalClearance(MM(0.3))
    z.SetMinThickness(MM(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(MM(0.3))
    z.SetThermalReliefSpokeWidth(MM(0.5))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    b.Add(z)

# GND stitching vias on a grid where free (checked later by DRC; remove offenders)
stitch = []
for gx in range(102, 164, 4):
    for gy in range(102, 138, 4):
        v = pcbnew.PCB_VIA(b)
        v.SetPosition(pcbnew.VECTOR2I(MM(gx + 0.0), MM(gy + 0.0)))
        v.SetWidth(MM(0.6)); v.SetDrill(MM(0.3)); v.SetNet(gnd)
        stitch.append(v)

def collides(v):
    pos = v.GetPosition(); rad = MM(0.3 + 0.35)
    bb = pcbnew.BOX2I(pcbnew.VECTOR2I(pos.x - rad, pos.y - rad), pcbnew.VECTOR2I(2 * rad, 2 * rad))
    for fp in b.GetFootprints():
        if fp.GetCourtyard(pcbnew.F_CrtYd).Collide(pcbnew.VECTOR2I(pos.x, pos.y), MM(0.4)):
            return True
        if fp.GetReference() == "U2":  # whole module + antenna area
            if fp.GetBoundingBox(False, False).Contains(pos): return True
    for t in b.GetTracks():
        if t.GetBoundingBox().Intersects(bb):
            if t.GetNetname() != "GND" or t.Type() == pcbnew.PCB_VIA_T:
                if t.HitTest(pos, MM(0.3 + 0.3 + 0.25)): return True
    ex = MM(1.0)
    if not (MM(x0) + ex < pos.x < MM(x1) - ex and MM(y0) + ex < pos.y < MM(y1) - ex): return True
    return False

n = 0
for v in stitch:
    if not collides(v):
        b.Add(v); n += 1
print("stitch vias", n)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard("ledctl.kicad_pcb", b)
pcbnew.WriteDRCReport(b, "drc.rpt", pcbnew.EDA_UNITS_MILLIMETRES, True)
print(open("drc.rpt").read()[-3000:])
