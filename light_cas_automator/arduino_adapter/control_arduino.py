import io
import urllib
from flask import Flask, request
from flask_restx import Namespace, Resource, Api, fields, abort
from werkzeug.exceptions import BadRequest, HTTPException
import os
import pyfirmata
import time
import socket

from light_cas_automator.arduino_adapter.control_commands import ControlCommands
from light_cas_automator.extract_measurement_data.extract_measurement_data import MeasurementExtractor
from light_cas_automator.arduino_adapter.xml_message_extractor import XMLExtractor
from light_cas_automator.arduino_adapter.spinsolve_message_reader import SpinsolveMessageReader
from light_cas_automator.arduino_adapter.socket_starter import SocketStarter
from light_cas_automator.arduino_adapter.control_panel import ControlPanel
from light_cas_automator.arduino_adapter.measurement_controller import MeasurementController
from light_cas_automator.extract_measurement_data.extract_measurement_data import MeasurementExtractor
from light_cas_automator.arduino_adapter.ot_control_decisions import OTControlDecisions
from light_cas_automator.arduino_adapter.control_panel_arduino_2 import Controller2


#from light_cas_automator.arduino_adapter.control_panel import ControlPanel

'''
Global variables required to control the NMR. The NMR is controlled via the Spinsolve software, which 
has a webserver implemented. This webserver is addressable over the localhost: 127.0.0.1 and the standard port 13000. The port can (if necessary)
be changed in the Spinsolve software.

HOST: Defines the localhost of the Computer on which the spinsolve software is running on
PORT: Is the Port of the websever in the Spinsolve software (by defaulöt 13000)

'''
HOST = "127.0.0.1"  # Replace
PORT = 13000 #Default port

'''
The first task when starting the ABBA-control center is a test which checks if the Arduino is connected correctly
It connects to the Arduino (COM 3) which controls the LED strip and checks wether a successful connection is established or not.

'''

try:
    board = pyfirmata.Arduino("COM3")
    LED = board.get_pin('d:6:o')
    print("the board is:", board)
except Exception as err:
    print(err)
    #raise


namespace = Namespace("api/ot", description="REST API used for the control of the LightCas Microcontroller environment")

@namespace.route("/light_up")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        command = ControlCommands()
        command.start_LED(LED)
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
        



@namespace.route("/start_pump_2")
class Pump2Starter(Resource):
    def get(self):
        controller2 = Controller2()
        controller2.start_pump_2()
        return("pump läuft")
@namespace.route("/stop_pump_2")
class Pump2Starter(Resource):
    def get(self):
        controller2 = Controller2()
        controller2.stop_pump_2()
        return("pump läuft nicht")

@namespace.route("/start_pump_3")
class Pump2Starter(Resource):
    def get(self):
        controller2 = Controller2()
        controller2.start_pump_3()
        return("pump läuft")
@namespace.route("/stop_pump_3")
class Pump2Starter(Resource):
    def get(self):
        controller2 = Controller2()
        controller2.stop_pump_3()
        return("pump läuft nicht")


@namespace.route("/measure")
class Pump2Starter(Resource):
    def get(self):
        measurement = MeasurementController(HOST,PORT)
        measurement.start_quickscan()

        measurement.sample_shim()
        measurement.start_quickscan()
        measurement.measure_id_extended()
        try:

            data = MeasurementExtractor("C:/Users/Malzacher/DATA", [{"name":"reference", "protons":9},{"name":"butanal", "protons":1}, {"name":"PAC", "protons":3}], 5)
            concentrations = data.calculate_concentrations()
        except Exception as err:
            print("die exception ist",err)
            concentrations = "not there"
        return concentrations



@namespace.route("/automated_system")
class AutomatedProcess(Resource):
    @namespace.doc()
    def get(self):
        print("lets go!!!")
        ot_control = ControlCommands() #TODO #27
        measurement = MeasurementController(HOST,PORT)
        measurement.start_quickscan()
        measurement.sample_shim()
        measurement.start_quickscan()
        measurement.measure_id_extended()
        
        try:

            data = MeasurementExtractor("C:/Users/Malzacher/DATA", [{"name":"reference", "protons":9},{"name":"butanal", "protons":1}, {"name":"PAC", "protons":3}], 5)
            concentrations = data.calculate_concentrations()
        except Exception as err:
            print("die exception ist",err)
            print("ERRRRRRRRROR")
            concentrations = "not there"

        time.sleep(10)
        

        boundaries = {"butanal":3}

        return concentrations

@namespace.route("/inactivate")
class AutomatedProcess(Resource):
    @namespace.doc()
    def get(self):
        command = ControlCommands()
        command.start_LED(LED)
        time.sleep(3600)
        command.stop_LED(LED)
    
        return "inactivation done"

@namespace.route("/reaction2")
class AutomatedProcess(Resource):
    @namespace.doc()
    def post(self):
        data = request.get_json()
        print(data)
        durations = data["duration"]
        pump2 = float(durations["pump1"])
        pump3 = float(durations["pump2"])
        controller2 = Controller2()
        controller2.start_pump_2()
        time.sleep(pump2)
        controller2.stop_pump_2()
        controller2.start_pump_3()
        time.sleep(pump3)
        controller2.stop_pump_3()
        
        time.sleep(10)
    
        return "successful added enzyme"



