import pyfirmata
import time



while True:
    board = pyfirmata.Arduino("COM4")
    print("Connected to board")
    led = board.get_pin('d:7:o')
    pump2 = board.get_pin("d:10:o")
    print("pins are subscribed")

    print("yeah")
    led.write(1)
    time.sleep(5)
    led.write(0)
    pump2.write(1)
    time.sleep(5)
    pump2.write(0)
    board.exit()
    print("board disconnected")

