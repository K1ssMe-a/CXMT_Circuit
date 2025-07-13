import sys
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from modules.Inverter01 import Inverter01
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

def test_inverter_static():
    circuit = Circuit('Inverter Static Test')
    
    vdd = circuit.V('dd', 'VDD', circuit.gnd, 5@u_V)
    circuit.subcircuit(Inverter01())
    circuit.X('1', 'Inverter01', 'Vin', 'Vout', circuit.gnd, 'VDD')
    
    input_source = circuit.V('in', 'Vin', circuit.gnd, 0@u_V)
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    test_conditions = [
        {'Vin': 0.0, 'expected_Vout': 5.0}, 
        {'Vin': 5.0, 'expected_Vout': 0.0} ]
    
    tolerance = 0.05
    
    all_passed = True
    detailed_results = []
    
    for test in test_conditions:
        input_source.dc_value = test['Vin']@u_V
        
        analysis = simulator.operating_point()
        
        vout = analysis['Vout'].as_ndarray().item()
        expected = test['expected_Vout']
        
        expected_min = expected - vdd.dc_value * tolerance
        expected_max = expected + vdd.dc_value * tolerance
        
        in_range = expected_min <= vout <= expected_max
        
        detailed_results.append({
            'Vin': test['Vin'],
            'Vout': vout,
            'expected': expected,
            'in_range': in_range,
            'min': expected_min,
            'max': expected_max
        })
        
        if not in_range:
            all_passed = False
    
    print("\nDetailed Test Results:")
    print("Vin (V)\tVout (V)\tExpected (V)\tMin (V)\tMax (V)\tStatus")
    for result in detailed_results:
        status = "PASS" if result['in_range'] else "FAIL"
        print(f"{result['Vin']:.1f}\t{result['Vout']:.3f}\t\t{result['expected']:.1f}\t\t{result['min']:.2f}\t{result['max']:.2f}\t{status}")
    
    if all_passed:
        print("\nTest_Passed: All conditions met within tolerance")
    else:
        print("\nTest_Failed: One or more conditions outside tolerance range")
    
    return all_passed

if __name__ == "__main__":
    test_inverter_static()