## Top Circuit Generate

Please help me determine the sub-module required by a [Model] circuit and the connection method of the sub-module，below is a template for the problem input and response.

## Model Description

Model: TwoStageDifferentialOpamp
Description: A two-stage differential opamp (first stage: common-source with an active load and a tail current, second stage: common-source with an active load)
Input Nodes: Vinp, Vinn, Vbias1, Vbias2, Vbias3
Output Nodes: Vout

## Module 01

Model: DiffInputStage
Description: Differential pair with active load and tail current source (first stage). Converts the differential input into a single-ended signal and drives the following stage.
Input Nodes: Vinp (non-inverting input), Vinn (inverting input), Vbias1 (tail current source bias), Vbias2 (active-load current-mirror bias)
Output Nodes: Vout_int (output of the first stage, fed to the second stage)

## Module 02

Model: CSGainStage
Description: Common-source amplifier with active load (second stage). Provides high voltage gain and drives the output node.
Input Nodes: Vin_int (input of the second stage, connected to the first-stage output), Vbias3 (active-load current-source bias)
Output Nodes: Vout (final output)

## Topology

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

## Model Description

Model: [Model]
Description: [Description]
Input Nodes: [InputNode]
Ouput Nodes: [OutputNode]
