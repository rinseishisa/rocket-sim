import numpy as np

def rho_exponential(h_m: float) -> float:
    """
    Very simple exponential atmosphere model.
    rho(h) = rho0 * exp(-h/H)
    """
    rho0 = 1.225  # kg/m^3 at sea level
    H = 8500.0    # m (scale height)
    h = max(0.0, h_m)
    return float(rho0 * np.exp(-h / H))