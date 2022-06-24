from flask import Flask
from flask_restx import Namespace, Resource, Api, fields, abort
from werkzeug.exceptions import BadRequest, HTTPException
import os
import pyfirmata


from light_cas_automator.arduino_adapter.control_panel import ControlPanel


arduino = ControlPanel("COM3")
board=arduino.build_connection()
p_pwm = board.get_pin('d:9:p')
p_on_off = board.get_pin("d:2:o")
LED = board.get_pin('d:6:o')

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
    
        
    
        
        