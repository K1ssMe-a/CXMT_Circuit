import sys
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import matplotlib.pyplot as plt
import numpy as np
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from modules.TwoStageOpamp import TwoStageOpamp


def simulate_two_stage_opamp():
    circuit = Circuit('Two Stage Opamp Test')

    # 创建运算放大器实例
    circuit.subcircuit(TwoStageOpamp(
        diff_nmos_width=15e-6, 
        diff_pmos_width=30e-6,
        cs_nmos_width=25e-6, 
        cs_pmos_width=25e-6,
        channel_length=0.18e-6,
        compensation_capacitor=2e-12, 
        compensation_resistor=10e3
    ))
    
    # 实例化运放并连接
    circuit.X('Opamp', 'TwoStageOpamp', 'Vinp', 'Vinn', 'Vbias1', 'Vbias2', 'Vbias3', 'Vout', 'VDD', 'GND')

    # 设置输入信号 - 添加AC分析输入源
    circuit.SinusoidalVoltageSource('Vin', 'Vinp', circuit.gnd, amplitude=0.5@u_V)
    
    # 设置偏置电压
    circuit.V('vdd', 'VDD', circuit.gnd, 5@u_V)
    circuit.V('Vbias1', 'Vbias1', 'GND', 1.2@u_V)
    circuit.V('Vbias2', 'Vbias2', 'GND', 1.2@u_V)
    circuit.V('Vbias3', 'Vbias3', 'GND', 1.2@u_V)
    
    # 连接反相输入端到地（开环配置）
    circuit.R('GND_connect', 'Vinn', circuit.gnd, 1@u_Ohm)  # 小电阻确保DC路径
    
    # 添加负载电容
    circuit.C('Load', 'Vout', circuit.gnd, 1@u_pF)
    
    # 添加输出负载电阻
    circuit.R('Load', 'Vout', circuit.gnd, 100@u_kOhm)

    # 仿真设置（AC分析）
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=1@u_Hz,  # 更低的起始频率
                           stop_frequency=100@u_MHz, # 更高的截止频率
                           number_of_points=100, 
                           variation='dec')

    # 获取频率数据和输出数据
    frequency = np.array(analysis.frequency)
    vout = np.array(analysis['Vout'])
    
    # 计算增益（dB）和相位（度）
    gain = 20 * np.log10(np.abs(vout))
    phase = np.angle(vout, deg=True)
    
    # 计算相位裕度（找到0dB频率点）
    unity_gain_freq_index = np.argmax(gain < 0)
    if unity_gain_freq_index > 0:
        phase_margin = phase[unity_gain_freq_index] + 180  # 因为相位从-180开始
        if phase_margin < 0:
            phase_margin += 360
    else:
        phase_margin = None
    
    # 计算直流增益
    dc_gain = gain[0] if len(gain) > 0 else 0

    # 绘制波特图
    plt.figure(figsize=(12, 8))
    
    # 增益图
    plt.subplot(2, 1, 1)
    plt.semilogx(frequency, gain, 'b-', linewidth=2)
    plt.title('Two-Stage Opamp Bode Plot')
    plt.ylabel('Gain (dB)')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # 标记直流增益
    plt.annotate(f'DC Gain: {dc_gain:.1f} dB', 
                xy=(10, dc_gain), 
                xytext=(100, dc_gain - 10),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    # 标记相位裕度
    if phase_margin is not None and unity_gain_freq_index > 0:
        unity_gain_freq = frequency[unity_gain_freq_index]
        plt.plot(unity_gain_freq, 0, 'ro', markersize=8)
        plt.annotate(f'UGF: {unity_gain_freq/1e6:.2f} MHz\nPM: {phase_margin:.1f}°', 
                    xy=(unity_gain_freq, 0), 
                    xytext=(unity_gain_freq*10, -20),
                    arrowprops=dict(facecolor='red', shrink=0.05))

    # 相位图
    plt.subplot(2, 1, 2)
    plt.semilogx(frequency, phase, 'g-', linewidth=2)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (degrees)')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # 添加-180度参考线
    plt.axhline(y=-180, color='r', linestyle='--', alpha=0.7)
    
    # 标记相位裕度位置
    if phase_margin is not None and unity_gain_freq_index > 0:
        plt.plot(unity_gain_freq, phase[unity_gain_freq_index], 'ro', markersize=8)
        plt.annotate(f'{phase[unity_gain_freq_index]:.1f}°', 
                    xy=(unity_gain_freq, phase[unity_gain_freq_index]), 
                    xytext=(unity_gain_freq*0.1, phase[unity_gain_freq_index] + 20))

    plt.tight_layout()
    plt.savefig('opamp_bode_plot.png', dpi=300)
    plt.show()
    
    # 打印关键参数
    print("\nOpamp Performance Summary:")
    print(f"DC Gain: {dc_gain:.1f} dB")
    if phase_margin is not None:
        print(f"Unity Gain Frequency: {unity_gain_freq/1e6:.2f} MHz")
        print(f"Phase Margin: {phase_margin:.1f}°")
    
    # 寻找-3dB带宽
    bandwidth_index = np.argmax(gain < (dc_gain - 3))
    if bandwidth_index > 0:
        bandwidth = frequency[bandwidth_index]
        print(f"-3dB Bandwidth: {bandwidth/1e3:.2f} kHz")
    
    return analysis


if __name__ == '__main__':
    analysis = simulate_two_stage_opamp()