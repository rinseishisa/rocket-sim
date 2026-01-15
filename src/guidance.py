def pitch_program(t: float, h: float, params: dict) -> float:
    """
    Simple gravity-turn-ish pitch schedule (2D).
    pitch = angle from +x axis (horizontal). 90deg means straight up.

    params:
      - hold_time: time to keep vertical [s]
      - turn_start_h: start turning above this altitude [m]
      - turn_rate_deg_s: pitch decrease rate after turn starts [deg/s]
      - min_pitch_deg: do not go below this [deg]
    """
    hold_time = params.get("hold_time", 5.0)
    turn_start_h = params.get("turn_start_h", 500.0)
    turn_rate = params.get("turn_rate_deg_s", 0.7)
    min_pitch = params.get("min_pitch_deg", 5.0)

    if t < hold_time or h < turn_start_h:
        return 90.0

    dt = t - hold_time
    pitch = 90.0 - turn_rate * dt
    if pitch < min_pitch:
        pitch = min_pitch
    return pitch
