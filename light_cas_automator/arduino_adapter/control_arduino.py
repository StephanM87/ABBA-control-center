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

    #LED.write(1)
    #time.sleep(10)
    #LED.write(0)
    print("disconnect")
    #board.exit()

    print("halo")
    print("the board is:", board)
except Exception as err:
    print(err)
    #raise


namespace = Namespace("api/ot", description="Route whicht creates Enzymeml documents and returns them in form of omex archives")

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
        print("lets go")

        # Pump the reactor content into the NMR
        ot_control = ControlCommands()
        ot_control.stop_flow_pumping_in(p_pwm, p_on_off, p_direction)

        # Shim the reaction sample

        shim_session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        shim_session.connect((HOST, PORT))
        shim_command = ot_control.start_shimm()
        shim_session.send(shim_command.encode())
        shim_session.settimeout(10.0)
        shim_condition = True
        while shim_condition:
            time.sleep(0.2)
            shim_payload = shim_session.recv(8192)
            shim_read = XMLExtractor(shim_payload)
            shim_status = shim_read.check_if_error_or_status()
            print("Der shim output ist:t",shim_status)
            if shim_status["status"] == "error":
                print("Error detected")
                if shim_status["message"] == "Device is busy":
                    time.sleep(30)
                    shim_condition = False
                    shim_session.close()
            elif shim_status["status"] == "progress":
                        print("the shim percentage is at " + str(shim_status["message"]) + " %")
                        if shim_status["message"] == "100":
                            shim_session.close()
                            shim_condition = False
        test_condition = True
        
        while test_condition:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            xml_command = ot_control.start_shim()
            s.send(xml_command.encode())
            s.settimeout(10.0)
            time.sleep(0.2)
            chunk = s.recv(8192)
            print(chunk)
            test_read = XMLExtractor(chunk)
            payload_test = test_read.check_if_error_or_status()
            if payload_test["status"] == "error":
                if payload_test["message"] != "Device is busy":
                    test_condition = False
                    print("Unknown Error detected in test phase")
                elif payload_test["message"] == "Device is busy":
                    print("Beschäftigt!")
                    s.close()
                    time.sleep(30)   
            elif payload_test["status"] == "progress":
                test_condition = False
                print("die messare ist",payload_test["message"])
                print("it is working")
        conditio = True

        while conditio:
                time.sleep(0.2)
                print("der socket ist", type(s))
                chunk = s.recv(8192)
                test_read = XMLExtractor(chunk)
                payload = test_read.check_if_error_or_status()
                print("Der output ist:t",payload)
                if payload["status"] == "error":
                    print("Error detected")
                    if payload["message"] == "Device is busy":
                        time.sleep(30)
                        conditio = False
                        s.close()
                elif payload["status"] == "progress":
                    print("the shim percentage is at " + str(payload["message"]) + " %")
                    if payload["message"] == "100":
                        s.close()
                        conditio = False
                        print("Messung ist durch")
                        measurement = MeasurementExtractor("C:/PROJECTS/DATA")
                        measurement.get_measurement_folder()
                    else:
                        pass
                    