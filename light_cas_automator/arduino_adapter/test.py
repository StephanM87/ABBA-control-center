import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('COM6')
    LED_links = board.get_pin('d:6:o')
    p_pump_on_off = board.get_pin('d:2:o')
    p_pump_direction = board.get_pin('d:3:o')
    p_pwm = board.get_pin('d:9:p')
    


    #LED_rechts = board.get_pin('d:3:o')

    def LED_start():

        a = 5
        b = 0

        while True:
            print(1)
            print("b=", b)
            b = b+1
            print("b nach addition", b)
            
            LED_links.write(1)
            p_pump_on_off.write(0)
            p_pump_direction.write(0)
            p_pwm.write(0.3)
            time.sleep(3)
            

            LED_links.write(0)
            p_pump_on_off.write(1)
            p_pump_direction.write(1)
            p_pwm.write(0.1)
            time.sleep(10)
            
           


        
LED_start()



