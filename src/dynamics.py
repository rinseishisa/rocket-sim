import numpy as np
from .atmosphere import rho_exponential
from .vehicle import Rocket, G0

def gravity_accel(y_m: float) -> float:
    # constant g approximation (good enough for MVP)
    return G0

def drag_force(rho: float, v: float, cd: float, area: float) -> float:
    return 0.5 * rho * v * v * cd * area

def current_stage(t: float, rocket: Rocket) -> int:
    """
    returns 1 if stage1 burning or coasting before sep,
            2 if stage2 burning,
            0 if after stage2 burnout (coast)
    Stage separation assumed immediately after stage1 burnout.
    """
    if t <= rocket.stage1.burn_time:
        return 1
    elif t <= rocket.stage1.burn_time + rocket.stage2.burn_time:
        return 2
    else:
        return 0

def thrust_and_mdot(t: float, rocket: Rocket) -> tuple[float, float, float, float]:
    """
    Returns (T, mdot, cd, area) depending on which stage is active.
    """
    s = current_stage(t, rocket)
    if s == 1:
        return rocket.stage1.thrust, rocket.stage1.mdot, rocket.stage1.cd, rocket.stage1.area
    if s == 2:
        return rocket.stage2.thrust, rocket.stage2.mdot, rocket.stage2.cd, rocket.stage2.area
    return 0.0, 0.0, rocket.stage2.cd, rocket.stage2.area  # coast: use stage2 aero

def mass_after_separation(m: float, t: float, rocket: Rocket) -> float:
    """
    At stage1 burnout moment, drop stage1 dry mass.
    Implemented as: if t just passed burnout and we still carry stage1 dry, drop it.
    We'll handle in simulate loop with an event check (cleaner).
    """
    return m
