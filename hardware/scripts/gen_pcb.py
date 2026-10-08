"""Build ledctl.kicad_pcb from the exported netlist + placement table."""
import sys, os, pcbnew
sys.path.insert(0, os.path.dirname(__file__))
from sexp import parse, find
from placement import PLACE, BOARD, HOLES

MM = pcbnew.FromMM
FPDIR = "/usr/share/kicad/footprints"
out = sys.argv[1]

net = parse(open("ledctl.net").read())
comps = {}
for c in find(find(net, "components")[0], "comp"):
    ref = c[1] if not isinstance(c[1], list) else find(c, "ref")[0][1]
    ref = find(c, "ref")[0][1]
    comps[ref] = dict(fp=find(c, "footprint")[0][1], value=find(c, "value")[0][1])
pinnet = {}
for n in find(find(net, "nets")[0], "net"):
    name = find(n, "name")[0][1].lstrip("/")
    for nd in find(n, "node"):
        pinnet[(find(nd, "ref")[0][1], find(nd, "pin")[0][1])] = name

b = pcbnew.BOARD()
b.SetCopperLayerCount(2)
ds = b.GetDesignSettings()
ds.m_TrackMinWidth = MM(0.2)
ds.m_MinClearance = MM(0.2)
ds.m_ViasMinSize = MM(0.6)
ds.m_MinThroughDrill = MM(0.2)
ds.m_CopperEdgeClearance = MM(0.25)

nets = {}
def getnet(name):
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(b, name)
        b.Add(ni)
        nets[name] = ni
    return nets[name]

for ref, info in comps.items():
    lib, fpname = info["fp"].split(":")
    fp = pcbnew.FootprintLoad(f"{FPDIR}/{lib}.pretty", fpname)
    assert fp, info["fp"]
    fp.SetReference(ref)
    fp.SetValue(info["value"])
    fp.SetFPID(pcbnew.LIB_ID(lib, fpname))
    x, y, rot, side = PLACE[ref]
    b.Add(fp)
    fp.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    if side == "B":
        fp.Flip(fp.GetPosition(), False)
    fp.SetOrientationDegrees(rot)
    for p in fp.Pads():
        n = pinnet.get((ref, p.GetNumber()))
        if n and p.GetNumber():
            p.SetNet(getnet(n))
        if ref == "U2" and p.GetNumber() == "19":
            p.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    fp.Reference().SetTextSize(pcbnew.VECTOR2I(MM(0.8), MM(0.8)))
    fp.Reference().SetTextThickness(MM(0.12))

for i, (x, y) in enumerate(HOLES):
    h = pcbnew.FootprintLoad(f"{FPDIR}/MountingHole.pretty", "MountingHole_3.2mm_M3")
    h.SetReference(f"H{i+1}")
    b.Add(h)
    h.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    h.Reference().SetVisible(False); h.Value().SetVisible(False)

# outline with rounded corners
x0, y0, x1, y1, r = BOARD
def seg(a, c):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pcbnew.VECTOR2I(MM(a[0]), MM(a[1]))); s.SetEnd(pcbnew.VECTOR2I(MM(c[0]), MM(c[1])))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1)); b.Add(s)
def arc(cx, cy, sx, sy):
    s = pcbnew.PCB_SHAPE(b); s.SetShape(pcbnew.SHAPE_T_ARC)
    s.SetCenter(pcbnew.VECTOR2I(MM(cx), MM(cy))); s.SetStart(pcbnew.VECTOR2I(MM(sx), MM(sy)))
    s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(MM(0.1)); b.Add(s)
seg((x0 + r, y0), (x1 - r, y0)); seg((x1, y0 + r), (x1, y1 - r))
seg((x1 - r, y1), (x0 + r, y1)); seg((x0, y1 - r), (x0, y0 + r))
arc(x1 - r, y0 + r, x1 - r, y0); arc(x1 - r, y1 - r, x1, y1 - r)
arc(x0 + r, y1 - r, x0 + r, y1); arc(x0 + r, y0 + r, x0, y0 + r)

# silkscreen labels
def text(s, x, y, size=1.0, layer=pcbnew.F_SilkS):
    t = pcbnew.PCB_TEXT(b); t.SetText(s); t.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size))); t.SetTextThickness(MM(size * 0.15)); t.SetLayer(layer); b.Add(t)
from placement import SILK
for s, x, y, sz in SILK:
    text(s, x, y, sz)

b.SetFileName(out)
pcbnew.SaveBoard(out, b)
print("saved", len(comps), "footprints")
