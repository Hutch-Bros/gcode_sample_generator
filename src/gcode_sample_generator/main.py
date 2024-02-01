import os
import json
import random
from datetime import datetime
from sequence import SeqGenerator


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
        self.fileid = random.randint(1000000, 9999999)
        self.partnum = self._get_partnum()
        self.machineid = self._get_machineid()
        self.revisionid = 1.0
        self.revisiondate = datetime.now().strftime("%m-%d-%Y")
        self.revisiontime = datetime.now().strftime("%I:%M:%S%p").lower()
        self.controlleros = self._get_controlleros()
        self.tcodes = self._get_tcodes()
        self.number_of_sequences = self._get_number_of_sequences()
        self.gcode = self._generate_gcode()

    def _get_partnum(self) -> str:
        """
        Generates a random part number consisting of a three-digit number, a middle letter,
        a four-digit number, and a dash followed by a single-digit number.

        Returns:
            str: The randomly generated part number.
        """
        first_3_nums = random.randint(100, 999)
        middle_letter = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
        last_4_nums = random.randint(1000, 9999)
        dash_num = random.randint(1, 9)

        return f"{first_3_nums}{middle_letter}{last_4_nums}-{dash_num}"
    
    def _get_machineid(self) -> int:
        """
        Generates a random machine identifier (ID) from a predefined list. This ID represents 
        a unique identifier for a CNC machine in a machining environment.

        Returns:
            int: A randomly selected machine ID, which could be either 1, 2, or 3.
        """
        return random.choice([1, 2, 3])

    def _get_controlleros(self) -> str:
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
        max_sequences = len(self.tcodes) + random.randint(0, 5)
        return random.randint(len(self.tcodes), max_sequences)
    
    def _nblock_prefix(self, gcodes) -> str:
        """
        Prepends each G-code command in the provided list with an N-block number.

        This method iterates through the given list of G-code commands and prefixes each command with an N-block number. The N-block number is generated sequentially, starting from the current value of `self._last_nblock` and incrementing it for each command. 

        The purpose of the N-block numbering is to provide a unique identifier for each line of G-code, which can be useful for debugging or referencing specific commands within the CNC program.

        Args:
            gcodes (List[str]): A list of G-code commands to be prefixed with N-block numbers.

        Returns:
            List[str]: The list of G-code commands, each prefixed with a unique N-block number.

        Note:
            This method modifies `self._last_nblock` by incrementing it with each command processed. The initial value of `self._last_nblock` should be set appropriately before calling this method.
        """
        for i in range(len(gcodes)):
            self._last_nblock += 1 
            gcodes[i] = f'N{self._last_nblock} {gcodes[i]}'
        return gcodes
    
    def _add_line_breaks(self, gcodes) -> str:
        """
        Adds line breaks to the given list of G-code commands.

        This method iterates through the given list of G-code commands and appends a line break character to each command. The line break character is used to separate each command and ensure that the G-code program is formatted correctly.

        Args:
            gcodes (List[str]): A list of G-code commands to be formatted with line breaks.

        Returns:
            str: A string containing the G-code commands, each separated by a line break.

        """
        return '\n'.join(gcodes)
    
    def _generate_file_start(self) -> list:

        match self.controlleros:
            case "grbl":
                # startup codes
                gcode_file_start = [
                    "%",
                ]
                return gcode_file_start
            case "fanuc":
                return None
            case "siemens":
                return None
            case _:
                return None
    
    def _generate_header(self) -> str:
        """
        Generates a header string for CNC machine programming based on the specified controller OS.

        This method constructs the header by aggregating metadata and startup codes specific to the controller OS. The metadata includes details like file ID, part number, file number, revision ID, revision date, revision time, author ID, machine ID, and controller OS. The startup codes are tailored to the controller OS used in the CNC machine.

        For 'grbl' controllers, the method includes specific program start and machine start sequences. For 'fanuc' and 'siemens' controllers, this method currently returns None, indicating a placeholder for future implementation.

        The method uses an internal counter to track the last NBlock sequence number after adding program starts.

        Returns:
            str: A string containing the formatted header for the CNC program, tailored to the specific controller OS. Returns None for 'fanuc', 'siemens', and other unspecified controller OS types.

        Note:
            This method relies on internal attributes such as fileid, partnum, revisionid, revisiondate, revisiontime, and controlleros, which should be set prior to calling this method.
        """

        header_meta = [
                    f"(@@ meta_fileid = {self.fileid})",
                    f"(@@ meta_partnum = {self.partnum})",
                    f"(@@ meta_filenum = 1)",
                    f"(@@ meta_revisionid = {self.revisionid})",
                    f"(@@ meta_revisiondate = {self.revisiondate})",
                    f"(@@ meta_revisiontime = {self.revisiontime})",
                    f"(@@ meta_authorid = 1)",
                    f"(@@ meta_machineid = 1)",
                    f"(@@ meta_controlleros = {self.controlleros})",
                ]

        match self.controlleros:
            case "grbl":
                # startup codes
                startup_codes = [
                    "G90 G94 G17 G49 G40 G80",
                    "G20",
                    "G28 G91 Z0.",
                    "G90",
                ]
                return header_meta + startup_codes
            case "fanuc":
                return None
            case "siemens":
                return None
            case _:
                return None
    
    def _generate_sequences(self) -> str:

        seqno_tools = list(self.tcodes.keys())

        # If there are more sequences than tcodes, assign remaining sequences randomly
        while len(seqno_tools) < self.number_of_sequences:
            seqno_tools.append(random.choice(list(self.tcodes.keys())))

        seq_gcode = []
        seqno = 1
        for seqno_tool in seqno_tools:
            seqgenerator = SeqGenerator(tcodeid=seqno_tool, tcode_params=self.tcodes[seqno_tool])
            seq_gcode.append(f"(@@ seq_start = {seqno})")
            seq_gcode.extend(seqgenerator.generate_random_motion())
            seq_gcode.append(f"(@@ seq_end = {seqno})")
            seqno += 1

        return seq_gcode
    
    def _generate_gcode(self):
        
        no_nblock = self._generate_file_start()
        with_nblock = self._generate_header() + self._generate_sequences() + ["M30"]

        start_block_num = len(no_nblock) + 1

        # Using list comprehension to add the prefix
        nblocks_added = [f"N{start_block_num + i} {item}" for i, item in enumerate(with_nblock)]

        return no_nblock + nblocks_added + ["%"]
    
    def print_summary(self):
        """
        Prints a summary of the current state of the class attributes. This includes the
        controller operating system, machine identifier, and a summary of the tool codes.
        """
        print("-----GCode Sample Generator Summary-----")
        print(f"Machine ID: {self.machineid}")
        print(f"Controller OS: {self.controlleros}")
        print(f"Number of Sequences: {self.number_of_sequences}")
        print(f"Tool Codes: {len(self.tcodes)}")
        for tcode, details in self.tcodes.items():
            print(f"  {tcode}")
        
def output_gcode(gcode):
    """
    Outputs the generated G-code to a file.

    This function writes the provided G-code to a file with a filename based on the current date and time. The file is saved in the 'output' directory within the current working directory.

    Args:
        gcode (str): The G-code to be written to the file.
    """
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".nc"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(gcode))

    print(f"Generated G-code has been saved to: {file_path}")


def run():

    generated_gcode = GCodeSampleGenerator()
    output_gcode(generated_gcode.gcode)

if __name__ == "__main__":
    run()
