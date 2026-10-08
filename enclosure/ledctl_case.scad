// ESP32-C3 LED Strip Controller - 3D printable enclosure (rev A)
// Coordinates: X = board_x - 100, Y = 138 - board_y (KiCad board coords),
// so the PCB occupies X 0..64, Y 0..38; USB-C faces -Y, terminals face -X.
//
// Render:  openscad -D 'part="base"' -o base.stl ledctl_case.scad
//          openscad -D 'part="lid"'  -o lid.stl  ledctl_case.scad
// part = "base" | "lid" | "assembly"

part = "assembly";

include <bilginier_logo.scad>

/* [Fit] */
clr        = 0.5;    // PCB to wall clearance
wall       = 2.0;
floor_t    = 2.0;
lid_t      = 2.0;
corner_r   = 3.0;

/* [PCB] */
pcb_w      = 64;
pcb_h      = 38;
pcb_t      = 1.6;
standoff_h = 5.0;    // floor top -> PCB bottom (room for THT pins + keyhole screw heads)
comp_h     = 11.5;   // PCB top -> lid underside (terminal blocks ~10 mm, pin header 8.5 mm)
antenna_x  = 70.0;   // ESP32-C3-WROOM-02 overhangs the right PCB edge

/* [Fasteners] */
// M3 screws go lid -> lid post -> PCB hole -> base standoff. M3x20 recommended.
standoff_d   = 6.5;
pilot_d      = 2.6;  // M3 self-tapping into plastic (use 4.0 for M3 heat-set inserts)
post_d       = 5.5;
screw_clear  = 3.4;

/* [Wall mount] */
keyhole_head = 8.5;  // screw head pass-through
keyhole_slot = 4.2;  // screw shank
keyhole_len  = 8.0;

$fn = 48;

// ---------------------------------------------------------------- data
holes = [[59, 35.0], [59, 3.5], [4, 3.4], [14.5, 21.2]];   // H1..H4
term_pins  = [[5, 33.5], [5, 28.4], [5, 16.0], [5, 10.9]]; // J1+, J1-, J2+, J2-
term_spans = [[25.88, 36.04], [8.38, 18.54]];               // J1, J2 (Y range)
usb_c      = [30, 0];                                       // J3 mouth center
buttons    = [[15, 4.5, "RST"], [42.5, 4.5, "BTN"]];        // SW1, SW2
status_led = [49.5, 3.4];                                   // D4
keyholes   = [[25, 14], [45, 14]];                          // slot points +Y (= up on the wall)

// derived
in_x0 = -clr;            in_x1 = antenna_x + 1.0;
in_y0 = -clr;            in_y1 = pcb_h + clr;
out_x0 = in_x0 - wall;   out_x1 = in_x1 + wall;
out_y0 = in_y0 - wall;   out_y1 = in_y1 + wall;
pcb_z  = floor_t + standoff_h;          // PCB bottom
top_z  = pcb_z + pcb_t;                 // PCB top
base_h = top_z + comp_h;                // base wall height = lid underside

module rrect(x0, y0, x1, y1, h, r) {
  translate([x0 + r, y0 + r, 0])
    linear_extrude(h) offset(r) square([x1 - x0 - 2 * r, y1 - y0 - 2 * r]);
}

module slot2d(l, w) { hull() { circle(d = w); translate([l, 0]) circle(d = w); } }

// ---------------------------------------------------------------- base
module base() {
  difference() {
    union() {
      difference() {
        rrect(out_x0, out_y0, out_x1, out_y1, base_h, corner_r);
        translate([0, 0, floor_t]) rrect(in_x0, in_y0, in_x1, in_y1, base_h, 1);
      }
      for (h = holes) translate([h[0], h[1], 0]) cylinder(d = standoff_d, h = pcb_z);
    }
    // standoff pilot holes
    for (h = holes) translate([h[0], h[1], floor_t - 1.5]) cylinder(d = pilot_d, h = 50);
    // terminal block wire openings (left wall)
    for (s = term_spans)
      translate([out_x0 - 1, s[0] - 0.5, top_z - 0.2]) cube([wall + 2, s[1] - s[0] + 1, 8.2]);
    // USB-C opening (front wall), sized for typical cable overmolds
    translate([usb_c[0], out_y0 - 1, top_z + 1.6]) rotate([-90, 0, 0])
      linear_extrude(wall + 2) offset(2.5) square([11 - 5, 6.5 - 5], center = true);
    // wall keyholes
    for (k = keyholes) translate([k[0], k[1], -1]) {
      cylinder(d = keyhole_head, h = floor_t + 2);
      linear_extrude(floor_t + 2) rotate(90) slot2d(keyhole_len, keyhole_slot);
    }
    // bottom label
    translate([(out_x0 + out_x1) / 2, out_y1 - 8, -0.01]) mirror([1, 0, 0])
      linear_extrude(0.5) text("LED CTRL rev A", size = 4, halign = "center", font = "Liberation Sans:style=Bold");
  }
}

