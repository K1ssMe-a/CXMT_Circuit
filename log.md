## 1. Top Circuit Generate Input

Please help me determine the sub-module required by a ClockDataRecovery circuit and the connection method of the sub-module，below is a template for the problem input and response.

**Model Description**

Model: TwoStageDifferentialOpamp
Description: A two-stage differential opamp (first stage: common-source with an active load and a tail current, second stage: common-source with an active load)
Input Nodes: Vinp, Vinn, Vbias1, Vbias2, Vbias3
Output Nodes: Vout

**Module 01**

Model: DiffInputStage
Description: Differential pair with active load and tail current source (first stage). Converts the differential input into a single-ended signal and drives the following stage.
Input Nodes: Vinp (non-inverting input), Vinn (inverting input), Vbias1 (tail current source bias), Vbias2 (active-load current-mirror bias)
Output Nodes: Vout_int (output of the first stage, fed to the second stage)

**Module 02**

Model: CSGainStage
Description: Common-source amplifier with active load (second stage). Provides high voltage gain and drives the output node.
Input Nodes: Vin_int (input of the second stage, connected to the first-stage output), Vbias3 (active-load current-source bias)
Output Nodes: Vout (final output)

**Topology**

```python
class TwoStageOpamp(SubCircuitFactory):
    NAME = 'TwoStageOpamp'
    NODES = ('Vinp', 'Vinn', 'Vbias1', 'Vbias2', 'Vbias3', 'Vout', 'VDD', 'GND')

    def __init__(self):
	 #Parameters
        [diff_nmos_width=xx
        diff_pmos_width=xx
        cs_nmos_width=xx
        cs_pmos_width=xx
        channel_length=xx
        compensation_capacitor=xx
        compensation_resistor=xx]

        super().__init__()

        self.model('nmos_model', 'nmos', level=1, kp=200e-6, vto=0.5)
        self.model('pmos_model', 'pmos', level=1, kp=100e-6, vto=-0.5)

        # Add sub-circuit definitions
        self.subcircuit(DiffInputStage('diff_stage', [some parameter]))
        self.subcircuit(CSGainStage('cs_stage', [some parameter]))

        # Instantiate sub-modules
        self.X('diff_stage', 'DiffInputStage',
               'Vinp', 'Vinn', 'Vbias1', 'Vbias2', 'Vout_int',
               'VDD', 'GND',
               some_parameters(placeholder))

        self.X('cs_stage', 'CSGainStage',
               'Vout_int', 'Vbias3', 'Vout',
               'VDD', 'GND',
               some_parameters(placeholder))

       [other devices]

```

Additional notes not included in the response:

1. User input only contains the Model Description section, and you need to generate sub-modules and Topology sections accordingly.
2. There is no need to generate circuits for submodules.
3. Note that in the Topology section, you only need to define the top-level modules clearly, and directly call the sub-modules and other required devices.

Here is the specific input:

**Model Description**

Model: ClockDataRecovery
Description: A clock and data recovery circuit consisting of four key components: a phase detector (PD), loop filter (LF), voltage-controlled oscillator (VCO), and data recovery unit. The PD detects phase differences between input data and the VCO clock, the LF converts phase errors into a control voltage, the VCO generates an adjustable clock signal, and the recovery unit samples data using the synchronized clock.
Input Nodes: DataIn, Vctrl_Init (initial VCO control voltage), VDD, VSS
Ouput Nodes: RecoveredClk, RecoveredData



## 1. Top Circuit Generate Output

**Module 01**

Model: PhaseDetector
Description: Detects the phase difference between the input data and the VCO clock signal. Outputs a signal proportional to the phase error.
Input Nodes: DataIn (input data signal), VCO_Clk (clock from VCO), VDD (power supply), VSS (ground)
Output Nodes: PhaseError (phase difference signal)

**Module 02**

Model: LoopFilter
Description: Low-pass filter that converts the phase error signal from the PD into a stable control voltage for the VCO.
Input Nodes: PhaseError (input from phase detector), VDD (power supply), VSS (ground)
Output Nodes: Vctrl (control voltage for VCO)

