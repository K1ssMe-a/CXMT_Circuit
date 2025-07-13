from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class LoopFilter(SubCircuitFactory):
    NAME = 'LoopFilter'
    NODES = ('PhaseError', 'Vctrl', 'VDD', 'VSS')
  
    def __init__(self, r1=10e3, r2=100e3, c1=100e-12, c2=10e-12):
        super().__init__()
        # Passive components
        self.R('R1', 'PhaseError', 'Vctrl', r1)
        self.R('R2', 'Vctrl', 'VSS', r2)
        self.C('C1', 'PhaseError', 'Vctrl', c1)
        self.C('C2', 'Vctrl', 'VSS', c2)