## PySpice Module Generation

Help me generate the PySpice code for the [Model] circuit module. Below is a template for the problem input and response.

## Problem

Model: Inverter01
Description: Digital inverter, complete the voltage inversion of the digital level
Input Nodes: Vin, VDD, GND
Output Nodes: Vout

## Component Selection

**PMOS Transistor**: M1 (used for pull-up) to output high voltage level
**NMOS Transistor**: M2 (used for pull-down) to output low voltage level
**Power Supply**: VDD and GND for DC power supply
**Capacitors**: C1 (Not specified but can be included for coupling and bypass applications if required)

## Code_Generation

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

### Parameter_Explanation

```python
- nmos_width: Channel width of the NMOS transistor, Raising this value increases the NMOS drive strength, but also enlarges the area and raises parasitic capacitances.
- pmos_width: Channel width of the PMOS transistor. Increasing it enhances the PMOS drive capability and improves the rising-edge speed, yet it expands the area and raises power consumption
- channel_length: MOSFET channel length. Shortening it boosts switching speed but aggravates short-channel effects; lengthening it reduces leakage current.
- load_capacitance: Capacitive load at the output node. Larger values slow the switching transients and increase propagation delay; setting it to 0 removes the load capacitor.
```

Some tips that not included in the response:

1. As shown above, the user input only includes the problem section. Your response should be divided into three steps. First, determine the possible component selection for the circuit design. Second, determine the generated code. Lastly, explain the parameters.
2. Also, please note the following requirements:
3. The module class definition should be `class [Model](SubCircuitFactory):`
4. The MOSFETs should use level 1 for simulation and only include the kp and vto parameters. When using MOSFETs, only the width-to-length ratio needs to be defined.
5. For the MOSFET definition `self.MOSFET(name, drain, gate, source, bulk, model, w=w1,l=l1)`, be careful about the parameter sequence.
6. Connect the bulk of a MOSFET to its source.
7. Other basic components include capacitors, resistors, inductors, etc. Avoid calling submodules.
8. Avoid giving any AC voltage in the sources; only consider the operating points.
9. Ensure that the interface of the subcircuit matches the requirements.

Here is the specific input:

## Problem

Model: [Model]
Description: [Description]
Input Nodes: [InputNode]
Ouput Nodes: [OutputNode]
