from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class Inverter01(SubCircuitFactory):
    NAME = 'Inverter01'
    NODES = ('Vin', 'Vout', 'GND', 'VDD')
    
    def __init__(self, nmos_width=0.5e-6, pmos_width=1e-6, channel_length=0.18e-6, load_capacitance=10e-15):
        super().__init__()
        # Define MOSFET models (level 1)
        self.model('nmos_model', 'nmos', level=1, kp=100e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=40e-6, vto=-0.5)
        
        # Topology
        self.MOSFET('M1', 'Vout', 'Vin', 'VDD', 'VDD', model='pmos_model', w=pmos_width, l=channel_length)
        self.MOSFET('M2', 'Vout', 'Vin', 'GND', 'GND', model='nmos_model', w=nmos_width, l=channel_length)
        
        # Load capacitance (optional)
        if load_capacitance > 0:
            self.C('C1', 'Vout', 'GND', load_capacitance)