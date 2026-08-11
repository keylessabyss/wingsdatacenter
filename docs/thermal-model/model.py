"""
Wing Data Center - Thermal Sanity-Check Model
------------------------------------------------
Purpose: quick order-of-magnitude comparison between a flat enclosure and a
"wing" (finned) enclosure for passive/wind-assisted heat rejection, plus a
rough estimate of how much power a building-integrated turbine could recover.

This is NOT a CFD replacement. It uses standard textbook heat-transfer
correlations (flat plate + extended surface / fin theory) to get numbers in
the right ballpark. Use it to decide whether a real CFD study (SimScale /
OpenFOAM) is worth running, and to size your tabletop prototype test.

Units: SI throughout (Watts, meters, Kelvin/Celsius, m/s) unless noted.
"""

import math
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Physical constants / air properties (approx, at ~25 C, sea level)
# ---------------------------------------------------------------------------
AIR_DENSITY = 1.184          # kg/m^3
AIR_KINEMATIC_VISCOSITY = 1.56e-5   # m^2/s
AIR_THERMAL_CONDUCTIVITY = 0.026    # W/(m*K)
AIR_PRANDTL = 0.707
AIR_SPECIFIC_HEAT = 1005     # J/(kg*K)


@dataclass
class Enclosure:
    name: str
    surface_area_m2: float          # total heat-rejecting surface area
    characteristic_length_m: float  # length in the flow direction (for Nu correlations)
    fin_efficiency: float = 1.0     # 1.0 = flat plate (no fins), <1.0 accounts for
                                     # fin conduction losses reducing effective area


@dataclass
class SimResult:
    name: str
    wind_speed_ms: float
    h_conv: float            # convective heat transfer coefficient, W/(m^2*K)
    max_heat_rejected_w: float
    reynolds: float
    flow_regime: str


def convective_coefficient(wind_speed_ms: float, characteristic_length_m: float) -> tuple:
    """
    Estimate the convective heat transfer coefficient for air flowing over a
    surface, using flat-plate forced-convection correlations.

    Returns (h, Reynolds number, flow regime string)
    """
    if wind_speed_ms <= 0.05:
        # Natural convection fallback (very rough vertical-plate correlation)
        # Nu ~ 1.42 * (dT/L)^0.25 -- but we don't have dT here, so use a
        # conservative fixed natural-convection h typical for still air.
        h = 5.0  # W/(m^2*K), typical still-air natural convection estimate
        return h, 0.0, "natural convection (still air)"

    reynolds = wind_speed_ms * characteristic_length_m / AIR_KINEMATIC_VISCOSITY

    if reynolds < 5e5:
        # Laminar flat plate, average Nusselt number
        nusselt = 0.664 * (reynolds ** 0.5) * (AIR_PRANDTL ** (1 / 3))
        regime = "laminar"
    else:
        # Turbulent flat plate (mixed boundary layer), average Nusselt number
        nusselt = (0.037 * (reynolds ** 0.8) - 871) * (AIR_PRANDTL ** (1 / 3))
        regime = "turbulent"

    h = nusselt * AIR_THERMAL_CONDUCTIVITY / characteristic_length_m
    return h, reynolds, regime


def max_heat_rejection(enclosure: Enclosure, wind_speed_ms: float, delta_t_c: float) -> SimResult:
    """
    Estimate the maximum convective heat rejection for a given enclosure,
    wind speed, and surface-to-ambient temperature difference.

    delta_t_c: surface temperature minus ambient air temperature (C or K, same scale)
    """
    h, reynolds, regime = convective_coefficient(wind_speed_ms, enclosure.characteristic_length_m)
    effective_area = enclosure.surface_area_m2 * enclosure.fin_efficiency
    q_watts = h * effective_area * delta_t_c

    return SimResult(
        name=enclosure.name,
        wind_speed_ms=wind_speed_ms,
        h_conv=h,
        max_heat_rejected_w=q_watts,
        reynolds=reynolds,
        flow_regime=regime,
    )


