import io
from flask import Flask
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
        p_pwm.write(0.7)
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
        data = MeasurementExtractor("C:/PROJECTS/DATA", [{"name":"reference", "protons":9},{"name":"butanal", "protons":1}], 5)
        concentrations = data.calculate_concentrations()
        print(concentrations)
        ot_control.stop_flow_pumping_out(p_pwm, p_on_off, p_direction)
        
        action = OTControlDecisions(p_pwm, p_on_off, p_direction, LED,  )

        






        '''
        print("lets go")
        test_condition = True
        while test_condition:
        # Check status
            s_1d = SocketStarter(HOST,PORT, 10).start_check_quick_scan()
            payload = ControlPanel(s_1d, "quickscan").get_status()
            measurement_condition = payload["measurement"]

            while measurement_condition:
                
                measurement_payload = ControlPanel(s_1d, "quickscan").get_status()
                measurement_condition = measurement_payload["measurement"]
                test_condition = measurement_payload["command"]
                print("test_condition", test_condition)

        shim_condition = True
        while shim_condition:
        # Check status
            s_shim = SocketStarter(HOST,PORT, 10).start_shim()
            payload = ControlPanel(s_shim, "sample_shim").get_status()
            measurement_condition = payload["measurement"]

            while measurement_condition:
                
                measurement_payload = ControlPanel(s_shim, "sample_shim").get_status()
                measurement_condition = measurement_payload["measurement"]
                shim_condition = measurement_payload["command"]

        while test_condition:
        # Check status
            s_1d = SocketStarter(HOST,PORT, 10).start_check_quick_scan()
            payload = ControlPanel(s_1d, "quickscan").get_status()
            measurement_condition = payload["measurement"]

            while measurement_condition:
                
                measurement_payload = ControlPanel(s_1d, "quickscan").get_status()
                measurement_condition = measurement_payload["measurement"]
                test_condition = measurement_payload["command"]
                print("test_condition", test_condition)

        sample_condition = True
        while sample_condition:
        # Check status
            s_shim = SocketStarter(HOST,PORT, 10).start_1DExtended()
            payload = ControlPanel(s_shim, "sample_shim").get_status()
            measurement_condition = payload["measurement"]

            while measurement_condition:
                
                measurement_payload = ControlPanel(s_shim, "sample_shim").get_status()
                measurement_condition = measurement_payload["measurement"]
                sample_condition = measurement_payload["command"]
        '''


