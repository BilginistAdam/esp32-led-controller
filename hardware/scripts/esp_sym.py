"""Generate project symbol library with ESP32-C3-WROOM-02."""
L = 2.54
left = [("1", "3V3", "power_in", 17.78), ("2", "EN", "input", 15.24),
        ("8", "IO9", "bidirectional", 10.16), ("7", "IO8", "bidirectional", 7.62),
        ("16", "IO2", "bidirectional", 5.08), ("11", "RXD/IO20", "bidirectional", 0),
        ("12", "TXD/IO21", "bidirectional", -2.54), ("13", "IO18/USB_D-", "bidirectional", -7.62),
        ("14", "IO19/USB_D+", "bidirectional", -10.16)]
right = [("18", "IO0", "bidirectional", 17.78), ("17", "IO1", "bidirectional", 15.24),
         ("15", "IO3", "bidirectional", 12.7), ("3", "IO4", "bidirectional", 10.16),
         ("4", "IO5", "bidirectional", 7.62), ("5", "IO6", "bidirectional", 5.08),
         ("6", "IO7", "bidirectional", 2.54), ("10", "IO10", "bidirectional", 0)]
bottom = [("9", "GND", "power_in", -2.54), ("19", "GND", "passive", 2.54)]


def pin(num, name, typ, x, y, rot):
    return (f'      (pin {typ} line (at {x} {y} {rot}) (length {L})\n'
            f'        (name "{name}" (effects (font (size 1.27 1.27))))\n'
            f'        (number "{num}" (effects (font (size 1.27 1.27)))))\n')


def build():
    s = '(kicad_symbol_lib (version 20220914) (generator ledctl_gen)\n'
    s += '  (symbol "ESP32-C3-WROOM-02" (in_bom yes) (on_board yes)\n'
    s += '    (property "Reference" "U" (at -10.16 21.59 0) (effects (font (size 1.27 1.27)) (justify left)))\n'
    s += '    (property "Value" "ESP32-C3-WROOM-02" (at 0 -24.13 0) (effects (font (size 1.27 1.27))))\n'
    s += '    (property "Footprint" "RF_Module:ESP32-C3-WROOM-02" (at 0 -26.67 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (property "Datasheet" "https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))\n'
    s += '    (symbol "ESP32-C3-WROOM-02_0_1"\n'
    s += '      (rectangle (start -10.16 20.32) (end 10.16 -20.32) (stroke (width 0.254) (type default)) (fill (type background))))\n'
    s += '    (symbol "ESP32-C3-WROOM-02_1_1"\n'
    for n, nm, t, y in left:
        s += pin(n, nm, t, -12.7, y, 0)
    for n, nm, t, y in right:
        s += pin(n, nm, t, 12.7, y, 180)
    for n, nm, t, x in bottom:
        s += pin(n, nm, t, x, -22.86, 90)
    s += '    )\n  )\n)\n'
    return s


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(build())