// ---------------------------------------------------------------- lid
peg_gap  = 0.4;   // peg tip to tact switch actuator
sw_h     = 1.5;   // TS-1187A actuator height
module lid() {
  tongue_w = 6; tongue_l = 13; cut = 0.8;
  difference() {
    union() {
      rrect(out_x0, out_y0, out_x1, out_y1, lid_t, corner_r);
      // screw posts that clamp the PCB onto the standoffs
      for (h = holes) translate([h[0], h[1], -comp_h]) cylinder(d = post_d, h = comp_h);
      // button pegs hanging from the flexure tongues
      for (b = buttons) translate([b[0], b[1], -(comp_h - sw_h - peg_gap)])
        cylinder(d = 3, h = comp_h - sw_h - peg_gap);
      // status LED light tube
      translate([status_led[0], status_led[1], -(comp_h - 1)]) cylinder(d = 3.6, h = comp_h - 1);
      // stiffening rim that keys into the base opening (skips the terminal side)
      difference() {
        translate([0, 0, -2]) rrect(in_x0 + 0.3, in_y0 + 0.3, in_x1 - 0.3, in_y1 - 0.3, 2, 1);
        translate([0, 0, -3]) rrect(in_x0 + 1.5, in_y0 + 1.5, in_x1 - 1.5, in_y1 - 1.5, 4, 1);
        translate([in_x0 - 1, in_y0 - 1, -3]) cube([12, in_y1 - in_y0 + 2, 4]);   // terminal blocks
        translate([usb_c[0] - 8, in_y0 - 1, -3]) cube([16, 3, 4]);                // USB-C
      }
    }
    // screw holes + head counterbore
    for (h = holes) translate([h[0], h[1], -comp_h - 1]) cylinder(d = screw_clear, h = comp_h + lid_t + 2);
    // terminal screwdriver access
    for (p = term_pins) translate([p[0] - 1, p[1], -1]) linear_extrude(lid_t + 2) slot2d(2, 4.2);
    // flexure tongues: U-shaped cut around each button pad, hinge toward +Y
    for (b = buttons) translate([b[0], b[1], -1]) linear_extrude(lid_t + 2) difference() {
      translate([-tongue_w / 2 - cut, -tongue_w / 2 - cut]) square([tongue_w + 2 * cut, tongue_l + cut]);
      translate([-tongue_w / 2, -tongue_w / 2]) square([tongue_w, tongue_l + 1]);
    }
    // light tube bore
    translate([status_led[0], status_led[1], -comp_h]) cylinder(d = 2.2, h = comp_h + lid_t + 1);
    // engraved labels
    engrave = 0.6;
    translate([0, 0, lid_t - engrave]) linear_extrude(engrave + 1) {
      for (p = term_pins) translate([8.6, p[1]])
        text(p[1] == 33.5 || p[1] == 16.0 ? "+" : "-", size = 3, valign = "center", font = "Liberation Sans:style=Bold");
      translate([-1, 37.8]) text("12-24V IN", size = 2.6, font = "Liberation Sans:style=Bold");
      translate([-1, 20.5]) text("LED", size = 2.6, font = "Liberation Sans:style=Bold");
      for (b = buttons) translate([b[0] + 4.3, b[1] + tongue_l - 5]) text(b[2], size = 2.6, font = "Liberation Sans:style=Bold");
      translate([status_led[0], status_led[1] + 2.6]) text("WiFi", size = 2.2, halign = "center", font = "Liberation Sans:style=Bold");
      translate([40, 30]) bilginier_logo(12);
      translate([40, 19.6]) text("LED Controller", size = 3.6, halign = "center", font = "Liberation Sans:style=Bold");
      translate([40, 15.9]) text("BILGINIER", size = 2.3, spacing = 1.35, halign = "center", font = "Liberation Sans:style=Bold");
    }
  }
}

// ---------------------------------------------------------------- output
module pcb_dummy() {
  color("darkgreen") translate([0, 0, pcb_z]) cube([pcb_w, pcb_h, pcb_t]);
  color("silver") translate([49.8, 9, top_z]) cube([20.1, 18, 3.2]);           // ESP module
  color("green") for (s = term_spans) translate([0.4, s[0], top_z]) cube([9.8, s[1] - s[0], 10]);
  color("gray") translate([25.4, -0.4, top_z]) cube([9.2, 7.4, 3.2]);          // USB-C
}

if (part == "base") base();
else if (part == "lid") translate([0, 0, lid_t]) mirror([0, 0, 1]) lid();   // print face-down
else {
  color("#e8e6e0") base();
  pcb_dummy();
  color("#f0a040", 0.85) translate([0, 0, base_h + 8]) lid();
}
