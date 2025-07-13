from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class VoltageControlledOscillator(SubCircuitFactory):
    NAME = 'VoltageControlledOscillator'
    NODES = ('Vctrl', 'Vctrl_Init', 'VCO_Clk', 'VDD', 'VSS')
    
    def __init__(self, 
                 inverter_width_n=0.5e-6, 
                 inverter_width_p=1e-6,
                 control_width_n=1e-6,
                 control_width_p=2e-6,
                 channel_length=0.18e-6,
                 load_capacitance=10e-15):
        
        super().__init__()
        
        # Define MOSFET models (level 1)
        self.model('nmos_model', 'nmos', level=1, kp=100e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=40e-6, vto=-0.5)
        
        # Control transistors (current starving)
        self.MOSFET('Mp_ctrl', 'VDD', 'Vctrl', 'VDD', 'VDD', 
                   model='pmos_model', w=control_width_p, l=channel_length)
        self.MOSFET('Mn_ctrl', 'VSS', 'Vctrl', 'VSS', 'VSS',
                   model='nmos_model', w=control_width_n, l=channel_length)
        
        # Initial control transistors (startup)
        self.MOSFET('Mp_init', 'VDD', 'Vctrl_Init', 'VDD', 'VDD',
                   model='pmos_model', w=control_width_p, l=channel_length)
        self.MOSFET('Mn_init', 'VSS', 'Vctrl_Init', 'VSS', 'VSS',
                   model='nmos_model', w=control_width_n, l=channel_length)
        
        # Ring oscillator with 3 stages
        # Stage 1
        self.MOSFET('Mp1', 'net1', 'VCO_Clk', 'Mp_ctrl', 'Mp_ctrl',
                   model='pmos_model', w=inverter_width_p, l=channel_length)
        self.MOSFET('Mn1', 'net1', 'VCO_Clk', 'Mn_ctrl', 'Mn_ctrl',
                   model='nmos_model', w=inverter_width_n, l=channel_length)
        
        # Stage 2
        self.MOSFET('Mp2', 'net2', 'net1', 'Mp_ctrl', 'Mp_ctrl',
                   model='pmos_model', w=inverter_width_p, l=channel_length)
        self.MOSFET('Mn2', 'net2', 'net1', 'Mn_ctrl', 'Mn_ctrl',
                   model='nmos_model', w=inverter_width_n, l=channel_length)
        
        # Stage 3 (output stage)
        self.MOSFET('Mp3', 'VCO_Clk', 'net2', 'Mp_ctrl', 'Mp_ctrl',
                   model='pmos_model', w=inverter_width_p, l=channel_length)
        self.MOSFET('Mn3', 'VCO_Clk', 'net2', 'Mn_ctrl', 'Mn_ctrl',
                   model='nmos_model', w=inverter_width_n, l=channel_length)
        
        # Load capacitance
        if load_capacitance > 0:
            self.C('C1', 'VCO_Clk', 'VSS', load_capacitance)