**Module 03**

Model: VoltageControlledOscillator
Description: Generates a clock signal whose frequency is controlled by the input control voltage from the loop filter.
Input Nodes: Vctrl (control voltage from loop filter), Vctrl_Init (initial control voltage), VDD (power supply), VSS (ground)
Output Nodes: VCO_Clk (output clock signal)

**Module 04**

Model: DataRecoveryUnit
Description: Samples the input data using the synchronized clock from the VCO to recover the original data.
Input Nodes: DataIn (input data signal), VCO_Clk (synchronized clock from VCO), VDD (power supply), VSS (ground)
Output Nodes: RecoveredData (output recovered data)

**Topology**

```python
class ClockDataRecovery(SubCircuitFactory):
    NAME = 'ClockDataRecovery'
    NODES = ('DataIn', 'Vctrl_Init', 'VDD', 'VSS', 'RecoveredClk', 'RecoveredData')

    def __init__(self):
        # Parameters
        [pd_gain=xx
        lf_cutoff=xx
        vco_gain=xx
        dr_setup_time=xx
        dr_hold_time=xx]

        super().__init__()

        # Add sub-circuit definitions
        self.subcircuit(PhaseDetector('pd', [some parameter]))
        self.subcircuit(LoopFilter('lf', [some parameter]))
        self.subcircuit(VoltageControlledOscillator('vco', [some parameter]))
        self.subcircuit(DataRecoveryUnit('dr', [some parameter]))

        # Instantiate sub-modules
        self.X('pd', 'PhaseDetector',
               'DataIn', 'VCO_Clk', 'VDD', 'VSS', 'PhaseError',
               some_parameters(placeholder))

        self.X('lf', 'LoopFilter',
               'PhaseError', 'VDD', 'VSS', 'Vctrl',
               some_parameters(placeholder))

        self.X('vco', 'VoltageControlledOscillator',
               'Vctrl', 'Vctrl_Init', 'VDD', 'VSS', 'VCO_Clk',
               some_parameters(placeholder))

        self.X('dr', 'DataRecoveryUnit',
               'DataIn', 'VCO_Clk', 'VDD', 'VSS', 'RecoveredData',
               some_parameters(placeholder))

        # Connect VCO clock to output
        self.connect('VCO_Clk', 'RecoveredClk')

        [other devices]
```

## 2. PySpice Module Generation Input

Help me generate the PySpice code for the PhaseDetector circuit module. Below is a template for the problem input and response.

**Problem**

Model: Inverter01
Description: Digital inverter, complete the voltage inversion of the digital level
Input Nodes: Vin, VDD, GND
Output Nodes: Vout

**Component Selection**

PMOS Transistor: M1 (used for pull-up) to output high voltage level
NMOS Transistor: M2 (used for pull-down) to output low voltage level
Power Supply: VDD and GND for DC power supply
Capacitors: C1 (Not specified but can be included for coupling and bypass applications if required)

**Code_Generation**

```python
from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class Inverter01(SubCircuitFactory):
    NAME = 'Inverter01'
    NODES = ('Vin', 'Vout', 'VDD', 'GND')
  
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
```

**Parameter_Explanation**

```python
- nmos_width: Channel width of the NMOS transistor, Raising this value increases the NMOS drive strength, but also enlarges the area and raises parasitic capacitances.
- pmos_width: Channel width of the PMOS transistor. Increasing it enhances the PMOS drive capability and improves the rising-edge speed, yet it expands the area and raises power consumption
- channel_length: MOSFET channel length. Shortening it boosts switching speed but aggravates short-channel effects; lengthening it reduces leakage current.
- load_capacitance: Capacitive load at the output node. Larger values slow the switching transients and increase propagation delay; setting it to 0 removes the load capacitor.
```

Some tips that not included in the response:

