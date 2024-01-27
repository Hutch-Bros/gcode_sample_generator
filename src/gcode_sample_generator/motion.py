import random

APPROACH = 1.0
RETRACT = 0.250

class Motion:
    def __init__(self, controller_os: str, tool: dict) -> None:
        self.controller_os = controller_os
        self.tool = tool
        self.rpm = self.calc_random_rpm()
        self.feedrate = self.calc_random_feedrate()
        self.size = random.randint(5, 20)

    def calc_random_rpm(self) -> float:
        """
        Calculates a random RPM (Rotations Per Minute) based on the given surface feet per minute (SFM) range and diameter.

        Args:
            sfm_min (float): The minimum surface feet per minute.
            sfm_max (float): The maximum surface feet per minute.
            diameter (float): The diameter of the object.

        Returns:
            float: The calculated random RPM.

        """
        sfm = random.uniform(self.tool["sfm"]["min"], self.tool["sfm"]["max"])
        return round(sfm * 3.82 / self.tool["diameter"], 2)
    
    def calc_random_feedrate(self) -> float:
        """
        Calculates a random feedrate based on the given inputs.

        Args:
            ipt_min (float): The minimum inches per tooth (IPT) value.
            ipt_max (float): The maximum inches per tooth (IPT) value.
            rpm (float): The revolutions per minute (RPM) value.

        Returns:
            float: The calculated feedrate.

        """
        ipt = random.uniform(self.tool["ipt"]["min"], self.tool["ipt"]["max"])
        return round(ipt * self.rpm, 2)

    def cutter_compensation(self) -> str:
        """
        Determines whether (and how) to apply cutter compensation.

        This method decides whether to apply cutter compensation based on the tool's capability.
        If the tool supports cutter compensation (cutcom), it randomly selects either no compensation,
        left compensation (G41), or right compensation (G42). The choice is made with equal probability.

        Returns:
            str: A G-code command for cutter compensation ('G41' for left, 'G42' for right),
                or an empty string if no compensation is to be applied.

        """
        if self.tool["cutcom"]:
            return random.choice([None, "G41", "G42"])
        return None
    
    def square(self) -> str:
        """
        Generates a G-code sequence for creating a square with rounded corners.

        Returns:
            str: A string containing the complete G-code sequence for the operation.

        """
        corner_radius = self.size / 5
        cutcom = self.cutter_compensation()

        # Define points for G-code
        points = [
            f"S{self.rpm} M3",  # Spindle on
            f"G0 X0 Y-{APPROACH + corner_radius} Z3.0",  # Point 1
            "G0 Z0.1",  # Point 2
            f"G1 Z0.0 F{round(self.feedrate * 1/random.randint(1,5), 2)}" # Point 3
            ]  
        
        if cutcom is not None:
            points.append(cutcom)

        points += [
            f"G1 Y-{corner_radius}",  # Point 4
            f"G2 X{corner_radius} Y0 I{corner_radius} J0",  # Point 5
            f"G1 X{self.size - corner_radius} Y0 F{self.feedrate}",  # Point 6
            f"G3 X{self.size} Y{corner_radius} I0 J{corner_radius}",  # Point 7
            f"G1 X{self.size} Y{self.size - corner_radius}",  # Point 8
            f"G3 X{self.size - corner_radius} Y{self.size} I-{corner_radius} J0",  # Point 9
            f"G1 X{corner_radius} Y{self.size}",  # Point 10
            f"G3 X0 Y{self.size - corner_radius} I0 J-{corner_radius}",  # Point 11
            f"G1 X0 Y{corner_radius}",  # Point 12
            f"G3 X{corner_radius} Y0 I{corner_radius} J0",  # Point 13
            f"G2 X{corner_radius + RETRACT} Y-{RETRACT} I0 J-{RETRACT}",  # Point 14
        ]

        # Turn off cutter compensation if it was used
        if cutcom is not None:
            points.append("G40")

        # Retract Z
        points.append("G0 Z3.0")

        # temporary
        print("square")

        return '\n'.join(points)
    
    def oval(self) -> str:
            """
            Generates a G-code sequence for creating an oval with rounded ends.

            The oval is created by moving the cutter in a circular motion along the specified arc size.
            The size of the oval is determined by the 'size' attribute of the object.

            Returns:
                str: A string containing the complete G-code sequence for the operation.

            """
            arc_size = self.size / 2
            cutcom = self.cutter_compensation()

            # Define points for G-code
            points = [
                f"S{self.rpm} M3",  # Spindle on
                f"G0 X-1.0 Y-2.0 Z3.0",  # Point 1
                "G0 Z0.1",  # Point 2
                f"G1 Z0.0 F{round(self.feedrate * 1/random.randint(1,5), 2)}" # Point 3
                ]  
            
            if cutcom is not None:
                points.append(cutcom)

            points += [
                f"G1 Y-1.0",  # Point 4
                f"G2 X0 Y0 I1.0 J0",  # Point 5
                f"G3 X{arc_size} Y{arc_size} I0 J{arc_size} F{self.feedrate}",  # Point 6
                f"G1 Y{arc_size + 1}", # Point 7
                f"G3 X0 Y{self.size + 1} I-{arc_size} J0",  # Point 8
                f"G3 X-{arc_size} Y{arc_size + 1} I0 J-{arc_size}",  # Point 9
                f"G1 Y{arc_size}",  # Point 10
                f"G3 X0 Y0 I{arc_size} J0",  # Point 11
                f"G2 X{RETRACT} Y-{RETRACT} I0 J-{RETRACT}"  # Point 12   
            ]

            # Turn off cutter compensation if it was used
            if cutcom is not None:
                points.append("G40")

            # Retract Z
            points.append("G0 Z3.0")

            # temporary
            print("oval")

            return '\n'.join(points)
    
def run_generator(controller_os: str, tool: dict):
    motion = Motion(controller_os=controller_os, tool=tool)
    chosen_motion = random.choice([motion.square, motion.oval])
    return chosen_motion()