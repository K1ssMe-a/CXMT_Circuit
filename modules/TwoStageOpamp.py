import sys
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory
from modules.DiffInputStage import DiffInputStage
from modules.CSGainStage import CSGainStage

class TwoStageOpamp(SubCircuitFactory):
    NAME = 'TwoStageOpamp'
    NODES = ('Vinp', 'Vinn', 'Vbias1', 'Vbias2', 'Vbias3', 'Vout', 'VDD', 'GND')

    def __init__(self,
                 diff_nmos_width=10e-6, diff_pmos_width=20e-6,
                 cs_nmos_width=20e-6, cs_pmos_width=20e-6,
                 channel_length=0.18e-6,
                 compensation_capacitor=2e-12,
                 compensation_resistor=0):

        super().__init__()

       # 添加MOSFET模型定义
        self.model('nmos_model', 'nmos', level=1, kp=200e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=100e-6, vto=-0.5)

        # 添加子电路定义（包含MOSFET模型）
        self.subcircuit(DiffInputStage(
            diff_nmos_width=diff_nmos_width, 
            diff_pmos_width=diff_pmos_width, 
            channel_length=channel_length
        ))
        
        self.subcircuit(CSGainStage(
            cs_nmos_width=cs_nmos_width, 
            cs_pmos_width=cs_pmos_width, 
            channel_length=channel_length
        ))

        # 实例化差分输入级
        self.X('diff_stage', 'DiffInputStage',
               'Vinp', 'Vinn', 'Vbias1', 'Vbias2', 'Vout_int',
               'VDD', 'GND',
               diff_nmos_width=diff_nmos_width, 
               diff_pmos_width=diff_pmos_width, 
               channel_length=channel_length)

        # 实例化共源增益级
        self.X('cs_stage', 'CSGainStage',
               'Vout_int', 'Vbias3', 'Vout',
               'VDD', 'GND',
               cs_nmos_width=cs_nmos_width, 
               cs_pmos_width=cs_pmos_width, 
               channel_length=channel_length)

        # 添加输出级偏置电流源（确保输出级正常工作）
        self.M('Mbias', 'Vbias3', 'Vbias3', 'VDD', 'VDD', 
               model='pmos_model', 
               l=channel_length, 
               w=cs_pmos_width * 0.5)  # 偏置管尺寸为负载管的一半
        
        # 添加尾电流源偏置（确保差分对正常工作）
        self.M('Mtail_bias', 'Vbias2', 'Vbias2', 'GND', 'GND', 
               model='nmos_model', 
               l=channel_length, 
               w=diff_nmos_width * 2)  # 尾电流源偏置管尺寸为差分对管的两倍