import pyfirmata
import time


class Controller2:
    def __init__(self):
        pass
    

    def start_pump_2(self):
        board = pyfirmata.Arduino("COM4")
        led = board.get_pin('d:10:o')
        led.write(1)
        board.exit()
        print("board disconnected")
    def stop_pump_2(self):
        board = pyfirmata.Arduino("COM4")
        led = board.get_pin('d:10:o')
        led.write(0)
        board.exit()
    def start_pump_3(self):
        board = pyfirmata.Arduino("COM4")
        pump = board.get_pin('d:7:o')
        pump.write(1)
        board.exit()
        print("board disconnected")
    def stop_pump_3(self):
        board = pyfirmata.Arduino("COM4")
        pump = board.get_pin('d:7:o')
        pump.write(0)
        board.exit()

    
    def feed_reaction_step_2(pump2, pump3):
        board = pyfirmata.Arduino("COM4")
        pump2 = board.get_pin('d:10:o')
        pump3 = board.get_pin('d:7:o')
        pump2.write(1)
        time.sleep(pump2)
        pump2.write(0)
        pump3.write(1)
        time.sleep(pump3)
        pump3.write(0)
        board.exit