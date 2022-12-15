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
HOST = "127.0.0.1"  # Replace
PORT = 13000 #Default port

try:
    #arduino = ControlPanel("COM3")
    board = pyfirmata.Arduino("COM3")
    #board = "hallo"
    p_pwm = board.get_pin('d:9:p')
    p_on_off = board.get_pin("d:2:o")
    p_direction = board.get_pin('d:3:o')
    LED = board.get_pin('d:6:o')
    print("the board is:", board)
    p_on_off.write(1)
except Exception as err:
    print(err)
    #raise


namespace = Namespace("api/ot", description="")

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
        

@namespace.route("/start_pump")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        p_pwm.write(0.1)
        p_on_off.write(0)
        return "Pumpe läuft"

@namespace.route("/stop_pump")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        p_pwm.write(0.7) 
        p_on_off.write(1)
        return "Pumpe aus"

@namespace.route("/test_pump")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        print("kack ab du kackvogel")
        ot_control = ControlCommands()
        ot_control.stop_flow_pumping_in(p_pwm, p_on_off, p_direction)
        ot_control.stop_flow_pumping_out(p_pwm, p_on_off, p_direction)

        return "Pumpe aus"
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



@namespace.route("/automated_system")
class AutomatedProcess(Resource):
    @namespace.doc()
    def get(self):
        print("lets go!!!")
        ot_control = ControlCommands()
        ot_control.stop_flow_pumping_in(p_pwm, p_on_off, p_direction)

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
        
        #print(concentrations)
        ot_control.stop_flow_pumping_out(p_pwm, p_on_off, p_direction)

        boundaries = {"butanal":3}
        
        #action = OTControlDecisions(p_pwm, p_on_off, p_direction, LED, concentrations, boundaries)
        #action.get_phase_and_boudaries("butanal")

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