def turbine_power_potential(wind_speed_ms: float, swept_area_m2: float,
                             turbine_efficiency: float = 0.35) -> float:
    """
    Estimate electrical power recoverable from wind via small integrated
    turbines in the fin channels.

    Uses the standard wind power equation P = 0.5 * rho * A * v^3, scaled by
    an efficiency factor. Real small building-integrated turbines typically
    achieve well below the Betz limit (0.593) due to turbulence and scale --
    0.25-0.35 is a realistic "decent design" assumption, not a best case.
    """
    if wind_speed_ms <= 0:
        return 0.0
    theoretical_power = 0.5 * AIR_DENSITY * swept_area_m2 * (wind_speed_ms ** 3)
    return theoretical_power * turbine_efficiency


def pressure_drop_penalty_estimate(wind_speed_ms: float, loss_coefficient: float = 0.4) -> float:
    """
    Very rough estimate of dynamic pressure loss (Pa) introduced by placing
    turbines/obstructions in a channel. loss_coefficient (K) is a placeholder
    -- for real numbers this needs CFD or wind-tunnel testing.

    dP = K * 0.5 * rho * v^2
    """
    return loss_coefficient * 0.5 * AIR_DENSITY * (wind_speed_ms ** 2)


def compare_enclosures(wind_speed_ms: float, delta_t_c: float):
    """
    Run the flat-vs-wing comparison and print a readable summary.
    Adjust the geometry numbers below to match your actual prototype dimensions.
    """
    flat = Enclosure(
        name="Flat enclosure (baseline)",
        surface_area_m2=1.0,          # 1 m^2 flat panel, e.g. a prototype box face
        characteristic_length_m=1.0,
        fin_efficiency=1.0,
    )

    # "Wing" enclosure: same footprint, but fins roughly triple the effective
    # heat-rejecting surface area, at ~80% fin efficiency (typical for
    # aluminum extruded/cast fins of moderate length).
    wing = Enclosure(
        name='"Wing" finned enclosure',
        surface_area_m2=3.0,
        characteristic_length_m=1.0,
        fin_efficiency=0.80,
    )

    flat_result = max_heat_rejection(flat, wind_speed_ms, delta_t_c)
    wing_result = max_heat_rejection(wing, wind_speed_ms, delta_t_c)

    print("=" * 70)
    print(f"Wind speed: {wind_speed_ms} m/s | Surface-ambient dT: {delta_t_c} C")
    print("=" * 70)
    for r in (flat_result, wing_result):
        print(f"\n{r.name}")
        print(f"  Flow regime:            {r.flow_regime}")
        print(f"  Reynolds number:        {r.reynolds:,.0f}")
        print(f"  h (convective coeff):   {r.h_conv:.2f} W/(m^2*K)")
        print(f"  Max heat rejected:      {r.max_heat_rejected_w:.1f} W")

    improvement = (wing_result.max_heat_rejected_w / flat_result.max_heat_rejected_w - 1) * 100
    print(f"\n>> Wing enclosure rejects {improvement:.1f}% more heat than flat, "
          f"at this wind speed and dT.\n")

    # Turbine potential in a single fin channel (example: 0.3 m^2 swept area)
    turbine_swept_area = 0.3
    turbine_power = turbine_power_potential(wind_speed_ms, turbine_swept_area)
    dp = pressure_drop_penalty_estimate(wind_speed_ms)

    print(f"Turbine (per channel, {turbine_swept_area} m^2 swept area):")
    print(f"  Estimated recoverable power: {turbine_power:.2f} W")
    print(f"  Estimated pressure drop added: {dp:.2f} Pa "
          f"(this fights your cooling airflow -- lower is better)")
    print("=" * 70)


