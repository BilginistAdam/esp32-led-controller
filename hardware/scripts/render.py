"""Render PCB layers to PNG for review: render.py board.kicad_pcb out_prefix"""
import subprocess, sys, cairosvg
pcb, pre = sys.argv[1], sys.argv[2]
sets = {
    "top": "F.Cu,F.SilkS,F.Fab,Edge.Cuts,F.Mask",
    "bot": "B.Cu,B.SilkS,Edge.Cuts",
    "both": "F.Cu,B.Cu,F.SilkS,Edge.Cuts",
}
for k, layers in sets.items():
    svg = f"{pre}_{k}.svg"
    subprocess.run(["kicad-cli", "pcb", "export", "svg", "-l", layers, "--page-size-mode", "2",
                    "--exclude-drawing-sheet", "-o", svg, pcb], check=True, capture_output=True)
    cairosvg.svg2png(url=svg, write_to=f"{pre}_{k}.png", output_width=1400, background_color="white")
print("rendered")
