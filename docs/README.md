# Wing Data Center

**An open concept for passively-cooled, wind-integrated data center architecture.**

Author: Jose F Salinas ([Keyless Abyss](https://keylessabyss.github.io/))
License: MIT (see [LICENSE](./LICENSE)) — free to use, modify, build on, or ignore.

---

## The idea, in one sentence

Instead of hiding a data center's cooling system behind a plain warehouse
facade, make the **building envelope itself** the heat exchanger — shaped
like giant curved fins (think: a skyscraper-sized CPU heatsink), oriented to
work with prevailing wind, with small turbines placed in select channels to
recover a bit of that wind as electricity.

```
WIND →→→

    ╭│╮ ╭│╮ ╭│╮ ╭│╮
    │││ │││ │││ │││
    │││ │││ │││ │││   ← exterior fins/wings, exposed as architecture
    │││ │││ │││ │││
   ┌─────────────────┐
   │   DATA CENTER    │
   │   GPU   GPU      │
   │   GPU   GPU      │
   └─────────────────┘
          ↑
      liquid loops carry heat from racks to the exterior fins
```

## Why this might matter

Modern hyperscale data centers reject enormous amounts of heat, and a lot of
that cooling relies on evaporating significant volumes of water (cooling
towers) or on energy-hungry mechanical chillers. Water use in particular is
becoming a real constraint in drought-prone regions where data centers are
increasingly being sited.

This concept trades some of that water dependency for **more surface area
and smarter airflow design** — closer to how a CPU tower cooler or a
motorcycle engine's finned cylinder works, just built at architectural
scale. It won't power the racks themselves (the numbers below show that
clearly), but it could meaningfully cut water use and offset auxiliary loads
like cooling fans and pumps.

## What's actually in this repo

This is an **early-stage concept with a first-pass math sanity-check**, not
a validated engineering design. Please read that sentence twice before
citing this anywhere. Specifically:

| Component | Status |
|---|---|
| Core concept (finned building envelope + wind-assisted cooling) | Conceptual, grounded in established heat-transfer principles (extended surface / fin theory, forced convection) |
| `thermal-model/model.py` | A Python script using textbook heat-transfer correlations (flat-plate Nusselt number correlations) to estimate order-of-magnitude heat rejection, turbine power potential, and a "crossover" wind speed above which turbine drag stops being a net cooling cost. **Not CFD. Several constants are estimated placeholders**, clearly marked in the code. |
| CFD validation (`cfd/`) | Not yet done. This is the critical next step — see "What this needs next" below. |
| Physical prototype | Not built. A simple tabletop comparison (flat enclosure vs. finned enclosure, same heat source, same wind) would be the logical first physical test. |
| Architectural/structural feasibility | Not evaluated at all. No input yet from anyone with actual building engineering or hyperscale data center design experience. |

### What the model currently suggests (take with real skepticism)

- A finned "wing" exterior with roughly 3x the surface area of an equivalent
  flat wall could reject on the order of 140% more heat at the same wind
  speed and temperature difference — this effect holds even in still air,
  since it's driven by surface area, not wind.
- Wind-harvested electricity from small integrated turbines is small relative
  to a data center's total power draw — plausible for offsetting fans/pumps,
  not for powering compute.
- Because turbine drag reduces the airflow reaching the cooling fins, there
  appears to be a **minimum wind speed (roughly 5–7.5 m/s in the current
  model, depending on turbine design) below which a turbine does more harm
  to cooling than it recovers in electricity.** This means site selection —
  not just fin design — may be the deciding factor in whether the turbine
  portion of this idea is worth including at all.

Run `python thermal-model/model.py` to see the full sweep and reasoning.

## What this needs next

Roughly in order of usefulness:

1. **Real CFD** (SimScale, OpenFOAM, Ansys Fluent) on an actual fin geometry
   to replace the placeholder drag/loss coefficients with measured numbers.
2. **A tabletop physical prototype** — flat vs. finned enclosure, same heat
   source, same fan/wind conditions — to sanity-check the model against
   reality at small scale.
3. **Review from people who actually do this for a living**: data-center
   thermal/mechanical engineers, HVAC engineers, or an architecture firm
   that designs hyperscale facilities.
4. **Site wind-data analysis** — the turbine crossover finding above means
   this concept's viability depends heavily on local average wind speed,
   which hasn't been checked against any real candidate location yet.

## Why this is public and MIT-licensed

This isn't being pursued for profit or exclusive credit. If any part of this
concept is useful — the framing, the math, the visual language — it's meant
to be picked up, corrected, improved, and built on by whoever can actually
take it further. If you're a thermal engineer, an architect, a grad student
looking for a CFD project, or just someone who wants to run the numbers
better than this repo currently does: please do, and feel free to open an
issue or a PR.

## Repo structure

```
WingsDataCenter/
├── thermal-model/     # Python heat-transfer / crossover sanity-check model
├── cfd/                # (empty for now) real CFD studies go here
├── UE4-viz/             # UE4.27 HTML5-branch visualization/prototype
├── notes/               # design notes, sketches, writeups
├── LICENSE              # MIT
└── README.md            # this file
```

## Disclaimer

Nothing in this repo has been reviewed by a licensed engineer. The math is a
first-pass sanity check meant to decide whether the idea is worth pursuing
further, not a design you should build from. If you're evaluating this
professionally, please treat every number here as "probably the right order
of magnitude, definitely not the right precision."