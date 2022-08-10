


class OTControlDecisions:
    def __init__(self,p_pwm,p_on_off,p_direction,LED, concentrations, boundaries):
        self.p_pwm = p_pwm
        self.p_on_off = p_on_off
        self.p_direction = p_direction
        self.LED = LED
        self.concentrations = concentrations
        self.boundaries = boundaries
    
    def get_phase_and_boudaries(self, boundaries, reaction_phase):
        
        key = self.boundaries[reaction_phase]
        value = self.concentrations[key]

        print("the concentration to target is:", value)
        


        

    

    