# ---------------------------------------------------------------------------
# Crossover analysis: turbine drag vs. net cooling benefit
# ---------------------------------------------------------------------------
# Key assumption (clearly flagged -- this is the part real CFD needs to
# replace): when a turbine sits in a wind-driven fin channel, the available
# driving dynamic pressure (0.5 * rho * v^2, from the ambient wind) gets
# split between (a) the turbine's flow resistance and (b) actually moving air
# across the fins. We model that as:
#
#     v_effective = v / sqrt(1 + K)
#
# where K is the turbine's loss coefficient. This says: at K=0 (no turbine),
# effective velocity = wind speed. As K grows, more of the driving pressure
# is "spent" on the turbine and less on airflow, so effective velocity at
# the fin surface drops. This is a simplification of a real duct-flow energy
# balance, not a CFD result -- treat it as a first-pass sanity check only.

FAN_COP = 3.0
# "Coefficient of performance" placeholder: assumed watts of heat rejection
# restored per watt of electrical fan power spent compensating for lost
# airflow. Real value depends on fan/motor efficiency and duct design --
# 3.0 is a reasonable placeholder for a decent axial fan, not a measured number.


def effective_velocity_with_turbine(wind_speed_ms: float, loss_coefficient: float) -> float:
    """Wind velocity actually reaching the fin surface once turbine drag
    is accounted for (see assumption above)."""
    return wind_speed_ms / math.sqrt(1 + loss_coefficient)


def net_turbine_benefit(wind_speed_ms: float, enclosure: Enclosure, delta_t_c: float,
                         turbine_swept_area_m2: float, loss_coefficient: float,
                         turbine_efficiency: float = 0.35, fan_cop: float = FAN_COP) -> dict:
    """
    For a given wind speed, compute:
      - heat rejected with no turbine present (full wind speed at the fins)
      - heat rejected with turbine present (reduced effective velocity)
      - thermal penalty (W) = cooling capacity lost to turbine drag
      - equivalent fan power (W) needed to make up that lost cooling
      - turbine harvested power (W)
      - net benefit (W) = turbine harvested power - equivalent fan power cost

    net_benefit > 0  => turbine is a net win at this wind speed
    net_benefit < 0  => turbine's drag penalty costs more (in fan power terms)
                        than the turbine recovers
    """
    q_no_turbine = max_heat_rejection(enclosure, wind_speed_ms, delta_t_c).max_heat_rejected_w

    v_eff = effective_velocity_with_turbine(wind_speed_ms, loss_coefficient)
    q_with_turbine = max_heat_rejection(enclosure, v_eff, delta_t_c).max_heat_rejected_w

    thermal_penalty_w = max(0.0, q_no_turbine - q_with_turbine)
    fan_power_to_compensate_w = thermal_penalty_w / fan_cop

    turbine_power_w = turbine_power_potential(wind_speed_ms, turbine_swept_area_m2, turbine_efficiency)

    net_benefit_w = turbine_power_w - fan_power_to_compensate_w

    return {
        "wind_speed_ms": wind_speed_ms,
        "q_no_turbine_w": q_no_turbine,
        "q_with_turbine_w": q_with_turbine,
        "thermal_penalty_w": thermal_penalty_w,
        "fan_power_to_compensate_w": fan_power_to_compensate_w,
        "turbine_power_w": turbine_power_w,
        "net_benefit_w": net_benefit_w,
    }


def find_crossover_points(wind_range_ms, enclosure: Enclosure, delta_t_c: float,
                           turbine_swept_area_m2: float, loss_coefficient: float) -> list:
    """
    Scan a wind-speed range and find where net_benefit_w changes sign.
    Returns a list of (v_low, v_high) brackets where the crossover happens,
    refined once via linear interpolation for a cleaner estimate.
    """
    results = [net_turbine_benefit(v, enclosure, delta_t_c, turbine_swept_area_m2, loss_coefficient)
               for v in wind_range_ms]

    crossovers = []
    for i in range(1, len(results)):
        prev_v, prev_net = results[i - 1]["wind_speed_ms"], results[i - 1]["net_benefit_w"]
        curr_v, curr_net = results[i]["wind_speed_ms"], results[i]["net_benefit_w"]
        if prev_net == 0:
            crossovers.append(prev_v)
        elif prev_net < 0 < curr_net or prev_net > 0 > curr_net:
            # linear interpolation between the two sample points
            frac = -prev_net / (curr_net - prev_net)
            v_cross = prev_v + frac * (curr_v - prev_v)
            crossovers.append(round(v_cross, 3))

    return crossovers


