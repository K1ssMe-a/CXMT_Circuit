import sys
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)
 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from modules.Inverter01 import Inverter01
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
 
def test_inverter_threshold_condition():
    # Create circuit
    circuit = Circuit('Inverter Threshold Condition Test')
    
    # Set power supply voltage
    vdd_value = 5.0
    vdd = circuit.V('dd', 'VDD', circuit.gnd, vdd_value@u_V)
    
    # Add inverter subcircuit
    circuit.subcircuit(Inverter01(
        nmos_width=0.5e-6,
        pmos_width=1e-6,
        channel_length=0.18e-6,
        load_capacitance=10e-15
    ))
    circuit.X('inv', 'Inverter01', 'Vin', 'Vout', circuit.gnd, 'VDD')
    
    # Add input voltage source for DC sweep
    input_source = circuit.V('in', 'Vin', circuit.gnd, 0@u_V)
    
    # Setup simulator
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    
    # Perform DC sweep analysis
    print("Running DC sweep analysis...")
    analysis = simulator.dc(Vin=slice(0, vdd_value, 0.01))  # 0V to VDD, 0.01V steps
    
    # Extract results
    vin = np.array(analysis.sweep)
    vout = np.array(analysis['Vout'])
    
    # Define MOSFET threshold voltages
    vth_nmos = 0.5  # NMOS threshold voltage
    vth_pmos = vdd_value - 0.5  # Effective PMOS threshold (VDD - |Vth_p|)
    
    # Calculate actual threshold voltage (Vin where Vout = Vin)
    diff = vout - vin
    idx = np.argwhere(np.diff(np.sign(diff)))[0][0]
    x1, x2 = vin[idx], vin[idx+1]
    y1, y2 = diff[idx], diff[idx+1]
    actual_threshold = x1 - y1 * (x2 - x1) / (y2 - y1)
    
    # Analyze behavior in threshold regions
    # 1. When Vin < NMOS threshold, Vout should be near VDD
    low_vin_mask = vin < vth_nmos
    vout_low_vin = vout[low_vin_mask]
    
    # 2. When Vin > PMOS threshold, Vout should be near 0V
    high_vin_mask = vin > vth_pmos
    vout_high_vin = vout[high_vin_mask]
    
    # Set tolerance
    tolerance = 0.05 * vdd_value  # 5% tolerance
    
    # Check test results
    test_passed = True
    failure_reasons = []
    
    # Check low input voltage region
    if not np.all(vout_low_vin >= (vdd_value - tolerance)):
        test_passed = False
        min_vout = np.min(vout_low_vin)
        failure_reasons.append(
            f"FAIL: When Vin < {vth_nmos}V, output should be high (~{vdd_value}V), "
            f"but min Vout = {min_vout:.3f}V"
        )
    
    # Check high input voltage region
    if not np.all(vout_high_vin <= tolerance):
        test_passed = False
        max_vout = np.max(vout_high_vin)
        failure_reasons.append(
            f"FAIL: When Vin > {vth_pmos:.2f}V, output should be low (~0V), "
            f"but max Vout = {max_vout:.3f}V"
        )
    
    # Check transition region monotonicity
    transition_region = (vin >= vth_nmos) & (vin <= vth_pmos)
    if not np.all(np.diff(vout[transition_region]) < 0):
        test_passed = False
        failure_reasons.append("FAIL: Output voltage not monotonically decreasing in transition region")
    
    # Print detailed test report
    print("\n" + "="*60)
    print("Inverter Threshold Voltage Condition Test Results")
    print("="*60)
    
    print(f"Test Parameters:")
    print(f"  VDD = {vdd_value}V")
    print(f"  NMOS Threshold = {vth_nmos}V")
    print(f"  PMOS Threshold = {vth_pmos:.2f}V")
    print(f"  Actual Threshold (Vin where Vout=Vin) = {actual_threshold:.3f}V")
    print(f"  Expected Threshold (VDD/2) = {vdd_value/2:.3f}V")
    print(f"  Tolerance = ±{tolerance:.2f}V")
    
    print("\nRegion Checks:")
    print(f"1. Low Input Region (Vin < {vth_nmos}V):")
    print(f"   Expected Vout > {vdd_value - tolerance:.2f}V")
    print(f"   Actual Min Vout = {np.min(vout_low_vin):.3f}V")
    
    print(f"\n2. High Input Region (Vin > {vth_pmos:.2f}V):")
    print(f"   Expected Vout < {tolerance:.2f}V")
    print(f"   Actual Max Vout = {np.max(vout_high_vin):.3f}V")
    
    print("\n3. Transition Region Monotonicity:")
    transition_vout = vout[transition_region]
    monotonic = np.all(np.diff(transition_vout) < 0)
    print(f"   Monotonic decreasing: {'Yes' if monotonic else 'No'}")
    
    print("\n" + "-"*60)
    if test_passed:
        print("\nTest_Passed: All threshold voltage conditions met")
    else:
        print("\nTest_Failed: One or more threshold conditions failed")
        for reason in failure_reasons:
            print(f"  • {reason}")
    
    return test_passed, vin, vout, vdd_value, actual_threshold
 
if __name__ == "__main__":
    test_result, vin, vout, vdd_value, actual_threshold = test_inverter_threshold_condition()
    
    # Create plot
    plt.figure(figsize=(10, 8), dpi=100)
    plt.plot(vin, vout, 'b-', linewidth=2.5, label='Voltage Transfer Characteristic')
    
    # Plot actual threshold point
    plt.plot(actual_threshold, actual_threshold, 'ro', markersize=8, 
             label=f'Actual Threshold ({actual_threshold:.3f}V)')
    
    # Plot expected threshold line
    expected_threshold = vdd_value / 2
    plt.axvline(x=expected_threshold, color='g', linestyle='--', linewidth=1.5, 
                label=f'Expected Threshold ({expected_threshold:.3f}V)')
    
    # Plot VDD line
    plt.axhline(y=vdd_value, color='k', linestyle=':', alpha=0.7, label=f'VDD ({vdd_value}V)')
    
    # Plot y=x reference line
    plt.plot([0, vdd_value], [0, vdd_value], 'm--', alpha=0.6, linewidth=1.2, label='Vout = Vin')
    
    # Set plot properties
    plt.title('Inverter Voltage Transfer Characteristic', fontsize=14, fontweight='bold')
    plt.xlabel('Input Voltage (Vin) [V]', fontsize=12)
    plt.ylabel('Output Voltage (Vout) [V]', fontsize=12)
    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.axis([0, vdd_value, 0, vdd_value * 1.05])
    
    # Set minor ticks
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.1))
    plt.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
    
    # Add annotations
    plt.text(0.05, vdd_value * 0.95, 'PMOS Active\nVout ≈ VDD', 
             fontsize=10, verticalalignment='top')
    plt.text(vdd_value * 0.85, 0.1, 'NMOS Active\nVout ≈ 0V', 
             fontsize=10, horizontalalignment='right')
    plt.text(actual_threshold + 0.1, actual_threshold - 0.2, 
             f'Threshold Point\nVout = Vin = {actual_threshold:.3f}V', 
             fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    # Add legend
    plt.legend(loc='upper right', frameon=True, shadow=True)
    
    # Save and show plot
    plt.tight_layout()
    plt.savefig('inverter_threshold_characteristic.png', dpi=150)
    print("\nPlot saved as 'inverter_threshold_characteristic.png'")
    plt.show()