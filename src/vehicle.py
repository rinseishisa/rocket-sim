from dataclasses import dataclass

G0 = 9.80665

@dataclass
class Stage:
    dry_mass: float     # kg
    prop_mass: float    # kg
    thrust: float       # N(constant)
    isp: float          # s 
    burn_time: float    # s
    cd: float           # -
    area: float         # m^2

    @property
    def mdot(self) -> float:
        # mass flow rate (kg/s)
        return self.thrust / (self.isp * G0)
    
@dataclass
class Rocket:
    stage1: Stage
    stage2: Stage
    payload_mass: float  # kg

    def initial_mass(self) -> float:
        return (self.payload_mass
                + self.stage1.dry_mass + self.stage1.prop_mass
                + self.stage2.dry_mass + self.stage2.prop_mass)