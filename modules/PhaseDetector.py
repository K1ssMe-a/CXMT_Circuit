from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class PhaseDetector(SubCircuitFactory):
    NAME = 'PhaseDetector'
    NODES = ('DataIn', 'VCO_Clk', 'PhaseError', 'VDD', 'VSS')
  
    def __init__(self, nmos_width=0.5e-6, pmos_width=1e-6, channel_length=0.18e-6, filter_capacitance=10e-12):
        super().__init__()
        # Define MOSFET models (level 1)
        self.model('nmos_model', 'nmos', level=1, kp=100e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=40e-6, vto=-0.5)
    
        # Phase detector topology
        self.MOSFET('M1', 'PhaseError', 'DataIn', 'VDD', 'VDD', model='pmos_model', w=pmos_width, l=channel_length)
        self.MOSFET('M2', 'PhaseError', 'VCO_Clk', 'VDD', 'VDD', model='pmos_model', w=pmos_width, l=channel_length)
        self.MOSFET('M3', 'PhaseError', 'DataIn', 'VSS', 'VSS', model='nmos_model', w=nmos_width, l=channel_length)
        self.MOSFET('M4', 'PhaseError', 'VCO_Clk', 'VSS', 'VSS', model='nmos_model', w=nmos_width, l=channel_length)
    
        # Output filtering
        if filter_capacitance > 0:
            self.C('C1', 'PhaseError', 'VSS', filter_capacitance)