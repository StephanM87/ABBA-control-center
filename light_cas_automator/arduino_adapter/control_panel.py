import pyfirmata

class ControlPanel:

    def __init__(self, board):

        self.COM = board
        self.board = board
    
    def build_connection(self):
        try:
            board = pyfirmata.Arduino("COM3")
            return board
        except Exception as Err:
            print(Err, "already initialised")
    
    def start_led(self):
        board = self.build_connection()
        LED_links = board.get_pin('d:6:o')
        LED_links.write(1)
        board.exit()

    def start_led_init(self):
            #board = self.build_connection()
            LED_links = board.get_pin('d:6:o')
            LED_links.write(1)
            #board.exit()
'''
    def stop_led(self):
        #board = self.build_connection()
        LED_links = board.get_pin('d:6:o')
        LED_links.write(0)
        #board.exit()
    
    def start_pump_foward(self):
        print("hallo pump")
        board = self.build_connection()
        p_pump_pwm = board.get_pin('d:9:p')
        p_pump_pwm.write(0.7)
        p_pump_direction = board.get_pin('d:3:o')
        p_pump_direction.write(0)
        board.exit()

    def stop_pump(self):
        board = self.build_connection()
        p_pump_on_off = board.get_pin('d:2:o')
        p_pump_on_off.write(1)
        board.exit()

'''

