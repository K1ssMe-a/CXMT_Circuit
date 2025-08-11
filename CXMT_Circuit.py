import re
import sys
import subprocess
from pathlib import Path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from basic.LLM_interface import KIMI, DeepSeek_R1
from basic.circuit_model import *
import os

all_models = load_all_models()

prompt_paths = {
    'Generate_Circuit' : './prompts/circuit_generate.md',
    'Check_Promblems' : './prompts/check_problems.md',
    'Requirement_Parsing' : './prompts/requirement_parsing.md',
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
        print(f"Error: {e}") 
        raise
   
# def add_submodule(message: str, module_list: list[SUBMODEL]):
#     for i in range(len(module_list)):
#         message += f"\n\n##SubModel {i+1}\n"
#         message += f"Model: {module_list[i].model}"
#         message += f"Description: {module_list[i].description}"
#         message += f"Input Nodes: {module_list[i].inputnode}"
#         message += f"Output Nodes: {module_list[i].outputnode}"
#         message += f"Parameters: {module_list[i].parameter}"
#     return message



# def extract_code(message: str, leader: str):
#     pattern = rf'{leader}[^\n]*\s*```python(.*?)\s*```'
#     matches = re.findall(pattern, message, re.DOTALL)
    
#     code_blocks = [match.strip() for match in matches]
    
#     return code_blocks

def extract_code(text: str, segment_leader: str, code_leader: str):
    pattern = re.compile(
        r'###\s+' + re.escape(segment_leader) + r'\s*' + 
        r'```' + re.escape(code_leader) + r'\n(.*?)```',
        re.DOTALL
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

def extract_test_items(text: str):
    pattern = r'####\s+(Test_Item\s+\d+)(.*?)(?=#### Test_Item|\Z)'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    test_items = []
    test_descriptions = []    
    for match in matches:
        item_name = match.group(1).strip()
        item_content = match.group(2).strip()

        markdown_match = re.search(r'```markdown\n(.*?)```', item_content, re.DOTALL)
        markdown = markdown_match.group(1).strip() if markdown_match else None

        python_match = re.search(r'```python\n(.*?)```', item_content, re.DOTALL)
        python_code = python_match.group(1).strip() if python_match else None
        
        test_items.append(python_code)
        test_descriptions.append(markdown)
    
    return test_items, test_descriptions

def extract_submodels(message: str) -> list[CIRCUIT_MODEL]:
    pattern = re.compile(
        r'####\s+Module\s+\d+\s*\n'
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
            CIRCUIT_MODEL(
                model_name=model,
                model_description=description,
                inputnode=inputnode,
                outputnode=outputnode
            )
        )
    return submodels


# def run_python_file(file_path):
#     result = subprocess.run(
#         ['python', file_path],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
    
#     combined_output = result.stdout + result.stderr
    
#     print(combined_output)
    
#     return combined_output




# def connect_submodules(topmodule: SUBMODEL, submodule_list: list[SUBMODEL]):
#     prompt = generate_prompt(prompt_paths['Submodule_Connect'], topmodule.get_replacement())
#     prompt = add_submodule(prompt, submodule_list)
#     print(f"Get top circuit generation prompt:\n{prompt}")

#     response = LLM_model.get_answer(prompt)
#     print(f"Get response from {LLM_model.name}:\n{response}")


def create_sub_circuit(model: CIRCUIT_MODEL):
    prompt = generate_prompt(prompt_paths['Generate_Circuit'], model.get_replacement())
    print(f"\n\n{prompt}")

    response = LLM_model.get_answer(prompt)
    print(f"## Get Response from {LLM_model.name}\n\n{response}")

    model.netlist = extract_code(response, "NetList Code", 'python')
    model.parameter_description = extract_code(response, "Parameter Explanation", 'markdown')



def create_check_problems(model: CIRCUIT_MODEL):
    prompt = generate_prompt(prompt_paths['Check_Promblems'], model.get_replacement())
    print(f"\n\n{prompt}")

    response = LLM_model.get_answer(prompt)
    print(f"## Get response from {LLM_model.name} \n\n{response}")
    
    model.testcode, model.testDescription = extract_test_items(response)


def create_requirement_parsing(topmodel: CIRCUIT_MODEL):
    prompt = generate_prompt(prompt_paths['Requirement_Parsing'], topmodel.get_replacement())
    print(f"\n\n{prompt}")

    response = LLM_model.get_answer(prompt)
    print(f"## Get response from {LLM_model.name}\n\n{response}")

    submodel = extract_submodels(response)

    submodel_names = [ model.model_name for model in submodel ]
    topmodel.submodel_names = submodel_names
    
    for model in submodel:
        all_models[model.model_name] = model

if __name__ == '__main__':


    # create_pyspice_module(OneStageAmplifer01)

    # create_check_problems(OneStageAmplifer01)

    # result = run_python_file('./modules/OneStageAmplifier01_Test02.py')

    # submodule_list = create_pyspice_topmodule(ClockDataRecovery)
    # connect_submodules(ClockDataRecovery, submodule_list)

    # create_sub_circuit(all_models['OneStageAmplifier'])
    # create_check_problems(all_models['OneStageAmplifier'])

    create_requirement_parsing(all_models['TwoStageDifferentialOpamp'])

    all_models['TwoStageDifferentialOpamp'].save_model_json()

    # ClockDataRecovery.save_model_json()