1. As shown above, the user input only includes the problem section. Your response should be divided into three steps. First, determine the possible component selection for the circuit design. Second, determine the generated code. Lastly, explain the parameters.
2. Also, please note the following requirements:
3. The module class definition should be `class PhaseDetector(SubCircuitFactory):`
4. The MOSFETs should use level 1 for simulation and only include the kp and vto parameters. When using MOSFETs, only the width-to-length ratio needs to be defined.
5. For the MOSFET definition `self.MOSFET(name, drain, gate, source, bulk, model, w=w1,l=l1)`, be careful about the parameter sequence.
6. Connect the bulk of a MOSFET to its source.
7. Other basic components include capacitors, resistors, inductors, etc. Avoid calling submodules.
8. Avoid giving any AC voltage in the sources; only consider the operating points.
9. Ensure that the interface of the subcircuit matches the requirements.

Here is the specific input:

**Problem**

Model: PhaseDetector
Description: Detects the phase difference between the input data and the VCO clock signal. Outputs a signal proportional to the phase error.
Input Nodes: DataIn (input data signal), VCO_Clk (clock from VCO), VDD (power supply), VSS (ground)
Ouput Nodes: PhaseError (phase difference signal)



## 2. PySpice Module Generation Output

**Component Selection**

**PMOS Transistors**: M1, M2 (used for pull-up network)
**NMOS Transistors**: M3, M4 (used for pull-down network)
**Power Supply**: VDD and VSS for DC power supply
**Capacitors**: C1 (for filtering the output signal)
**Resistors**: R1 (optional, for output impedance matching)

**Code_Generation**

```python
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
```

**Parameter_Explanation**

```python
- nmos_width: Channel width of the NMOS transistors (M3, M4). Increasing this value strengthens the pull-down capability but increases area and capacitance.
- pmos_width: Channel width of the PMOS transistors (M1, M2). Larger widths improve pull-up strength but consume more area and power.
- channel_length: MOSFET channel length for all transistors. Smaller lengths increase speed but may worsen short-channel effects.
- filter_capacitance: Capacitance at the output node to filter high-frequency noise. Larger values provide better filtering but slow down the response time. Set to 0 to remove the capacitor.
```

Note: This implementation shows a basic XOR-type phase detector topology where the output voltage represents the phase difference between DataIn and VCO_Clk. The output will be high when the inputs are out of phase and low when they are in phase. The filter capacitor helps smooth the output signal.
Module code written to ./modules/PhaseDetector.py
Get circuit generation prompt:
## 3. PySpice Module Generation Input

Help me generate the PySpice code for the LoopFilter circuit module. Below is a template for the problem input and response.

**Problem**

Model: Inverter01
Description: Digital inverter, complete the voltage inversion of the digital level
Input Nodes: Vin, VDD, GND
Output Nodes: Vout

**Component Selection**

PMOS Transistor: M1 (used for pull-up) to output high voltage level
**NMOS Transistor**: M2 (used for pull-down) to output low voltage level
Power Supply: VDD and GND for DC power supply
Capacitors: C1 (Not specified but can be included for coupling and bypass applications if required)

**Code_Generation**

```python
from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class Inverter01(SubCircuitFactory):
    NAME = 'Inverter01'
    NODES = ('Vin', 'Vout', 'VDD', 'GND')
  
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
```

**Parameter_Explanation**

```python
- nmos_width: Channel width of the NMOS transistor, Raising this value increases the NMOS drive strength, but also enlarges the area and raises parasitic capacitances.
- pmos_width: Channel width of the PMOS transistor. Increasing it enhances the PMOS drive capability and improves the rising-edge speed, yet it expands the area and raises power consumption
- channel_length: MOSFET channel length. Shortening it boosts switching speed but aggravates short-channel effects; lengthening it reduces leakage current.
- load_capacitance: Capacitive load at the output node. Larger values slow the switching transients and increase propagation delay; setting it to 0 removes the load capacitor.
```

Some tips that not included in the response:

1. As shown above, the user input only includes the problem section. Your response should be divided into three steps. First, determine the possible component selection for the circuit design. Second, determine the generated code. Lastly, explain the parameters.
2. Also, please note the following requirements:
3. The module class definition should be `class LoopFilter(SubCircuitFactory):`
4. The MOSFETs should use level 1 for simulation and only include the kp and vto parameters. When using MOSFETs, only the width-to-length ratio needs to be defined.
5. For the MOSFET definition `self.MOSFET(name, drain, gate, source, bulk, model, w=w1,l=l1)`, be careful about the parameter sequence.
6. Connect the bulk of a MOSFET to its source.
7. Other basic components include capacitors, resistors, inductors, etc. Avoid calling submodules.
8. Avoid giving any AC voltage in the sources; only consider the operating points.
9. Ensure that the interface of the subcircuit matches the requirements.

