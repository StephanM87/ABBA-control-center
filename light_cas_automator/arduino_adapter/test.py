import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('COM5')
    LED_links = board.get_pin('d:2:o')
    LED_rechts = board.get_pin('d:3:o')

    def LED_start():

        while True:
            LED_links.write(1)
            LED_rechts.write(0)
            time.sleep(1.0)

            LED_links.write(0)
            LED_rechts.write(1)
            time.sleep(1.0)

LED_start()
