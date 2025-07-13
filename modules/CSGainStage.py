from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class CSGainStage(SubCircuitFactory):
    NAME = 'CSGainStage'
    NODES = ('Vin', 'Vbias', 'Vout', 'VDD', 'GND')
    
    def __init__(self, cs_nmos_width, cs_pmos_width, channel_length):
        super().__init__()
        
        # 添加MOSFET模型定义
        self.model('nmos_model', 'nmos', level=1, kp=200e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=100e-6, vto=-0.5)
        
        # 共源放大级
        self.M('1', 'Vout', 'Vin', 'GND', 'GND', model='nmos_model', 
               l=channel_length, w=cs_nmos_width)
        
        # 有源负载
        self.M('2', 'Vout', 'Vbias', 'VDD', 'VDD', model='pmos_model', 
               l=channel_length, w=cs_pmos_width)
        