Here is the specific input:

**Problem**

Model: LoopFilter
Description: Low-pass filter that converts the phase error signal from the PD into a stable control voltage for the VCO.
Input Nodes: PhaseError (input from phase detector), VDD (power supply), VSS (ground)
Ouput Nodes: Vctrl (control voltage for VCO)

## 3. PySpice Module Generation Output

**Component Selection**

Resistors: R1, R2 (used to set the filter time constants and gain)
Capacitors: C1, C2 (used to create the low-pass filtering effect)
Operational Amplifier: Not explicitly modeled here, but the filter can be designed to work with an external op-amp if needed
Power Supply: VDD and VSS for DC power supply

**Code_Generation**

```python
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
```

**Parameter_Explanation**

```python
- r1: Resistance of R1. Increasing this value raises the time constant of the first pole, slowing the filter response but improving stability.
- r2: Resistance of R2. Increasing this value raises the time constant of the second pole, further slowing the filter response but reducing ripple on the control voltage.
- c1: Capacitance of C1. Increasing this value lowers the cutoff frequency of the first pole, smoothing the control voltage but increasing settling time.
- c2: Capacitance of C2. Increasing this value lowers the cutoff frequency of the second pole, providing additional filtering of high-frequency noise but potentially increasing phase lag.
```
Module code written to ./modules/LoopFilter.py
## 4. PySpice Module Generation Input

Help me generate the PySpice code for the VoltageControlledOscillator circuit module. Below is a template for the problem input and response.

**Problem**

Model: Inverter01
Description: Digital inverter, complete the voltage inversion of the digital level
Input Nodes: Vin, VDD, GND
Output Nodes: Vout

**Component Selection**

PMOS Transistor: M1 (used for pull-up) to output high voltage level
NMOS Transistor: M2 (used for pull-down) to output low voltage level
Power Supply: VDD and GND for DC power supply
Capacitors: C1 (Not specified but can be included for coupling and bypass applications if required)

**Code_Generation**

```python
from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class Inverter01(SubCircuitFactory):
    NAME = 'Inverter01'
    NODES = ('Vin', 'Vout', 'VDD', 'GND')
  
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
```

**Parameter_Explanation**

```python
- nmos_width: Channel width of the NMOS transistor, Raising this value increases the NMOS drive strength, but also enlarges the area and raises parasitic capacitances.
- pmos_width: Channel width of the PMOS transistor. Increasing it enhances the PMOS drive capability and improves the rising-edge speed, yet it expands the area and raises power consumption
- channel_length: MOSFET channel length. Shortening it boosts switching speed but aggravates short-channel effects; lengthening it reduces leakage current.
- load_capacitance: Capacitive load at the output node. Larger values slow the switching transients and increase propagation delay; setting it to 0 removes the load capacitor.
```

Some tips that not included in the response:

1. As shown above, the user input only includes the problem section. Your response should be divided into three steps. First, determine the possible component selection for the circuit design. Second, determine the generated code. Lastly, explain the parameters.
2. Also, please note the following requirements:
3. The module class definition should be `class VoltageControlledOscillator(SubCircuitFactory):`
4. The MOSFETs should use level 1 for simulation and only include the kp and vto parameters. When using MOSFETs, only the width-to-length ratio needs to be defined.
5. For the MOSFET definition `self.MOSFET(name, drain, gate, source, bulk, model, w=w1,l=l1)`, be careful about the parameter sequence.
6. Connect the bulk of a MOSFET to its source.
7. Other basic components include capacitors, resistors, inductors, etc. Avoid calling submodules.
8. Avoid giving any AC voltage in the sources; only consider the operating points.
9. Ensure that the interface of the subcircuit matches the requirements.

