from flask import Flask
from flask_restx import Namespace, Resource, Api, fields, abort
from werkzeug.exceptions import BadRequest, HTTPException
import os
import pyfirmata
import time
import socket


#from light_cas_automator.arduino_adapter.control_panel import ControlPanel

try:
    #arduino = ControlPanel("COM3")
    board = pyfirmata.Arduino("COM3")
    #board = "hallo"
    p_pwm = board.get_pin('d:9:p')
    p_on_off = board.get_pin("d:2:o")
    p_direction = board.get_pin('d:3:o')
    LED = board.get_pin('d:6:o')
    #LED.write(1)
    #time.sleep(10)
    #LED.write(0)
    print("disconnect")
    #board.exit()

    print("halo")
    print("the board is:", board)
except Exception as err:
    print(err)
    raise


namespace = Namespace("api/ot", description="Route whicht creates Enzymeml documents and returns them in form of omex archives")

@namespace.route("/light_up")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        #control = ControlPanel(board)
        #control.build_connection()
        #control.start_led() 
        #LED_links = board.get_pin('d:6:o')
        LED.write(1)       
        return "LED leuchtet"

@namespace.route("/light_down")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        '''
        control = ControlPanel("COM3")
        control.stop_led()
        '''
        
        LED.write(0)
        return "LED aus"
        

@namespace.route("/start_pump")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        #control = ControlPanel("COM3")
        #control.start_pump_foward()
        #p_pump_pwm = board.get_pin('d:9:p')
        p_pwm.write(0.7)
        #p_pump_direction = board.get_pin('d:3:o')
        #p_pump_direction.write(0)
        #p_pump_on_off = board.get_pin("d:2:o") 
        p_on_off.write(0)
        
        
        return "Pumpe läuft"





@namespace.route("/stop_pump")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        #p_pump_pwm = board.get_pin('d:9:p')
        #p_pump_pwm.write(0.7)
        #p_pump_direction = board.get_pin('d:3:o')
        #p_pump_direction.write(0)
        #p_pump_on_off = board.get_pin("d:2:o") 
        #p_pump_on_off.write(1)
        #control = ControlPanel("COM3")
        #control.stop_pump()
        p_pwm.write(0.7)
        #p_pump_direction = board.get_pin('d:3:o')
        #p_pump_direction.write(0)
        #p_pump_on_off = board.get_pin("d:2:o") 
        p_on_off.write(1)
        return "Pumpe aus"


@namespace.route("/stop_flow")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        p_on_off.write(1)
        p_direction.write(1) # 1 is counterclockwise pumps into nmr
        p_pwm.write(0.8)
        print("pump starts")
        p_on_off.write(0)
        time.sleep(25)
        p_pwm.write(0.65)
        #time.sleep(10)
        #p_direction.write(0)
        time.sleep(35)
        p_on_off.write(1)
        
        HOST = "127.0.0.1"  # Replace
        PORT = 13000 #Default port
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.connect((HOST, PORT))
        '''
        message  = "<Message>\r\n"
        message += "   <CheckShimRequest/>\r\n"
        message += "</Message>\r\n"
        s.send(message.encode())
        print('\r\nMessage received:')
        s.settimeout(10.0)
        try:
            print("measurement ongoing")
        except socket.error as msg:
            s.settimeout(None)
            # will only get here if a timeout occurs
            print('\r\nClose connection')
            s.close()
        '''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        message  = "<Message>\r\n"
        message += "   <Start protocol='SHIM 1H SAMPLE'>\r\n"
        message += "     <Option name='SampleReference' value='4.74' />\r\n"
        message += "     <Option name='Shim' value='QuickShim1' />\r\n"
        message += "   </Start>\r\n"
        message += "</Message>\r\n"
        print('\r\nSend message:')
        print(message)
        s.send(message.encode())
        s.close()

        time.sleep(200)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        message  = "<Message>\r\n"
        message +="<Start protocol='1D EXTENDED+'>\r\n"
        message +="<Option name='Number' value='4' />\r\n"
        message +="<Option name='AquisitionTime' value='3.2' />\r\n"
        message +="<Option name='RepetitionTime' value='30' />\r\n"
        message +="<Option name='PulseAngle' value='90' />\r\n"
        message += "   </Start>\r\n"
        message += "</Message>\r\n"
        print('\r\nSend message:')
        print(message)
        s.send(message.encode())
        s.close()

        time.sleep(130)
        print("pump changes direction")
        p_on_off.write(1)
        p_pwm.write(0.65)
        p_direction.write(0) # 0 is clockwise, pumps into reactor
        p_on_off.write(0)
        print("yeah")
        #p_direction.write(1)
        time.sleep(50)
        p_on_off.write(1)


        return "Pumpe aus"
    
        
    
        
        