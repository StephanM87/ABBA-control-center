


class OTControlDecisions:
    def __init__(self,p_pwm,p_on_off,p_direction,LED, concentrations, boundaries):
        self.p_pwm = p_pwm
        self.p_on_off = p_on_off
        self.p_direction = p_direction
        self.LED = LED
        self.concentrations = concentrations
        self.boundaries = boundaries
    
    def get_phase_and_boudaries(self, reaction_phase):
        
        key = self.boundaries[reaction_phase]
        print(key)
        try:
            value = self.concentrations[key]
        except Exception as err:
            print("error in ot control", err)

        print("the concentration to target is:", value)
        


        

    

    