Here is the specific input:

**Problem**

Model: VoltageControlledOscillator
Description: Generates a clock signal whose frequency is controlled by the input control voltage from the loop filter.
Input Nodes: Vctrl (control voltage from loop filter), Vctrl_Init (initial control voltage), VDD (power supply), VSS (ground)
Ouput Nodes: VCO_Clk (output clock signal)

Get response from deepseek-chat:

## 4. PySpice Module Generation Output

**Component Selection**

Ring Oscillator Core: 

- 3 inverter stages (odd number required for oscillation)
- Each inverter uses complementary MOSFET pairs (PMOS + NMOS)

Current Starved Inverters:

- PMOS and NMOS transistors for each inverter stage with controlled current
- Additional control transistors (PMOS and NMOS) to implement current starving

Bias Circuitry:

- Control transistors (Mp_ctrl, Mn_ctrl) to regulate current based on Vctrl
- Initial control transistors (Mp_init, Mn_init) for startup

Power Supply: VDD and VSS for DC power supply
Capacitors: C1 (output load capacitor)

**Code_Generation**

```python
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
```

**Parameter_Explanation**

```python
- inverter_width_n: Channel width of NMOS transistors in inverter stages. Affects switching speed and power consumption.
- inverter_width_p: Channel width of PMOS transistors in inverter stages. Typically 2x NMOS width for balanced rise/fall times.
- control_width_n: Channel width of NMOS control transistors. Larger values increase current and oscillation frequency range.
- control_width_p: Channel width of PMOS control transistors. Larger values increase current and oscillation frequency range.
- channel_length: MOSFET channel length. Affects speed, power, and short-channel effects.
- load_capacitance: Output load capacitance. Larger values decrease oscillation frequency.

Key Features:
1. Current-starved architecture allows frequency control via Vctrl
2. Three-stage ring oscillator provides necessary phase shift for oscillation
3. Separate initial control voltage (Vctrl_Init) ensures startup
4. All bulks properly connected to prevent latch-up
5. Simple level 1 MOSFET models for fast simulation
```
Module code written to ./modules/VoltageControlledOscillator.py
Get circuit generation prompt:

## 5. PySpice Module Generation Input

Help me generate the PySpice code for the DataRecoveryUnit circuit module. Below is a template for the problem input and response.

**Problem**

Model: Inverter01
Description: Digital inverter, complete the voltage inversion of the digital level
Input Nodes: Vin, VDD, GND
Output Nodes: Vout

**Component Selection**

**PMOS Transistor**: M1 (used for pull-up) to output high voltage level
**NMOS Transistor**: M2 (used for pull-down) to output low voltage level
**Power Supply**: VDD and GND for DC power supply
**Capacitors**: C1 (Not specified but can be included for coupling and bypass applications if required)

**Code_Generation**

```python
from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory

class Inverter01(SubCircuitFactory):
    NAME = 'Inverter01'
    NODES = ('Vin', 'Vout', 'VDD', 'GND')
  
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
```

**Parameter_Explanation**

```python
- nmos_width: Channel width of the NMOS transistor, Raising this value increases the NMOS drive strength, but also enlarges the area and raises parasitic capacitances.
- pmos_width: Channel width of the PMOS transistor. Increasing it enhances the PMOS drive capability and improves the rising-edge speed, yet it expands the area and raises power consumption
- channel_length: MOSFET channel length. Shortening it boosts switching speed but aggravates short-channel effects; lengthening it reduces leakage current.
- load_capacitance: Capacitive load at the output node. Larger values slow the switching transients and increase propagation delay; setting it to 0 removes the load capacitor.
```

Some tips that not included in the response:

1. As shown above, the user input only includes the problem section. Your response should be divided into three steps. First, determine the possible component selection for the circuit design. Second, determine the generated code. Lastly, explain the parameters.
2. Also, please note the following requirements:
3. The module class definition should be `class DataRecoveryUnit(SubCircuitFactory):`
4. The MOSFETs should use level 1 for simulation and only include the kp and vto parameters. When using MOSFETs, only the width-to-length ratio needs to be defined.
5. For the MOSFET definition `self.MOSFET(name, drain, gate, source, bulk, model, w=w1,l=l1)`, be careful about the parameter sequence.
6. Connect the bulk of a MOSFET to its source.
7. Other basic components include capacitors, resistors, inductors, etc. Avoid calling submodules.
8. Avoid giving any AC voltage in the sources; only consider the operating points.
9. Ensure that the interface of the subcircuit matches the requirements.

