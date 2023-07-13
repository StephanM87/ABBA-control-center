'''

This Method aims to control the hardware communication used in the LightCas cascade.
One of the biggest challenges in this project is that a test possibility is missing, able to mimic the reaction

In this method the following functions are aimed to be tested:

1. Import and anlysis of the measured values by the NMR
2. Control of the connected hardware:
   - Measurement Pump
   - Dosage pump 1
   - Dosage pump 2
   - LED strip

'''


import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('COM3')
    LED_links = board.get_pin('d:6:o')
    #LED_rechts = board.get_pin('d:3:o')

    def LED_start():

        while True:
            print(1)
            LED_links.write(1)
            time.sleep(1.0)

            LED_links.write(0)
            time.sleep(1.0)

LED_start()
