from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class DiffInputStage(SubCircuitFactory):
    NAME = 'DiffInputStage'
    NODES = ('Vinp', 'Vinn', 'Vbias1', 'Vbias2', 'Vout', 'VDD', 'GND')
    
    def __init__(self, diff_nmos_width, diff_pmos_width, channel_length):
        super().__init__()
        
        # 添加MOSFET模型定义
        self.model('nmos_model', 'nmos', level=1, kp=200e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=100e-6, vto=-0.5)
        
        # 差分对
        self.M('1', 'Vout_int', 'Vinp', 'Vbias1', 'GND', model='nmos_model', 
               l=channel_length, w=diff_nmos_width)
        self.M('2', 'Vout_int', 'Vinn', 'Vbias1', 'GND', model='nmos_model', 
               l=channel_length, w=diff_nmos_width)
        
        # 有源负载
        self.M('3', 'Vout', 'Vbias2', 'VDD', 'VDD', model='pmos_model', 
               l=channel_length, w=diff_pmos_width)
        self.M('4', 'Vout', 'Vbias2', 'VDD', 'VDD', model='pmos_model', 
               l=channel_length, w=diff_pmos_width)
        
        # 尾电流源
        self.M('5', 'Vbias1', 'Vbias2', 'GND', 'GND', model='nmos_model', 
               l=channel_length, w=diff_nmos_width*2)