from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]  # rocket-sim/
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.vehicle import Stage, Rocket
from src.simulate import SimConfig, simulate_2d

st.title("2-Stage Rocket Trajectory Simulator (MVP)")

with st.sidebar:
    st.header("Stage 1")
    s1_thrust = st.number_input("Thrust [N]", value=140000.0)
    s1_isp = st.number_input("Isp [s]", value=260.0)
    s1_burn = st.number_input("Burn time [s]", value=75.0)
    s1_dry = st.number_input("Dry mass [kg]", value=1200.0)
    s1_prop = st.number_input("Prop mass [kg]", value=4500.0)
    s1_cd = st.number_input("Cd", value=0.35)
    s1_area = st.number_input("Area [m^2]", value=0.9)

    st.header("Stage 2")
    s2_thrust = st.number_input("Thrust [N] (S2)", value=45000.0)
    s2_isp = st.number_input("Isp [s] (S2)", value=310.0)
    s2_burn = st.number_input("Burn time [s] (S2)", value=90.0)
    s2_dry = st.number_input("Dry mass [kg] (S2)", value=350.0)
    s2_prop = st.number_input("Prop mass [kg] (S2)", value=1500.0)
    s2_cd = st.number_input("Cd (S2)", value=0.25)
    s2_area = st.number_input("Area [m^2] (S2)", value=0.5)

    payload = st.number_input("Payload mass [kg]", value=150.0)

    st.header("Guidance")
    hold_time = st.number_input("Hold vertical [s]", value=6.0)
    turn_start_h = st.number_input("Turn start altitude [m]", value=1200.0)
    turn_rate = st.number_input("Turn rate [deg/s]", value=0.9)
    min_pitch = st.number_input("Min pitch [deg]", value=5.0)

    st.header("Sim")
    t_final = st.number_input("t_final [s]", value=220.0)
    dt = st.number_input("dt [s]", value=0.05)

run = st.button("Run Simulation")

if run:
    s1 = Stage(s1_dry, s1_prop, s1_thrust, s1_isp, s1_burn, s1_cd, s1_area)
    s2 = Stage(s2_dry, s2_prop, s2_thrust, s2_isp, s2_burn, s2_cd, s2_area)
    rocket = Rocket(s1, s2, payload)

    cfg = SimConfig(
        t_final=float(t_final),
        dt=float(dt),
        guidance={
            "hold_time": float(hold_time),
            "turn_start_h": float(turn_start_h),
            "turn_rate_deg_s": float(turn_rate),
            "min_pitch_deg": float(min_pitch),
        }
    )

    t, X, extra = simulate_2d(rocket, cfg)
    x, y, vx, vy, m = X.T
    v = np.hypot(vx, vy)

    st.metric("Final altitude [km]", f"{y[-1]/1000:.2f}")
    st.metric("Final speed [m/s]", f"{v[-1]:.1f}")
    st.metric("Max-Q [kPa]", f"{np.max(extra['q_dyn'])/1000:.1f}")

    fig1 = plt.figure()
    plt.plot(x/1000, y/1000)
    plt.xlabel("Downrange x [km]")
    plt.ylabel("Altitude y [km]")
    plt.title("Trajectory")
    st.pyplot(fig1)

    fig2 = plt.figure()
    plt.plot(t, y/1000)
    plt.xlabel("Time [s]")
    plt.ylabel("Altitude [km]")
    plt.title("Altitude vs Time")
    st.pyplot(fig2)

    fig3 = plt.figure()
    plt.plot(t, extra["q_dyn"]/1000)
    plt.xlabel("Time [s]")
    plt.ylabel("Dynamic pressure q [kPa]")
    plt.title("Dynamic Pressure (Max-Q)")
    st.pyplot(fig3)