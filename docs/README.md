Wing Data Center

An open concept for building-integrated, low-water data center cooling using architectural heat-exchanger wings, natural airflow, and closed-loop thermal transport.

Author: Jose F. Salinas (Keyless Abyss)
License: MIT (see LICENSE) — free to use, modify, build on, or ignore.

The idea, in one sentence

Instead of hiding a data center's cooling system behind a plain warehouse facade, make the building envelope itself part of the heat-rejection system — shaped like giant curved fins (think: a building-sized CPU heatsink), designed to work with prevailing wind and natural convection, with fans available for assisted airflow and optional turbines in select channels where wind conditions justify them.

WIND →→→

    ╭│╮ ╭│╮ ╭│╮ ╭│╮
    │││ │││ │││ │││
    │││ │││ │││ │││   ← exterior heat-exchanger wings
    │││ │││ │││ │││
   ┌─────────────────┐
   │   DATA CENTER   │
   │   GPU   GPU     │
   │   GPU   GPU     │
   └─────────────────┘
          ↑
   closed thermal loop

The visual principle is simple:

The building looks like what it is doing.

If the facility is fundamentally a giant computer producing enormous amounts of heat, its architecture can express the thermal system rather than hiding it.

Why this might matter

Modern hyperscale data centers reject enormous amounts of heat. Depending on facility design and climate, cooling can involve evaporative water consumption, mechanical chillers, cooling towers, pumps, fans, dry coolers, or combinations of these systems.

Water consumption is an especially important consideration in drought-prone regions.

Wing Data Center asks whether some of that dependency on active cooling and evaporative water consumption could be reduced through three architectural ideas:

Much greater exterior heat-exchange surface area
Building geometry designed around natural and prevailing airflow
A closed thermal transport system connecting compute equipment to the exterior wings

The concept is closer to a CPU tower cooler, heat pipe, radiator, or finned motorcycle cylinder scaled into architecture than to a conventional warehouse with cooling equipment added afterward.

It does not attempt to eliminate thermodynamics.

The heat still has to go somewhere.

The final heat sink is still the surrounding environment.

The question is whether the building itself can help move that heat there more efficiently and with less water.

Closed-loop cooling concept

An important extension of the original idea is to keep the server environment and thermal working fluid closed from the outside environment.

Outside air does not need to pass through the compute rooms.

Instead:

GPU / CPU
    ↓
cold plate / internal cooling system
    ↓
closed thermal transport loop
    ↓
exterior Wing heat exchanger
    ↓
outside air carries heat away

This keeps dust, humidity, salt, insects, pollution, and other outside contaminants away from the compute environment while allowing the exterior architecture to interact directly with ambient airflow.

Two-phase / condenser version

A future version worth investigating is a sealed two-phase loop.

Rather than only circulating liquid coolant, a working fluid could absorb heat near the compute equipment, undergo a phase change, transport that energy toward the exterior Wing structure, condense there, and return as liquid.

Conceptually:

COMPUTE
  GPU / CPU
     ↓
working fluid absorbs heat
     ↓
evaporation / phase change
     ↓
vapor transports thermal energy
     ↑
     │
════════════════════════════
   EXTERIOR WING CONDENSER
════════════════════════════
     │
     ↓
vapor condenses
     ↓
latent heat enters Wing structure
     ↓
large fin area transfers heat
     ↓
outside airflow
     ↓
ATMOSPHERE

condensed liquid
     ↓
returns through sealed loop
     ↓
COMPUTE

This is not a new physical principle. Heat pipes, vapor chambers, condensers, thermosiphons, and other two-phase thermal systems already use related mechanisms.

The research question is whether those established principles can be usefully incorporated into the building envelope itself at data-center scale.

No two-phase Wing system has been modeled or validated by this project yet.

Natural + assisted airflow

The goal is not necessarily to make the facility completely fanless.

A more practical target is:

Use architecture and natural airflow to reduce how often and how hard mechanical airflow systems need to operate.

The exterior Wings could form large air channels.

Good wind
    ↓
natural airflow through Wings
    ↓
reduced fan assistance

Weak wind
    ↓
fans assist airflow

Hot + weak wind
    ↓
greater mechanical assistance

Cool + windy
    ↓
maximum opportunity for passive heat rejection

Large, relatively slow-moving fans could potentially be integrated into selected channels rather than treating every exterior surface identically.

The optimal arrangement is unknown and requires CFD.

Optional wind-energy recovery

Small turbines could potentially be placed in selected Wing channels to recover some wind energy.

This remains a secondary feature, not the core cooling concept.

The turbines are not expected to power the compute racks.

At best, recovered energy might help offset auxiliary loads such as:

fans
pumps
controls
lighting
other facility systems

More importantly, turbines create drag.

Any energy recovered from the airflow must therefore be compared against the cooling performance lost by obstructing that airflow.

The current first-pass model suggests there may be a crossover wind speed below which installing a turbine is thermally counterproductive.

That means:

A Wing without turbines may be better than a Wing with turbines at many sites.

The cooling architecture should not depend on the turbine idea being successful.

What's actually in this repo

This is an early-stage concept with a first-pass mathematical sanity check, not a validated engineering design.

