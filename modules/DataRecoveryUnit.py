from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class DataRecoveryUnit(SubCircuitFactory):
    NAME = 'DataRecoveryUnit'
    NODES = ('DataIn', 'VCO_Clk', 'RecoveredData', 'VDD', 'VSS')
    
    def __init__(self, nmos_width=0.5e-6, pmos_width=1e-6, channel_length=0.18e-6, load_capacitance=10e-15):
        super().__init__()
        # Define MOSFET models (level 1)
        self.model('nmos_model', 'nmos', level=1, kp=100e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=40e-6, vto=-0.5)
        
        # Master stage transmission gate (clock high)
        self.MOSFET('M1', 'node1', 'VCO_Clk', 'DataIn', 'VSS', model='nmos_model', w=nmos_width, l=channel_length)
        self.MOSFET('M2', 'node1', 'VCO_Clk', 'DataIn', 'VDD', model='pmos_model', w=pmos_width, l=channel_length)
        
        # Master stage inverter
        self.MOSFET('M3', 'node2', 'node1', 'VDD', 'VDD', model='pmos_model', w=pmos_width, l=channel_length)
        self.MOSFET('M4', 'node2', 'node1', 'VSS', 'VSS', model='nmos_model', w=nmos_width, l=channel_length)
        
        # Slave stage transmission gate (clock low)
        self.MOSFET('M5', 'RecoveredData', 'node2', 'node3', 'VSS', model='nmos_model', w=nmos_width, l=channel_length)
        self.MOSFET('M6', 'RecoveredData', 'node2', 'node3', 'VDD', model='pmos_model', w=pmos_width, l=channel_length)
        
        # Slave stage inverter
        self.MOSFET('M7', 'node3', 'node2', 'VDD', 'VDD', model='pmos_model', w=pmos_width, l=channel_length)
        self.MOSFET('M8', 'node3', 'node2', 'VSS', 'VSS', model='nmos_model', w=nmos_width, l=channel_length)
        
        # Output load capacitance (optional)
        if load_capacitance > 0:
            self.C('C1', 'RecoveredData', 'VSS', load_capacitance)