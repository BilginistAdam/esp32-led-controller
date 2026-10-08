import uuid, sys, os, copy
from sexp import *
from design import PARTS, NOTES, P

OUT = sys.argv[1]
PROJ = os.path.basename(OUT).replace(".kicad_sch", "")
LIBDIR = os.path.dirname(os.path.abspath(OUT))
U = lambda: str(uuid.uuid4())
ROOT = U()


def libpath(lib):
    return f"{LIBDIR}/{P}.kicad_sym" if lib == P else lib


def g(v):  # snap to 0.01
    return round(v, 2)


lib_symbols = {}
body = []
pinpos = {}  # (ref,pin)->(x,y,dir)

for ref, (lib, name, value, fp, (sx, sy), conns) in PARTS.items():
    sym = getsym(libpath(lib), name)
    full = f"{lib}:{name}"
    if full not in lib_symbols:
        e = copy.deepcopy(sym)
        e[1] = full
        lib_symbols[full] = e
    pins_ = pins(sym)
    props = []
    for pr in find(sym, "property"):
        k = pr[1]
        at = find(pr, "at")[0]
        val = {"Reference": ref, "Value": value, "Footprint": fp}.get(k, pr[2])
        eff = find(pr, "effects")
        e = copy.deepcopy(eff[0]) if eff else [Sym("effects"), [Sym("font"), [Sym("size"), 1.27, 1.27]]]
        if k == "Reference" and ref.startswith("#"):
            if not any(x == "hide" for x in e): e.append(Sym("hide"))
        props.append([Sym("property"), k, val,
                      [Sym("at"), g(sx + float(at[1])), g(sy - float(at[2])), float(at[3]) if len(at) > 3 else 0], e])
    inst = [Sym("symbol"), [Sym("lib_id"), full], [Sym("at"), sx, sy, 0], [Sym("unit"), 1],
            [Sym("in_bom"), Sym("no" if ref.startswith("#") else "yes")], [Sym("on_board"), Sym("yes")],
            [Sym("dnp"), Sym("no")], [Sym("uuid"), U()]] + props
    seen = set()
    for p in pins_:
        if p["num"] in seen: continue
        seen.add(p["num"])
        inst.append([Sym("pin"), p["num"], [Sym("uuid"), U()]])
    inst.append([Sym("instances"), [Sym("project"), PROJ, [Sym("path"), "/" + ROOT, [Sym("reference"), ref], [Sym("unit"), 1]]]])
    body.append(inst)
    # connections
    done = {}
    for p in pins_:
        px, py = g(sx + p["x"]), g(sy - p["y"])
        out = {0: (-1, 0), 180: (1, 0), 90: (0, 1), 270: (0, -1)}[p["rot"]]
        net = conns.get(p["num"])
        key = (px, py)
        if key in done:
            assert done[key] == net, (ref, p)
            continue
        done[key] = net
        if net is None:
            body.append([Sym("no_connect"), [Sym("at"), px, py], [Sym("uuid"), U()]])
            continue
        if ref.startswith("#FLG"):
            ex, ey = px, py
            ang = 270
        else:
            ex, ey = g(px + out[0] * 2.54), g(py + out[1] * 2.54)
            body.append([Sym("wire"), [Sym("pts"), [Sym("xy"), px, py], [Sym("xy"), ex, ey]],
                         [Sym("stroke"), [Sym("width"), 0], [Sym("type"), Sym("default")]], [Sym("uuid"), U()]])
            ang = {(-1, 0): 180, (1, 0): 0, (0, 1): 270, (0, -1): 90}[out]
        just = {0: "left", 90: "left", 180: "right", 270: "right"}[ang]
        body.append([Sym("label"), net, [Sym("at"), ex, ey, ang], [Sym("fields_autoplaced")],
                     [Sym("effects"), [Sym("font"), [Sym("size"), 1.27, 1.27]], [Sym("justify"), Sym(just), Sym("bottom")]],
                     [Sym("uuid"), U()]])
    for pn in conns:
        assert pn in {p["num"] for p in pins_}, (ref, pn)

for (x, y), t in NOTES:
    body.append([Sym("text"), t, [Sym("at"), x, y, 0],
                 [Sym("effects"), [Sym("font"), [Sym("size"), 1.6, 1.6], Sym("bold")], [Sym("justify"), Sym("left"), Sym("bottom")]],
                 [Sym("uuid"), U()]])

doc = [Sym("kicad_sch"), [Sym("version"), 20230121], [Sym("generator"), Sym("eeschema")], [Sym("uuid"), ROOT],
       [Sym("paper"), "A4"],
       [Sym("title_block"), [Sym("title"), "LED Controller - ESP32-C3 LED Strip Controller"], [Sym("rev"), "A"], [Sym("company"), "Bilginier"],
        [Sym("comment"), 1, "12-24V LED serit, WiFi ac/kapa + PWM"]],
       [Sym("lib_symbols")] + list(lib_symbols.values())] + body + [
       [Sym("sheet_instances"), [Sym("path"), "/", [Sym("page"), "1"]]]]
open(OUT, "w").write(dump(doc) + "\n")
print("ok", len(PARTS), "parts")
