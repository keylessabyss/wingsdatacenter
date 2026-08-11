// Wing Data Center — Tabletop Open-Cooling Prototype
// Units: millimeters
// Build: aluminum base + plate fins (sheet or extrusion)
// Compare against a flat plate of the same footprint.

/* ===================== PARAMETERS ===================== */
base_l = 300;        // length along intended wind direction
base_w = 200;        // width
base_t = 6;          // base plate thickness

fin_count = 12;      // number of fins
fin_h = 50;          // fin height above base top
fin_t = 1.5;         // fin thickness
fin_tip_gap = 2;     // small clearance if using a top rail (optional)

// Heater pocket (underside) — for a 100x100 silicone heater pad
heater_size = 100;
heater_recess = 1.5;

// Mount holes (M4)
hole_d = 4.2;
hole_margin = 15;

/* ===================== DERIVED ===================== */
fin_span = base_w - 20;                 // fins inset 10 mm from each side
channel_pitch = fin_span / (fin_count - 1);
fin_start_y = (base_w - fin_span) / 2;

echo("Footprint mm:", base_l, "x", base_w);
echo("Fin pitch (center-center) mm:", channel_pitch);
echo("Approx exposed fin area m2:",
     (fin_count * 2 * (base_l/1000) * (fin_h/1000)) +
     ((base_l/1000)*(base_w/1000)));

module base_plate() {
    difference() {
        cube([base_l, base_w, base_t], center = false);

        // heater recess on underside (z=0 is bottom)
        translate([
            (base_l - heater_size) / 2,
            (base_w - heater_size) / 2,
            0
        ])
            cube([heater_size, heater_size, heater_recess], center = false);

        // corner mount holes
        for (x = [hole_margin, base_l - hole_margin])
            for (y = [hole_margin, base_w - hole_margin])
                translate([x, y, -1])
                    cylinder(h = base_t + 2, d = hole_d, $fn = 32);
    }
}

module fin(i) {
    y = fin_start_y + i * channel_pitch - fin_t / 2;
    translate([0, y, base_t])
        cube([base_l, fin_t, fin_h], center = false);
}

module wing_assembly() {
    color("Silver") base_plate();
    color("Gainsboro")
        for (i = [0 : fin_count - 1])
            fin(i);
}

module flat_baseline() {
    // Same footprint, no fins — for A/B thermal test
    color("Gray") base_plate();
}

// Default: show the wing module
wing_assembly();

// Uncomment to export/view flat baseline instead:
// flat_baseline();
