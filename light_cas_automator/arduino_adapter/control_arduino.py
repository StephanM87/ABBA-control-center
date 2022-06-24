from flask import Flask
from flask_restx import Namespace, Resource, Api, fields, abort
from werkzeug.exceptions import BadRequest, HTTPException
import os
import pyfirmata


from light_cas_automator.arduino_adapter.control_panel import ControlPanel

#board = pyfirmata.Arduino(COM)

namespace = Namespace("api/ot", description="Route whicht creates Enzymeml documents and returns them in form of omex archives")

@namespace.route("/light_up")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        control = ControlPanel("COM3")
        control.start_led()        
        return "LED leuchtet"

@namespace.route("/light_down")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        control = ControlPanel("COM3")
        control.stop_led()
        return "LED aus"

@namespace.route("/start_pump")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        control = ControlPanel("COM3")
        control.start_pump_foward()
        return "Pumpe läuft"
@namespace.route("/stop_pump")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        control = ControlPanel("COM3")
        control.stop_pump()
        return "Pumpe aus"
    
        
    
        
        