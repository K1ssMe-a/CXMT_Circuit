## Submodule Connect

I'm designing a [Model] circuit. Please help me complete the connection of this circuit and determine the submodule parameters. below is a template for the problem input and response.

## Model Description

Model: TwoStageDifferentialOpamp
Description: A two-stage differential opamp (first stage: common-source with an active load and a tail current, second stage: common-source with an active load)
Input Nodes: Vinp, Vinn, Vbias1, Vbias2, Vbias3
Output Nodes: Vout

## SubModules

### SubModel 1

Model: DiffInputStage
Description: Differential pair with active load and tail current source (first stage). Converts the differential input into a single-ended signal and drives the following stage.
Input Nodes: Vinp (non-inverting input), Vinn (inverting input), Vbias1 (tail current source bias), Vbias2 (active-load current-mirror bias)
Output Nodes: Vout_int (output of the first stage, fed to the second stage)
Parameters: 
- cs_nmos_width: Channel width of the NMOS driver transistor in the common-source stage. Increasing this value boosts transconductance (gm) and gain, while raising input capacitance and power consumption. Reducing it saves power and area but degrades gain and bandwidth
- cs_pmos_width: Channel width of the PMOS active load transistor. Larger values decrease load resistance, improving output swing at the cost of higher output node capacitance. Smaller values increase gain (through higher load resistance) but limit current drive capability
- channel_length: MOSFET channel length for all transistors. Shorter lengths improve transconductance and frequency response while exacerbating short-channel effects. Longer lengths reduce leakage current and improve matching, but degrade gain and speed

### SubModel 2

Model: CSGainStage
Description: Common-source amplifier with active load (second stage). Provides high voltage gain and drives the output node.
Input Nodes: Vin_int (input of the second stage, connected to the first-stage output), Vbias3 (active-load current-source bias)
Output Nodes: Vout (final output)
Parameters: 
- diff_nmos_width: Channel width of the differential pair input transistors. Increasing enhances input transconductance, CMRR and gain, while increasing input capacitance. Reducing saves power and reduces input capacitance but lowers gain and slew rate
- diff_pmos_width: Channel width of the active load current mirror transistors. Wider devices lower mirror impedance, improving output swing but adding parasitic capacitance. Narrower devices increase gain (through higher output impedance) but limit maximum output current
- channel_length: MOSFET channel length for all devices. Shorter lengths improve transconductance and gain-bandwidth product (GBW). Longer lengths reduce channel-length modulation effects, improving output impedance and DC gain

## Topology

```python
import sys
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

# 2. External imports
from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory
from modules.DiffInputStage import DiffInputStage
from modules.CSGainStage import CSGainStage

# 3. Main class definition
class TwoStageOpamp(SubCircuitFactory):
    NAME  = 'TwoStageOpamp'
    NODES = ('Vinp', 'Vinn',   # differential inputs
             'Vbias1', 'Vbias2', 'Vbias3',  # bias voltages
             'Vout',            # single-ended output
             'VDD', 'GND')      # power rails

    def __init__(self):
        super().__init__()
        #Parameters
        diff_nmos_width: float = 10e-6
        diff_pmos_width: float = 20e-6
        cs_nmos_width : float = 20e-6
        cs_pmos_width : float = 20e-6
        channel_length: float = 0.18e-6

        self.model('nmos_model', 'nmos', level=1, kp=200e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=100e-6, vto=-0.5)

        # 3.2 Sub-circuits
        self.subcircuit(DiffInputStage(
            diff_nmos_width=diff_nmos_width,
            diff_pmos_width=diff_pmos_width,
            channel_length=channel_length))

        self.subcircuit(CSGainStage(
            cs_nmos_width=cs_nmos_width,
            cs_pmos_width=cs_pmos_width,
            channel_length=channel_length))

        # 3.3 Circuit instantiation
        self.X('diff_stage', 'DiffInputStage',
               'Vinp', 'Vinn', 'Vbias1', 'Vbias2', 'Vout_int',
               'VDD', 'GND')

        # 3.3.2 Common-source gain stage
        self.X('cs_stage', 'CSGainStage',
               'Vout_int', 'Vbias3', 'Vout',
               'VDD', 'GND')

        # 3.4 Biasing devices
        self.M('Mbias', 'Vbias3', 'Vbias3', 'VDD', 'VDD',
               model='pmos_model',
               l=channel_length,
               w=cs_pmos_width * 0.5)      # Half the width of the load device

        # Tail-current source for the differential pair
        self.M('Mtail_bias', 'Vbias2', 'Vbias2', 'GND', 'GND',
               model='nmos_model',
               l=channel_length,
               w=diff_nmos_width * 2)      # Twice the width of the input devices

```

Additional notes not included in the response:
1. 用户的输入仅包含Model Description和SubModules部分，请据此回答Topology部分


Here is the specific input:

## Model Description

Model: [Model]
Description: [Description]
Input Nodes: [InputNode]
Ouput Nodes: [OutputNode]

## SubModules

