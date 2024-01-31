import os
import json
import random
from motion import Motion


class GCodeSampleGenerator:
    """
    A class dedicated to generating G-code samples for CNC (Computer Numerical Control) machining. 
    This class simulates the creation of G-code by selecting random controller operating systems, 
    machine identifiers, and tool codes typically used in CNC operations.

    Attributes:
        controller_os (str): The controller operating system used in CNC machining.
        machineid (int): An identifier for the CNC machine.
        tcodes (dict): A collection of tool codes representing different cutting tools.
    """
    def __init__(self):
        """
        Initializes a new instance of GCodeSampleGenerator. This method automatically sets up
        the controller operating system, machine identifier, and tool codes for the instance
        by invoking respective private methods.
        """
        self.machineid = self._get_machineid()
        self.controller_os = self._get_controller_os()
        self.tcodes = self._get_tcodes()
        self.number_of_sequences = self._get_number_of_sequences()

    def _get_machineid(self) -> int:
        """
        Generates a random machine identifier (ID) from a predefined list. This ID represents 
        a unique identifier for a CNC machine in a machining environment.

        Returns:
            int: A randomly selected machine ID, which could be either 1, 2, or 3.
        """
        return random.choice([1, 2, 3])

    def _get_controller_os(self) -> str:
        """
        Selects a random controller operating system from a predefined list. This simulates 
        the different types of operating systems used in CNC controllers.

        Returns:
            str: A randomly selected controller operating system, either 'fanuc' or 'siemens'.
        """
        return random.choice(["grbl"])
    
    def _get_tcodes(self) -> dict:
        """
        Loads a set of cutting tool codes from a JSON file and selects a random subset. This 
        method simulates the selection of different cutting tools used in CNC machining.

        Returns:
            dict: A dictionary containing a randomly selected subset of tool codes, 
            each represented as key-value pairs where the key is the tool code and the value is its details.
        """
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cuttingtools', 'sample_tools.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            all_tools = json.load(file) 

        # Create a weighted list
        weighted_choices = [2, 3, 4] * 10 + list(range(5, 21)) 

        # Use random.choice to pick a number from the weighted list
        num_keys = min(random.choice(weighted_choices), len(all_tools))

        keys = random.sample(list(all_tools.keys()), num_keys)
        return {key: all_tools[key] for key in keys}
    
    def _get_number_of_sequences(self) -> int:
        """
        Generates a random number of sequences for the G-code sample. This method simulates the 
        selection of different sequences that are used in CNC machining.

        Returns:
            int: A randomly selected number of sequences, which could be between 1 and 10.
        """
        return random.randint(1, len(self.tcodes))
    
    def print_summary(self):
        """
        Prints a summary of the current state of the class attributes. This includes the
        controller operating system, machine identifier, and a summary of the tool codes.
        """
        print("-----GCode Sample Generator Summary-----")
        print(f"Machine ID: {self.machineid}")
        print(f"Controller OS: {self.controller_os}")
        print(f"Number of Sequences: {self.number_of_sequences}")
        print(f"Tool Codes: {len(self.tcodes)}")
        for tcode, details in self.tcodes.items():
            print(f"  {tcode}")
        

def run():

    # Plan: 
    # 1. Load the sample tools JSON file
    # 2. Select a random number of tools
    # 3. Select a random number of sequences
    # 4. Generate motion for each sequence. Use each tool once, and then repeat if # of tools hasn't been met. 
    # 5. Generate a random file name
    # 6. Save the generated motion to a new G-code file

    gcode = GCodeSampleGenerator()
    gcode.print_summary()

if __name__ == "__main__":
    run()
