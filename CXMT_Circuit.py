import re
import sys
import subprocess
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from basic.LLM_Interface import KIMI, DeepSeek_R1
from basic.submodel import *
import os
import pyperclip


prompt_paths = {
    'Generate_Circuit' : './prompts/circuit_generate.md',
    'Check_Promblems' : './prompts/check_problems.md',
    'Generate_TopCircuit' : './prompts/topcircuit_generate.md',
    'Submodule_Connect' : './prompts/submodule_connect.md'
}


LLM_model = DeepSeek_R1

def generate_prompt(file_path: str, replacement: dict) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        for key, value in replacement.items():
            if value != None:
                placeholder = f"[{key}]"
                content = content.replace(placeholder, value)
        return content
    except Exception as e:
        print(f"Error: {e}")  # 打印具体异常信息
        raise  # 重新抛出异常，或返回默认值
   
def add_submodule(message: str, module_list: list[SUBMODEL]):
    for i in range(len(module_list)):
        message += f"\n\n##SubModel {i+1}\n"
        message += f"Model: {module_list[i].model}"
        message += f"Description: {module_list[i].description}"
        message += f"Input Nodes: {module_list[i].inputnode}"
        message += f"Output Nodes: {module_list[i].outputnode}"
        message += f"Parameters: {module_list[i].parameter}"
    return message


def extract_submodels(message: str) -> list[SUBMODEL]:
    pattern = re.compile(
        r'##\s+Module\s+\d+\s*\n'
        r'Model:\s*(.*?)\s*\n'
        r'Description:\s*(.*?)\s*\n'
        r'Input\s+Nodes:\s*(.*?)\s*\n'
        r'Output\s+Nodes:\s*(.*?)\s*(?=\n##|$)',
        re.DOTALL | re.IGNORECASE
    )
    submodels = []
    for m in pattern.finditer(message):
        model       = m.group(1).strip()
        description = m.group(2).strip()
        inputnode   = m.group(3).strip()
        outputnode  = m.group(4).strip()
        submodels.append(
            SUBMODEL(
                model=model,
                description=description,
                inputnode=inputnode,
                outputnode=outputnode
            )
        )
    return submodels


def extract_code(message: str, leader: str):
    pattern = rf'{leader}[^\n]*\s*```python(.*?)\s*```'
    matches = re.findall(pattern, message, re.DOTALL)
    
    code_blocks = [match.strip() for match in matches]
    
    return code_blocks


def run_python_file(file_path):
    result = subprocess.run(
        ['python', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    combined_output = result.stdout + result.stderr
    
    print(combined_output)
    
    return combined_output


def create_pyspice_topmodule(topmodule: SUBMODEL):
    prompt = generate_prompt(prompt_paths['Generate_TopCircuit'], topmodule.get_replacement())
    print(f"Get top circuit generation prompt:\n{prompt}")

    response = LLM_model.get_answer(prompt)
    print(f"Get response from {LLM_model.name}:\n{response}")

    submodel_list = extract_submodels(response)

    topology = extract_code(response, 'Topology')

    for submodel in submodel_list:
        create_pyspice_module(submodel)

    return submodel_list

def connect_submodules(topmodule: SUBMODEL, submodule_list: list[SUBMODEL]):
    prompt = generate_prompt(prompt_paths['Submodule_Connect'], topmodule.get_replacement())
    prompt = add_submodule(prompt, submodule_list)
    print(f"Get top circuit generation prompt:\n{prompt}")

    response = LLM_model.get_answer(prompt)
    print(f"Get response from {LLM_model.name}:\n{response}")


def create_pyspice_module(module: SUBMODEL):
    prompt = generate_prompt(prompt_paths['Generate_Circuit'], module.get_replacement())
    print(f"Get circuit generation prompt:\n{prompt}")

    response = LLM_model.get_answer(prompt)
    print(f"Get response from {LLM_model.name}:\n{response}")

    code_block = extract_code(response, "Code_Generation")
    parameter = extract_code(response, "Parameter_Explanation")
    module.modelcode = code_block
    module.parameter = parameter

    target_file = os.path.join("./modules", f"{module.model}.py")
    with open(target_file, "w") as f:
        f.write(code_block[0])

    print(f"Module code written to {target_file}")


def create_check_problems(module: SUBMODEL):
    prompt = generate_prompt(prompt_paths['Check_Promblems'], module.get_replacement())
    print(f"Get problem check prompt:\n{prompt}")

    response = LLM_model.get_answer(prompt)
    print(f"Get response from {LLM_model.name}:\n{response}")
    
    test_codes = extract_code(message=response, leader='Test_Item')
    for i in range(len(test_codes)):
        with open(f"./modules/{module.model}_Test{i+1:02d}.py", "w") as f:
            f.write(test_codes[i])


if __name__ == '__main__':

    # create_pyspice_module(OneStageAmplifer01)

    # create_check_problems(OneStageAmplifer01)

    # result = run_python_file('./modules/OneStageAmplifier01_Test02.py')

    submodule_list = create_pyspice_topmodule(ClockDataRecovery)
    connect_submodules(ClockDataRecovery, submodule_list)