def sweep_and_report_crossover(delta_t_c: float, turbine_swept_area_m2: float, loss_coefficient: float,
                                v_min: float = 0.2, v_max: float = 20.0, step: float = 0.2):
    wing = Enclosure(
        name='"Wing" finned enclosure',
        surface_area_m2=3.0,
        characteristic_length_m=1.0,
        fin_efficiency=0.80,
    )

    wind_range = [round(v_min + i * step, 3) for i in range(int((v_max - v_min) / step) + 1)]

    print("=" * 78)
    print(f"CROSSOVER SWEEP  |  loss_coefficient K={loss_coefficient}  |  "
          f"turbine swept area={turbine_swept_area_m2} m^2  |  dT={delta_t_c} C")
    print("=" * 78)
    print(f"{'v (m/s)':>8} | {'Q lost to drag (W)':>19} | {'Fan cost (W)':>13} | "
          f"{'Turbine out (W)':>16} | {'Net (W)':>9}")
    print("-" * 78)

    sample_points = [v for v in wind_range if abs(v % 1.0) < 1e-6 or v in (v_min, v_max)]
    for v in sample_points:
        r = net_turbine_benefit(v, wing, delta_t_c, turbine_swept_area_m2, loss_coefficient)
        print(f"{v:8.1f} | {r['thermal_penalty_w']:19.2f} | {r['fan_power_to_compensate_w']:13.2f} | "
              f"{r['turbine_power_w']:16.2f} | {r['net_benefit_w']:9.2f}")

    crossovers = find_crossover_points(wind_range, wing, delta_t_c, turbine_swept_area_m2, loss_coefficient)

    print("-" * 78)
    if crossovers:
        for v_cross in crossovers:
            print(f">> Net benefit crosses zero at ~{v_cross} m/s")
        below = crossovers[0]
        print(f"\n>> Below ~{below} m/s: turbine drag costs more (in equivalent fan power)")
        print(f"   than the turbine harvests -- net loss.")
        print(f">> Above ~{below} m/s: turbine harvest outpaces its drag penalty -- net gain.")
    else:
        print(">> No sign change found in this range -- net benefit stayed the same sign")
        print("   across the whole swept range. Try widening v_min/v_max or changing K.")
    print("=" * 78 + "\n")


if __name__ == "__main__":
    # --- Example run: tweak these to match a real prototype / site conditions ---
    WIND_SPEED_MS = 4.0       # ~9 mph, a modest steady breeze
    SURFACE_DELTA_T_C = 15.0  # surface 15C above ambient air

    compare_enclosures(WIND_SPEED_MS, SURFACE_DELTA_T_C)

    print("\nTry different wind speeds to see how much the wing design")
    print("depends on having consistent wind vs. being becalmed:\n")
    for v in (0.0, 1.0, 2.0, 4.0, 8.0):
        compare_enclosures(v, SURFACE_DELTA_T_C)

    print("\n\nNow the crossover analysis: at what wind speed does turbine")
    print("harvested power start outpacing the cooling it costs you via drag?\n")

    # A more aggressive turbine (higher K) will push the crossover to a
    # higher wind speed -- try K=0.4 (light obstruction) vs K=1.5 (aggressive
    # turbine blocking more of the channel) to see the effect.
    for K in (0.4, 0.8, 1.5):
        sweep_and_report_crossover(
            delta_t_c=SURFACE_DELTA_T_C,
            turbine_swept_area_m2=0.3,
            loss_coefficient=K,
        )