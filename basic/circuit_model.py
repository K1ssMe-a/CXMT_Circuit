from dataclasses import dataclass, asdict
import os
import json

def read_file(file_path):
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except:
        pass


@dataclass
class CIRCUIT_MODEL:
    model_name: str = None
    model_description: str = None

    inputnode: str = None
    outputnode: str = None

    parameter: str = None
    parameter_description: str = None
    
    netlist: str = None

    testcode: list[str] = None
    testDescription: list[str] = None

    submodel_names: list[str] = None

    def __post_init__(self):
        self.__read_netlist()

    def get_replacement(self):
        replacement = {
            'Model': self.model_name,
            'Description': self.model_description,
            'InputNode': self.inputnode,
            'OutputNode': self.outputnode,
            'Parameter': self.parameter,
            'Parameter_Des': self.parameter_description,
            'ModelCode': self.netlist,
        }
        return replacement
    
    def __read_netlist(self):
        content = read_file(f'./model_json/{self.model_name}.py')
        if content != None:
            self.netlist = content

    def save_model_json(self):
        model_path = f'./model_json/{self.model_name}.json'
        try:
            model_dict = asdict(self)
            with open(model_path, 'w') as file:
                json.dump(model_dict, file, indent=4)
            # print(f"Model saved successfully to {model_path}")
        except Exception as e:
            print(f"Failed to save model: {e}")

    @staticmethod
    def load_model_json(model_path: str):
        try:
            with open(model_path, 'r') as file:
                model_dict = json.load(file)
                model = CIRCUIT_MODEL()
                model.__dict__.update(model_dict)
            # print(f"Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"Failed to load model: {e}")
            return None


class MODEL_SET:
    def __init__(self):
        self.all_models: dict = None
        self.load_all_models('./model_json')

    def save_all_models(self, json_path: str):
        for key in self.all_models:
            self.all_models[key].save_model_json

    def load_all_models(self, json_path: str):
        try:
            for filename in os.listdir(json_path):
                if filename.endswith('.json'):
                    filepath = os.path.join(json_path, filename)
                    model = CIRCUIT_MODEL.load_model_json(filepath)
                    if model:
                        model_key = os.path.splitext(filename)[0]
                        self.all_models[model_key] = model
            #print(f"Loaded {len(self.all_models)} models from {json_path}")
        except Exception as e:
            print(f"Error loading models from directory: {e}")