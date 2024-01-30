import random

class Motion:
    """
    Represents a motion controller for machining operations.

    This class provides functionalities to generate G-code sequences for different
    shapes (e.g., square, oval) with configurable parameters. It initializes with 
    specific settings for the controller's operating system and tool code (tcode), 
    and calculates random values for revolutions per minute (RPM), feedrate, and size 
    based on the tcode.

    Attributes:
        controller_os (str): The type of operating system used by the controller.
        tcode (dict): A dictionary containing tool-specific code data, including 
                      parameters for RPM and feedrate calculations.
        rpm (float): Calculated random RPM value for the operation.
        feedrate (float): Calculated random feedrate for the operation.
        size (int): A random size value used in shape generation.

    Methods:
        calc_random_rpm: Calculates a random RPM based on the tcode's SFM range and diameter.
        calc_random_feedrate: Calculates a random feedrate based on the tcode's IPT range and RPM.
        cutter_compensation: Determines cutter compensation (if any) based on the tool's capabilities.
        square: Generates a G-code sequence for a square shape with configurable parameters.
        oval: Generates a G-code sequence for an oval shape with configurable parameters.
    """
    APPROACH = 1.0
    RETRACT = 0.250

    def __init__(self, controller_os: str, tcode: dict) -> None:
        """
        Initialize the Motion object with controller operating system, tool code data,
        and randomly calculated parameters.

        Args:
            controller_os (str): The operating system of the controller.
            tcode (dict): A dictionary containing tool-specific code data.

        Attributes:
            controller_os (str): Operating system of the controller.
            tcode (dict): Tool-specific code data.
            rpm (float): Randomly calculated RPM.
            feedrate (float): Randomly calculated feedrate.
            size (int): Randomly determined size value for operations.
        """
        self.controller_os = controller_os
        self.tcode = tcode
        
    def _calc_random_rpm(self) -> float:
        """
        Calculates a random RPM (Rotations Per Minute) based on the given surface feet per minute (SFM) range and diameter.

        Args:
            sfm_min (float): The minimum surface feet per minute.
            sfm_max (float): The maximum surface feet per minute.
            diameter (float): The diameter of the object.

        Returns:
            float: The calculated random RPM.

        """
        sfm = random.uniform(self.tcode["sfm"]["min"], self.tcode["sfm"]["max"])
        return round(sfm * 3.82 / self.tcode["diameter"], 2)
    
    def _calc_random_feedrate(self, rpm) -> float:
        """
        Calculates a random feedrate based on the given inputs.

        Args:
            ipt_min (float): The minimum inches per tooth (IPT) value.
            ipt_max (float): The maximum inches per tooth (IPT) value.
            rpm (float): The revolutions per minute (RPM) value.

        Returns:
            float: The calculated feedrate.

        """
        ipt = random.uniform(self.tcode["ipt"]["min"], self.tcode["ipt"]["max"])
        return round(ipt * rpm, 2)

    def _cutter_compensation(self) -> str:
        """
        Determines whether (and how) to apply cutter compensation.

        This method decides whether to apply cutter compensation based on the tool's capability.
        If the tool supports cutter compensation (cutcom), it randomly selects either no compensation,
        left compensation (G41), or right compensation (G42). The choice is made with equal probability.

        Returns:
            str: A G-code command for cutter compensation ('G41' for left, 'G42' for right),
                or an empty string if no compensation is to be applied.

        """
        if self.tcode["cutcom"]:
            return random.choice([None, "G41", "G42"])
        return None
    
    def _square(self, size, cutcom, rpm, feedrate) -> str:
        """
        Generates a G-code sequence for creating a square with rounded corners.

        Returns:
            str: A string containing the complete G-code sequence for the operation.

        """
        corner_radius = size / 5

        print("---square---")

        # Define points for G-code
        points = [
            f"S{rpm} M3",  # Spindle on
            f"G0 X0 Y-{self.APPROACH + corner_radius} Z3.0",  # Point 1
            "G0 Z0.1",  # Point 2
            f"G1 Z0.0 F{round(feedrate * 1/random.randint(1,5), 2)}" # Point 3
            ]  
        
        if cutcom is not None:
            points.append(cutcom)

        points += [
            f"G1 Y-{corner_radius}",  # Point 4
            f"G2 X{corner_radius} Y0 I{corner_radius} J0",  # Point 5
            f"G1 X{size - corner_radius} Y0 F{feedrate}",  # Point 6
            f"G3 X{size} Y{corner_radius} I0 J{corner_radius}",  # Point 7
            f"G1 X{size} Y{size - corner_radius}",  # Point 8
            f"G3 X{size - corner_radius} Y{size} I-{corner_radius} J0",  # Point 9
            f"G1 X{corner_radius} Y{size}",  # Point 10
            f"G3 X0 Y{size - corner_radius} I0 J-{corner_radius}",  # Point 11
            f"G1 X0 Y{corner_radius}",  # Point 12
            f"G3 X{corner_radius} Y0 I{corner_radius} J0",  # Point 13
            f"G2 X{corner_radius + self.RETRACT} Y-{self.RETRACT} I0 J-{self.RETRACT}",  # Point 14
        ]

        # Turn off cutter compensation if it was used
        if cutcom is not None:
            points.append("G40")

        # Retract Z
        points.append("G0 Z3.0")

        return '\n'.join(points)
    
    def _oval(self, size, cutcom, rpm, feedrate) -> str:
        """
        Generates a G-code sequence for creating an oval with rounded ends.

        The oval is created by moving the cutter in a circular motion along the specified arc size.
        The size of the oval is determined by the 'size' attribute of the object.

        Args:
            cutcom (str): The cutter compensation value to be used. If None, no cutter compensation will be applied.

        Returns:
            str: A string containing the complete G-code sequence for the operation.

        """
        arc_size = size / 2

        print("---oval---")

        # Define points for G-code
        points = [
            f"S{rpm} M3",  # Spindle on
            f"G0 X-1.0 Y-2.0 Z3.0",  # Point 1
            "G0 Z0.1",  # Point 2
            f"G1 Z0.0 F{round(feedrate * 1/random.randint(1,5), 2)}" # Point 3
            ]  
        
        if cutcom is not None:
            points.append(cutcom)

        points += [
            f"G1 Y-1.0",  # Point 4
            f"G2 X0 Y0 I1.0 J0",  # Point 5
            f"G3 X{arc_size} Y{arc_size} I0 J{arc_size} F{feedrate}",  # Point 6
            f"G1 Y{arc_size + 1}", # Point 7
            f"G3 X0 Y{size + 1} I-{arc_size} J0",  # Point 8
            f"G3 X-{arc_size} Y{arc_size + 1} I0 J-{arc_size}",  # Point 9
            f"G1 Y{arc_size}",  # Point 10
            f"G3 X0 Y0 I{arc_size} J0",  # Point 11
            f"G2 X{self.RETRACT} Y-{self.RETRACT} I0 J-{self.RETRACT}"  # Point 12   
        ]

        # Turn off cutter compensation if it was used
        if cutcom is not None:
            points.append("G40")

        # Retract Z
        points.append("G0 Z3.0")

        return '\n'.join(points)
    
    def _triangle(self, size, cutcom, rpm, feedrate) -> str:
        print("---triangle---")
        return ""
    
    def generate_random_motion(self):
        """
        Randomly execute one of the motion methods (square or oval).

        This method selects either the `square` or `oval` method of the Motion object
        and executes it.

        Returns:
            The result of the executed Motion method, which could be the `square`, `oval`, 
            or 'triangle' method.

        """
        rpm = self._calc_random_rpm()
        feedrate = self._calc_random_feedrate(rpm)
        random_motion_method = random.choice([self._square, self._oval])
        return random_motion_method(size=random.randint(5, 20), 
                                    cutcom=self._cutter_compensation(), 
                                    rpm=rpm, 
                                    feedrate=feedrate)
