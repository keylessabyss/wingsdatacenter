# Wing Data Center — Tabletop Open-Cooling Prototype

Buildable A/B test article: **flat plate** vs **plate-fin wing**, same footprint.

## Geometry (default)

| Parameter | Value |
|-----------|-------|
| Footprint | 300 mm (flow direction) × 200 mm |
| Base thickness | 6 mm aluminum |
| Fins | 12 × 1.5 mm thick × 50 mm tall |
| Fin pitch (c-c) | ~16.4 mm |
| Channel gap | ~14.9 mm |
| Heater pocket | 100 × 100 × 1.5 mm recess, underside center |
| Mount holes | M4, 15 mm from corners |

### Approximate areas

- Flat top face: 0.06 m²
- Wing: base top between fins + both sides of fins ≈ **0.36 m²** exposed metal to air  
  (about **6×** flat top area before fin efficiency — real effective area lower)

## Bill of materials

**Wing module**
- 1× aluminum plate 300 × 200 × 6 mm (6061 or 5052)
- 12× aluminum strip 300 × 50 × 1.5 mm (or cut from sheet)
- Optional: 2× end rails 200 × 10 × 6 mm to square the fin pack
- 4× M4 screws + standoffs for stand
- 1× 100×100 mm silicone heater pad (24 V / ~30–60 W class) + PID or bench supply
- Thermocouples or digital probes: base center, fin tip mid-chord, ambient

**Flat baseline**
- Same base plate only (no fins), same heater and sensors

**Stand / wind**
- Open frame so underside heater is insulated from table (foam or air gap)
- Box fan or tunnel for 2 / 4 / 8 m/s along the 300 mm axis
- Anemometer at inlet

## Build notes

1. **Fin attachment (pick one)**
   - Epoxy (Arctic Silver / thermal epoxy) into shallow milled slots (0.5–1 mm)
   - Press-fit into slots + epoxy fillet at root
   - Weld/braze if you have capability (best conduction)

2. **Root conduction matters more than fin count.** A bad joint kills the “wing” advantage.

3. **Orient fins parallel to wind** (channels along 300 mm length).

4. **Natural convection:** stand vertical with fins vertical for still-air test; or horizontal as “roof” module — pick one and keep A/B consistent.

5. **Insulation:** heater side faces down into insulating foam so heat is forced into the aluminum, not the table.

## Test matrix (matches Python model)

| Run | Config | Wind | Power | Record |
|-----|--------|------|-------|--------|
| 1 | Flat | 0 m/s | fixed W | T_base, T_amb |
| 2 | Wing | 0 m/s | same W | T_base, T_fin_tip, T_amb |
| 3–5 | Flat | 2 / 4 / 8 m/s | same W | same |
| 6–8 | Wing | 2 / 4 / 8 m/s | same W | same |

Compare ΔT = T_base − T_amb. Wing should show lower ΔT at same power.

## SimScale CAD tips

- Export STEP from CAD, or rebuild as solid base + fin solids (no zero-thickness faces)
- Air domain: box ~ 900 × 600 × 400 mm for forced flow; larger for natural convection
- Inlet velocity on upstream face; pressure outlet downstream
- Heat source: power on heater patch or volumetric on a thin solid under the base
- Material: Aluminum, Air
- Analysis: Conjugate Heat Transfer, steady

## Files

- `wing_module.scad` — parametric OpenSCAD (edit counts/sizes at top)