Please read that sentence twice before citing this project as evidence that the architecture works.

Component	Status
Building-integrated fin / Wing concept	Conceptual, based on established extended-surface heat-transfer principles
Natural and wind-assisted airflow	Conceptual; requires CFD
Closed-loop thermal transport	Conceptual system direction
Two-phase Wing condenser / thermosiphon concept	Proposed for future investigation; not yet modeled
Fan-assisted Wing channels	Proposed for future investigation
Optional wind turbines	Included in first-pass mathematical exploration
thermal-model/model.py	Python sanity-check using simplified textbook heat-transfer correlations and estimated coefficients. Not CFD.
CFD validation (cfd/)	Not yet completed
Physical prototype	Not yet built
Architectural / structural feasibility	Not evaluated
Professional thermal/HVAC review	Not completed
What the current model suggests

Treat these results with substantial skepticism until CFD and physical testing exist.

The current simplified model suggests:

Increasing effective heat-exchange area through a finned exterior can substantially increase modeled heat rejection under equivalent assumed conditions.
The current Wing geometry uses roughly 3× the effective surface area of the comparison flat wall and produces roughly 140% greater modeled heat rejection under the model's assumptions.
Wind-harvested electricity is small compared with total data-center power consumption.
Turbine energy might be useful for auxiliary loads rather than compute.
Turbine drag can reduce airflow available for cooling.
The current model estimates a turbine crossover region around 5–7.5 m/s, depending on assumed turbine characteristics.
Below that region, the modeled cooling penalty from turbine obstruction may exceed the value of the recovered electricity.

These are order-of-magnitude exploration results, not engineering predictions.

Run:

python thermal-model/model.py

to see the current sweep and assumptions.

What this needs next

Roughly in order of usefulness:

Learn and reproduce a known CFD case
Complete a conventional heatsink / conjugate heat-transfer tutorial first.
Verify that the workflow produces sensible results before testing Wing geometry.
Single-Wing CFD
Flat control surface vs. one Wing geometry
Same heat input
Same ambient temperature
Same boundary conditions
Same wind velocity
Wind-speed sweep
Still / natural convection case where practical
Low wind
Moderate wind
High wind
Wing geometry optimization
Fin spacing
Curvature
Height
Thickness
Channel width
Wind direction sensitivity
Fan-assisted airflow study
Determine whether Wing channels can reduce required fan power compared with conventional heat-rejection geometry.
Two-phase thermal study
Investigate whether a sealed condenser / thermosiphon architecture is appropriate for transporting heat into the Wing structure.
Turbine CFD
Only after the basic cooling geometry is understood.
Measure the actual cooling penalty caused by airflow obstruction.
Tabletop physical prototype
Flat enclosure vs. finned enclosure
Same heat source
Same ambient conditions
Same airflow
Measure temperature and power consumption.
Professional review
Data-center thermal engineers
Mechanical/HVAC engineers
Structural engineers
Architects experienced with hyperscale facilities
Real-site analysis
Temperature
Humidity
prevailing wind direction
wind-speed distribution
dust
salt/corrosion exposure
seasonal extremes
water availability
The smallest useful experiment

The project intentionally follows a simple rule:

Prove the smallest mechanism before scaling the idea.

The first meaningful CFD comparison does not require an entire data center.

CONTROL                    WING

WIND →                     WIND →

┌────────────┐             ├────╮
│            │             ├────╮
│  HOT WALL  │             ├────╮
│            │             ├────╮
└────────────┘             └────────

Same heat input.
Same material.
Same ambient temperature.
Same wind.

Measure:

maximum surface temperature
average surface temperature
total heat flux
air velocity
pressure drop
temperature field
flow separation / recirculation
heat rejection

If the Wing cannot demonstrate a useful advantage under controlled conditions, there is no reason to simulate a skyscraper.

Why this is public and MIT-licensed

This isn't being pursued for profit or exclusive credit.

If any part of the concept is useful — the framing, math, architecture, CFD work, visual language, or even a failed experiment that tells someone what not to build — it is meant to be picked up, corrected, improved, and built upon.

If you're a thermal engineer, architect, HVAC engineer, data-center engineer, researcher, student looking for a CFD project, or simply someone capable of running the numbers better than this repository currently does:

Please do.

Issues, corrections, simulations, failed tests, and pull requests are welcome.

A result showing that part of the concept does not work is still a useful result.

Repo structure
WingsDataCenter/
├── thermal-model/      # Python heat-transfer / crossover sanity-check model
├── cfd/                # CFD studies and results
├── UE4-viz/            # UE4.27 HTML5-branch visualization/prototype
├── notes/              # design notes, sketches, writeups
├── LICENSE              # MIT
└── README.md            # this file
Disclaimer

Nothing in this repository has been reviewed or approved by a licensed engineer.

The current mathematics are a first-pass sanity check intended to determine whether parts of the idea are worth investigating further — not a design from which anyone should construct a facility or cooling system.

Any CFD results added later should likewise be treated as experimental modeling unless independently reviewed and validated against appropriate physical data.

If you're evaluating this concept professionally, assume every current number is:

Probably useful for asking the next question. Not precise enough to build from.