"""Export DSN with net classes, run Freerouting, import SES, add GND pours, save."""
import re, os, subprocess, sys, pcbnew
MM = pcbnew.FromMM
PCB = "ledctl.kicad_pcb"
CLASSES = {  # name: (width_um, clearance_um, nets)
    "HighCurrent": (1500, 250, ["VIN_RAW", "VIN", "LED-"]),
    "Power": (500, 220, ["VBUCK", "SW", "+3V3", "VBUS", "GND"]),
}
b = pcbnew.LoadBoard(PCB)
pcbnew.ExportSpecctraDSN(b, "ledctl.dsn")
d = open("ledctl.dsn").read()
m = re.search(r"\(class kicad_default \"\"(.*?)\(circuit", d, re.S)
allnets = re.findall(r'"[^"]*"|\S+', m.group(1))
special = {n for c in CLASSES.values() for n in c[2]}
q = lambda n: n if re.fullmatch(r"[A-Za-z0-9_+]+", n) else f'"{n}"'
default = [n for n in allnets if n.strip('"') not in special]
via = "(circuit (use_via Via[0-1]_600:300_um))"
blk = f'(class kicad_default "" {" ".join(default)} {via} (rule (width 250) (clearance 200)))\n'
for name, (w, c, nets) in CLASSES.items():
    blk += f'    (class {name} {" ".join(q(n) for n in nets)} {via} (rule (width {w}) (clearance {c})))\n'
start = d.index("(class kicad_default")
end = d.index("(wiring")
# end of network block: last ')' before (wiring  -> keep it
net_end = d.rindex(")", start, end)
d = d[:start] + blk + "  " + d[net_end:]
open("ledctl.dsn", "w").write(d)

r = subprocess.run(["xvfb-run", "-a", "java", "-jar", os.environ.get("FREEROUTING_JAR", "freerouting.jar"), "-de", "ledctl.dsn", "-do", "ledctl.ses", "-mp", "60"],
                   capture_output=True, text=True, timeout=900)
print(r.stdout[-1500:], r.stderr[-1500:])
