import json
import os
import random
import sys
from datetime import datetime

def generate_tool_code():
    return str(random.randint(100000, 999999))

def generate_random_tool():
    # Common diameters in inches
    common_diameters = [0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0, 1.125, 1.25, 1.375, 1.5, 1.625, 1.75, 1.875, 2.0, 2.125, 2.25, 2.375, 2.5, 2.625, 2.75, 2.875, 3.0]
    
    diameter = round(random.choice(common_diameters), 4)
    flutes = random.randint(2, 6)
    length = round(random.uniform(3.0, 8.0), 4)
    cutlength = round(random.uniform(0.1, 0.6) * length, 4)
    ipt_min = round(random.uniform(0.0005, 0.02), 4)
    ipt_max = min(round(ipt_min * random.uniform(1.0, 5.0), 4), 0.02)
    sfm_min = round(random.uniform(50, 1000), 4)
    sfm_max = min(round(sfm_min * random.uniform(1.0, 3.0), 4), 1000)
    indexable = random.choice([True, False])
    coolant = random.choice([True, False])
    air = random.choice([True, False])
    cutcom = random.choice([True, False])

    return {
        generate_tool_code(): {
            "type": "endmill",
            "diameter": diameter,
            "flutes": flutes,
            "length": length,
            "cutlength": cutlength,
            "ipt": {"min": ipt_min, "max": ipt_max},
            "sfm": {"min": sfm_min, "max": sfm_max},
            "indexable": indexable,
            "coolant": coolant,
            "air": air,
            "cutcom": cutcom,
        }
    }

def generate_tools_list(tool_count):
    tools_list = [generate_random_tool() for _ in range(tool_count)]
    return tools_list

def generate_file_name():
    # Specify the path to the cuttingtools folder
    cuttingtools_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cuttingtools')

    # Create the cuttingtools folder if it doesn't exist
    os.makedirs(cuttingtools_folder, exist_ok=True)

    # Generate the file name based on the current date and time
    current_datetime = datetime.now().strftime("%m-%d-%y_%I%M%S%p").lower()
    file_name = os.path.join(cuttingtools_folder, f"{current_datetime}.json")

    return file_name

def main():
    tool_count = 20
    
    tools_list = generate_tools_list(tool_count)

    # Save the generated tools to a new JSON file with a dynamic name
    file_name = generate_file_name()
    with open(file_name, "w") as json_file:
        json.dump(tools_list, json_file, indent=2)

    print(f"{tool_count} new tools added to the new JSON file: {file_name}")

if __name__ == "__main__":
    main()