Here is the specific input:

**Problem**

Model: DataRecoveryUnit
Description: Samples the input data using the synchronized clock from the VCO to recover the original data.
Input Nodes: DataIn (input data signal), VCO_Clk (synchronized clock from VCO), VDD (power supply), VSS (ground)
Ouput Nodes: RecoveredData (output recovered data)

Get response from deepseek-chat:

## 5.PySpice Module Generation Output

**Component Selection**

D Flip-Flop Core Components:
- 2 Transmission Gates (for data sampling)
- 2 Inverters (for signal buffering)
- 2 PMOS Transistors (for pull-up networks)
- 2 NMOS Transistors (for pull-down networks)

Additional Components:
- Power Supply: VDD and VSS for DC power
- Capacitors: Optional load capacitance at output

**Code_Generation**

```python
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
```

**Parameter_Explanation**

```python
- nmos_width: Channel width of NMOS transistors. Increasing this enhances drive strength but increases area and capacitance.
- pmos_width: Channel width of PMOS transistors. Larger values improve rising edge speed but consume more area and power.
- channel_length: MOSFET channel length. Smaller values increase speed but may worsen short-channel effects.
- load_capacitance: Output capacitive load. Higher values slow down transitions but may represent realistic load conditions.

Circuit Operation:
1. The master stage samples input data when clock is high
2. The slave stage transfers data to output when clock is low
3. Inverters provide signal restoration
4. Transmission gates control the sampling timing
```
Module code written to ./modules/DataRecoveryUnit.py
Get top circuit generation prompt:
## 6. Submodule Connect Input

I'm designing a ClockDataRecovery circuit. Please help me complete the connection of this circuit and determine the submodule parameters. below is a template for the problem input and response.

**Model Description**

Model: TwoStageDifferentialOpamp
Description: A two-stage differential opamp (first stage: common-source with an active load and a tail current, second stage: common-source with an active load)
Input Nodes: Vinp, Vinn, Vbias1, Vbias2, Vbias3
Output Nodes: Vout

**SubModules**

**SubModel 1** 

Model: DiffInputStage
Description: Differential pair with active load and tail current source (first stage). Converts the differential input into a single-ended signal and drives the following stage.
Input Nodes: Vinp (non-inverting input), Vinn (inverting input), Vbias1 (tail current source bias), Vbias2 (active-load current-mirror bias)
Output Nodes: Vout_int (output of the first stage, fed to the second stage)
Parameters: 

- cs_nmos_width: Channel width of the NMOS driver transistor in the common-source stage. Increasing this value boosts transconductance (gm) and gain, while raising input capacitance and power consumption. Reducing it saves power and area but degrades gain and bandwidth
- cs_pmos_width: Channel width of the PMOS active load transistor. Larger values decrease load resistance, improving output swing at the cost of higher output node capacitance. Smaller values increase gain (through higher load resistance) but limit current drive capability
- channel_length: MOSFET channel length for all transistors. Shorter lengths improve transconductance and frequency response while exacerbating short-channel effects. Longer lengths reduce leakage current and improve matching, but degrade gain and speed

**SubModel 2**

Model: CSGainStage
Description: Common-source amplifier with active load (second stage). Provides high voltage gain and drives the output node.
Input Nodes: Vin_int (input of the second stage, connected to the first-stage output), Vbias3 (active-load current-source bias)
Output Nodes: Vout (final output)
Parameters: 

