import time


class OTControlDecisions:
    def __init__(self,p_pwm,p_on_off,p_direction,LED, concentrations, boundaries):
        self.p_pwm = p_pwm
        self.p_on_off = p_on_off
        self.p_direction = p_direction
        self.LED = LED
        self.concentrations = concentrations
        self.boundaries = boundaries
    
    def get_phase_and_boudaries(self, reaction_phase):
        
        compare_value = self.boundaries[reaction_phase]
        print(compare_value)
        try:
            value = self.concentrations[reaction_phase]
            print("value is", value, "compare value is", compare_value)
            if value < compare_value:
                self.LED.write(1)
                time.sleep(20)
                self.LED.write(0)

        except Exception as err:
            print("error in ot control", err)

        print("the concentration to target is:", compare_value)

        


        

    

    