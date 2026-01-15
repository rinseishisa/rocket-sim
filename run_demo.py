import numpy as np
import matplotlib.pyplot as plt

from src.vehicle import Stage, Rocket
from src.simulate import SimConfig, simulate_2d

def main():
    # --- example parameters (not real vehicle) ---
    s1 = Stage(
        dry_mass=1200.0,
        prop_mass=4500.0,
        thrust=140000.0,
        isp=260.0,
        burn_time=75.0,
        cd=0.35,
        area=0.9
    )
    s2 = Stage(
        dry_mass=350.0,
        prop_mass=1500.0,
        thrust=45000.0,
        isp=310.0,
        burn_time=90.0,
        cd=0.25,
        area=0.5
    )
    rocket = Rocket(stage1=s1, stage2=s2, payload_mass=150.0)

    cfg = SimConfig(
        t_final=220.0,
        dt=0.05,
        guidance={"hold_time": 6.0, "turn_start_h": 1200.0, "turn_rate_deg_s": 0.9, "min_pitch_deg": 5.0}
    )

    t, X, extra = simulate_2d(rocket, cfg)
    x, y, vx, vy, m = X.T
    v = np.hypot(vx, vy)

    print("Final altitude [m]:", y[-1])
    print("Final speed [m/s]:", v[-1])
    print("Max dynamic pressure q [Pa]:", np.max(extra["q_dyn"]))

    # plots
    plt.figure()
    plt.plot(x/1000, y/1000)
    plt.xlabel("Downrange x [km]")
    plt.ylabel("Altitude y [km]")
    plt.title("Trajectory (2D)")

    plt.figure()
    plt.plot(t, y/1000)
    plt.xlabel("Time [s]")
    plt.ylabel("Altitude [km]")
    plt.title("Altitude vs Time")

    plt.figure()
    plt.plot(t, v)
    plt.xlabel("Time [s]")
    plt.ylabel("Speed [m/s]")
    plt.title("Speed vs Time")

    plt.figure()
    plt.plot(t, extra["q_dyn"]/1000)
    plt.xlabel("Time [s]")
    plt.ylabel("Dynamic pressure q [kPa]")
    plt.title("Dynamic Pressure (Max-Q indicator)")

    plt.show()

if __name__ == "__main__":
    main()
