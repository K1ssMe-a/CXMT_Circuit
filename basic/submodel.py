from dataclasses import dataclass
import os

def read_file(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except:
        pass


@dataclass
class SUBMODEL:
    model: str
    description: str
    inputnode: str
    outputnode: str
    parameter: str = None
    modelcode: str = None
    topology: str = None

    def __post_init__(self):
        self.read_model_code()

    def read_model_code(self):
        content = read_file(f'./modules/{self.model}.py')
        if content != None:
            self.modelcode = content

    def get_replacement(self):
        replacement = {
            'Model': self.model,
            'Description': self.description,
            'InputNode': self.inputnode,
            'OutputNode': self.outputnode,
            'ModelCode': self.modelcode,
            'Parameter': self.parameter
        }
        return replacement


Inverter01 = SUBMODEL(
    model='Inverter01',
    description='Digital inverter, complete the voltage inversion of the digital level',
    inputnode='Vin, VDD, GND',
    outputnode='Vout'
)


OneStageAmplifer01 = SUBMODEL(
    model="OneStageAmplifier01",
    description='One Stage Source-Common Amplifier with Resistor Load',
    inputnode='Vin, Vbias, VDD, GND',
    outputnode='Vout'
)

TwoStageDifferentialOpamp = SUBMODEL(
    model="TwoStageDifferentialOpamp",
    description="A two-stage differential opamp (first stage: common-source with an active load and a tail current, second stage: common-source with an active load)",
    inputnode='Vinp, Vinn, Vbias1, Vbias2, Vbias3',
    outputnode='Voutp, Vout'
)

ClockDataRecovery = SUBMODEL(
    model="ClockDataRecovery",
    description="A clock and data recovery circuit consisting of four key components: a phase detector (PD), loop filter (LF), voltage-controlled oscillator (VCO), and data recovery unit. The PD detects phase differences between input data and the VCO clock, the LF converts phase errors into a control voltage, the VCO generates an adjustable clock signal, and the recovery unit samples data using the synchronized clock.",
    inputnode='DataIn, Vctrl_Init (initial VCO control voltage), VDD, VSS',
    outputnode='RecoveredClk, RecoveredData'
)

