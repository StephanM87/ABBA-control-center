import pyfirmata


class Controller2:
    def __init__(self):
        pass
    

    def start_pump_2(self):
        board = pyfirmata.Arduino("COM4")
        print("Connected to board")
        led = board.get_pin('d:10:o')
        led.write(1)
        board.exit()
        print("board disconnected")
    def stop_pump_2(self):
        board = pyfirmata.Arduino("COM4")
        print("Connected to board")
        led = board.get_pin('d:10:o')
        led.write(0)
        board.exit()