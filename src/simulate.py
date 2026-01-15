import numpy as np
from dataclasses import dataclass
from .vehicle import Rocket
from .dynamics import thrust_and_mdot, drag_force, gravity_accel, current_stage
from .atmosphere import rho_exponential
from .guidance import pitch_program

@dataclass
class SimConfig:
    t_final: float = 250.0
    dt: float = 0.05  # 20 Hz
    guidance: dict = None

def rk4_step(f, t, x, dt):
    k1 = f(t, x)
    k2 = f(t + dt/2, x + dt*k1/2)
    k3 = f(t + dt/2, x + dt*k2/2)
    k4 = f(t + dt, x + dt*k3)
    return x + dt*(k1 + 2*k2 + 2*k3 + k4)/6

def simulate_2d(rocket: Rocket, cfg: SimConfig):
    """
    State x = [x, y, vx, vy, m]
    x,y in meters. y>=0 is altitude.
    """
    if cfg.guidance is None:
        cfg.guidance = {"hold_time": 5.0, "turn_start_h": 800.0, "turn_rate_deg_s": 0.8, "min_pitch_deg": 5.0}

    n = int(cfg.t_final / cfg.dt) + 1
    t_hist = np.zeros(n)
    X = np.zeros((n, 5))
    extra = {
        "pitch_deg": np.zeros(n),
        "T": np.zeros(n),
        "q_dyn": np.zeros(n),
        "stage": np.zeros(n, dtype=int),
    }

    # initial: on ground, vertical
    X[0, :] = np.array([0.0, 0.0, 0.0, 0.0, rocket.initial_mass()])

    sep_done = False
    t_sep = rocket.stage1.burn_time

    def deriv(t, x):
        px, py, vx, vy, m = x
        py = max(py, 0.0)

        T, mdot, cd, area = thrust_and_mdot(t, rocket)
        pitch = pitch_program(t, py, cfg.guidance)
        pitch_rad = np.deg2rad(pitch)

        v = float(np.hypot(vx, vy))
        rho = rho_exponential(py)
        D = drag_force(rho, v, cd, area)

        # Drag direction opposite to velocity (avoid div0)
        if v < 1e-6:
            ax_drag, ay_drag = 0.0, 0.0
        else:
            ax_drag = -D * (vx / v) / m
            ay_drag = -D * (vy / v) / m

        # Thrust direction given by pitch
        ax_th = (T * np.cos(pitch_rad)) / m
        ay_th = (T * np.sin(pitch_rad)) / m

        g = gravity_accel(py)
        ax = ax_th + ax_drag
        ay = ay_th + ay_drag - g

        dm = -mdot if T > 0 else 0.0

        return np.array([vx, vy, ax, ay, dm], dtype=float)

    for i in range(1, n):
        t = i * cfg.dt
        t_hist[i] = t

        # integrate
        X[i, :] = rk4_step(deriv, t_hist[i-1], X[i-1, :], cfg.dt)

        # ground clamp
        if X[i, 1] < 0:
            X[i, 1] = 0
            if X[i, 3] < 0:
                X[i, 3] = 0

        # stage separation event: drop stage1 dry mass once at burnout
        if (not sep_done) and (t_hist[i-1] < t_sep <= t_hist[i]):
            X[i, 4] -= rocket.stage1.dry_mass
            sep_done = True

        # record extras
        px, py, vx, vy, m = X[i, :]
        pitch = pitch_program(t, py, cfg.guidance)
        T, _, cd, area = thrust_and_mdot(t, rocket)
        v = float(np.hypot(vx, vy))
        rho = rho_exponential(py)
        q_dyn = 0.5 * rho * v * v  # dynamic pressure

        extra["pitch_deg"][i] = pitch
        extra["T"][i] = T
        extra["q_dyn"][i] = q_dyn
        extra["stage"][i] = current_stage(t, rocket)

    return t_hist, X, extra
