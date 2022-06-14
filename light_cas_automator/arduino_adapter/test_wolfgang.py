import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino('COM6')
    LED_links = board.get_pin('d:6:o')
    p_pump_on_off = board.get_pin('d:2:o')
    p_pump_direction = board.get_pin('d:3:o')
    p_pwm = board.get_pin('d:9:p')
    print("Good Morning Wolfgang, welcome to ABBA the Automated bio? \n please start the experiment by turning: \n the pump on \n the LED off")
    
    #LED_rechts = board.get_pin('d:3:o')

def LED_start_control(status_LED, status_Pump):

    a = 5
    b = 0
    b = b+1


    LED_links.write(status_LED)
    p_pump_on_off.write(status_Pump)
    p_pump_direction.write(0)
    p_pwm.write(0.4)
    time.sleep(40)

def stop_pump():
    p_pump_on_off.write(1)
    

while True:
    pump = input("Pump status on or off?")
    led = input("LED status on or off??")
    if pump == "on" and led == "off":
        # Step 1 Start the reaction
        print("The enzyme is beeing feeded")
        LED_start_control(0,0)
        print("enzymes feeding process has completed \n reaction is starting")
        stop_pump()
        time.sleep(10)
        print("reaction has completed, please inactivate the enzyme by setting: \n pump off \n LED on")
    elif pump == "off" and led=="on":
        LED_start_control(1,1)
        print("Inactivation completed")
        print("The experiment is completed, please shut down the pump and the LED stripe by: \n pump off \n LED off")
        
    elif pump == "off" and led=="off":
        print("Experiment shut down in progress")
        LED_start_control(0,1)
        print("Experiment has completed, thank you very much and have  nice day :)")
        break
    