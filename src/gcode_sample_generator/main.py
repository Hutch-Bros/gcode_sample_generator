import os
import json
import random

def load_sample_tools_json():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cuttingtools', 'sample_tools.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
    
def select_random_keys(json_data, num_keys=3):
    keys_list = list(json_data.keys())
    keys = random.sample(keys_list, min(num_keys, len(keys_list)))
    selected_data = {key: json_data[key] for key in keys}
    return selected_data

def run():
    cutting_tools = select_random_keys(load_sample_tools_json())

    return None

if __name__ == "__main__":
    run()