- diff_nmos_width: Channel width of the differential pair input transistors. Increasing enhances input transconductance, CMRR and gain, while increasing input capacitance. Reducing saves power and reduces input capacitance but lowers gain and slew rate
- diff_pmos_width: Channel width of the active load current mirror transistors. Wider devices lower mirror impedance, improving output swing but adding parasitic capacitance. Narrower devices increase gain (through higher output impedance) but limit maximum output current
- channel_length: MOSFET channel length for all devices. Shorter lengths improve transconductance and gain-bandwidth product (GBW). Longer lengths reduce channel-length modulation effects, improving output impedance and DC gain

**Topology**

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

**Model Description**

Model: ClockDataRecovery
Description: A clock and data recovery circuit consisting of four key components: a phase detector (PD), loop filter (LF), voltage-controlled oscillator (VCO), and data recovery unit. The PD detects phase differences between input data and the VCO clock, the LF converts phase errors into a control voltage, the VCO generates an adjustable clock signal, and the recovery unit samples data using the synchronized clock.
Input Nodes: DataIn, Vctrl_Init (initial VCO control voltage), VDD, VSS
Ouput Nodes: RecoveredClk, RecoveredData

**SubModules**

**SubModel 1**
Model: PhaseDetectorDescription: Detects the phase difference between the input data and the VCO clock signal. Outputs a signal proportional to the phase error.Input Nodes: DataIn (input data signal), VCO_Clk (clock from VCO), VDD (power supply), VSS (ground)Output Nodes: PhaseError (phase difference signal)
Parameters: 

- nmos_width: Channel width of the NMOS transistors (M3, M4). Increasing this value strengthens the pull-down capability but increases area and capacitance.
- pmos_width: Channel width of the PMOS transistors (M1, M2). Larger widths improve pull-up strength but consume more area and power.
- channel_length: MOSFET channel length for all transistors. Smaller lengths increase speed but may worsen short-channel effects.
- filter_capacitance: Capacitance at the output node to filter high-frequency noise. Larger values provide better filtering but slow down the response time. Set to 0 to remove the capacitor.

**SubModel 2**
Model: LoopFilterDescription: Low-pass filter that converts the phase error signal from the PD into a stable control voltage for the VCO.Input Nodes: PhaseError (input from phase detector), VDD (power supply), VSS (ground)Output Nodes: Vctrl (control voltage for VCO)
Parameters: 

- r1: Resistance of R1. Increasing this value raises the time constant of the first pole, slowing the filter response but improving stability.
-  r2: Resistance of R2. Increasing this value raises the time constant of the second pole, further slowing the filter response but reducing ripple on the control voltage.
- c1: Capacitance of C1. Increasing this value lowers the cutoff frequency of the first pole, smoothing the control voltage but increasing settling time.
- c2: Capacitance of C2. Increasing this value lowers the cutoff frequency of the second pole, providing additional filtering of high-frequency noise but potentially increasing phase lag.

**SubModel 3**
Model: VoltageControlledOscillatorDescription: Generates a clock signal whose frequency is controlled by the input control voltage from the loop filter.Input Nodes: Vctrl (control voltage from loop filter), Vctrl_Init (initial control voltage), VDD (power supply), VSS (ground)Output Nodes: VCO_Clk (output clock signal)
Parameters: 

- inverter_width_n: Channel width of NMOS transistors in inverter stages. Affects switching speed and power consumption.
-  inverter_width_p: Channel width of PMOS transistors in inverter stages. Typically 2x NMOS width for balanced rise/fall times.
- control_width_n: Channel width of NMOS control transistors. Larger values increase current and oscillation frequency range.
- control_width_p: Channel width of PMOS control transistors. Larger values increase current and oscillation frequency range.
- channel_length: MOSFET channel length. Affects speed, power, and short-channel effects.
- load_capacitance: Output load capacitance. Larger values decrease oscillation frequency.
- Key Features:Current-starved architecture allows frequency control via Vctrl. Three-stage ring oscillator provides necessary phase shift for oscillation. Separate initial control voltage (Vctrl_Init) ensures startup. All bulks properly connected to prevent latch-up. Simple level 1 MOSFET models for fast simulation

**SubModel 4**
Model: DataRecoveryUnitDescription: Samples the input data using the synchronized clock from the VCO to recover the original data.Input Nodes: DataIn (input data signal), VCO_Clk (synchronized clock from VCO), VDD (power supply), VSS (ground)Output Nodes: RecoveredData (output recovered data)
Parameters: 

