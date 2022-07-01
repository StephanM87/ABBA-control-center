import pyfirmata

board = pyfirmata.Arduino("COM3")

led = board.get_pin('d:6:o')
led.write(0)