- nmos_width: Channel width of NMOS transistors. Increasing this enhances drive strength but increases area and capacitance.
- pmos_width: Channel width of PMOS transistors. Larger values improve rising edge speed but consume more area and power.
- channel_length: MOSFET channel length. Smaller values increase speed but may worsen short-channel effects.
- load_capacitance: Output capacitive load. Higher values slow down transitions but may represent realistic load conditions.
- Circuit Operation: The master stage samples input data when clock is high. The slave stage transfers data to output when clock is low. Inverters provide signal restoration. Transmission gates control the sampling timing

Get response from deepseek-chat:



## 6. Submodule Connect Output


Here's the completed topology for the ClockDataRecovery circuit with submodule connections:

```python
import sys
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

# External imports
from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory
from modules.PhaseDetector import PhaseDetector
from modules.LoopFilter import LoopFilter
from modules.VoltageControlledOscillator import VoltageControlledOscillator
from modules.DataRecoveryUnit import DataRecoveryUnit

class ClockDataRecovery(SubCircuitFactory):
    NAME = 'ClockDataRecovery'
    NODES = ('DataIn', 'Vctrl_Init',  # Input signals
             'RecoveredClk', 'RecoveredData',  # Output signals
             'VDD', 'VSS')  # Power rails

    def __init__(self):
        super().__init__()
        
        # Parameters for submodules (example values, can be adjusted)
        pd_params = {
            'nmos_width': 10e-6,
            'pmos_width': 20e-6,
            'channel_length': 0.18e-6,
            'filter_capacitance': 1e-12
        }
        
        lf_params = {
            'r1': 10e3,
            'r2': 100e3,
            'c1': 10e-12,
            'c2': 1e-12
        }
        
        vco_params = {
            'inverter_width_n': 5e-6,
            'inverter_width_p': 10e-6,
            'control_width_n': 10e-6,
            'control_width_p': 20e-6,
            'channel_length': 0.18e-6,
            'load_capacitance': 10e-15
        }
        
        dr_params = {
            'nmos_width': 10e-6,
            'pmos_width': 20e-6,
            'channel_length': 0.18e-6,
            'load_capacitance': 10e-15
        }

        # Instantiate submodules
        self.subcircuit(PhaseDetector(**pd_params))
        self.subcircuit(LoopFilter(**lf_params))
        self.subcircuit(VoltageControlledOscillator(**vco_params))
        self.subcircuit(DataRecoveryUnit(**dr_params))

        # Phase Detector
        self.X('PD', 'PhaseDetector',
               'DataIn', 'VCO_Clk', 'PhaseError',
               'VDD', 'VSS')

        # Loop Filter
        self.X('LF', 'LoopFilter',
               'PhaseError', 'Vctrl',
               'VDD', 'VSS')

        # Voltage Controlled Oscillator
        self.X('VCO', 'VoltageControlledOscillator',
               'Vctrl', 'Vctrl_Init', 'VCO_Clk',
               'VDD', 'VSS')

        # Data Recovery Unit
        self.X('DR', 'DataRecoveryUnit',
               'DataIn', 'VCO_Clk', 'RecoveredData',
               'VDD', 'VSS')

        # Connect VCO clock to output node
        self.R('clk_out', 'VCO_Clk', 'RecoveredClk', 1@u_Ω)  # Small resistor for simulation stability
```

Key connections and notes:
1. The phase detector compares DataIn with VCO_Clk and outputs PhaseError
2. The loop filter processes PhaseError to generate Vctrl
3. The VCO uses Vctrl (and initial Vctrl_Init) to generate VCO_Clk
4. The data recovery unit samples DataIn using VCO_Clk to produce RecoveredData
5. VCO_Clk is also directly available as RecoveredClk output
6. All submodules share common power rails (VDD, VSS)
7. Example parameter values are provided but should be adjusted based on specific technology and performance requirements

The circuit forms a complete PLL-based clock and data recovery system where the VCO clock synchronizes to the input data edges through the phase detector and loop filter feedback path.
