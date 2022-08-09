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
        print("lets go")

        # Pump the reactor content into the NMR
        ot_control = ControlCommands()
        #ot_control.stop_flow_pumping_in(p_pwm, p_on_off, p_direction)
        
        # Shim the reaction sample
        '''
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
        '''
        test_condition = True
        while test_condition:
        # Check status
            s_1d = SocketStarter(HOST,PORT, 10).start_check_quick_scan()
            print("*****************Check Status Method***************")
            '''
            s.connect((HOST, PORT))
            xml_command = ot_control.check_quick_scan()
            s.send(xml_command.encode())
            s.settimeout(10.0)
            '''
            print("*****************Start the Test Method*******************")
            measurement_ongoing = True

            while measurement_ongoing:
                print("s_neu ist im while loop: ", s_1d)
                #time.sleep(0.1)
                chunk = s_1d.recv(8129) 
                payload_stat = SpinsolveMessageReader(s_1d, chunk, "quickscan")
                #payload_status = payload_stat.readout_message()
                messages = payload_stat.define_cases()
                print(messages)
                if messages["status"] == "progress":
                    if messages["message"] != "finished":
                        print("measurement is at: ", messages["message"], " %")
                    elif messages["message"] == "finished":
                        print("process has finised HAHAHAHAH")
                        time.sleep(5)
                        s_1d.close()
                        measurement_ongoing = False
                        test_condition = False
                if messages["status"] == "error":
                    if messages["message"] == "busy":
                        print("device is still busy")
                        time.sleep(15)
                        s_1d.close()
                        measurement_ongoing = False


            '''

                if payload_status["status"] == "error":
                    if payload_status["message"] == "Device is busy":
                        print("Beschäftigt!")
                        measurement_ongoing = False
                        s_neu.close()
                        time.sleep(30)
                    elif payload_status["message"] != "Device is busy":
                        #test_condition = False
                        print("Unknown Error detected in test phase")
                        time.sleep(40)
                    test_condition = False
                elif payload_status["status"] == "progress":
                    test_condition = False
                    print("die messare ist",payload_status["message"])
                    print("it is working")
                    if payload_status["message"] == '80':
                        print("final measurement has been done")
                        s_neu.close()
                        measurement_ongoing = False
                    if payload_status["message"] != '100':
                        print("new measurement")

                    
            
            
            #time.sleep(0.2)
            #chunk = s.recv(8192)
            #print(chunk)
            #test_read = XMLExtractor(chunk)
            #payload_test = test_read.check_if_error_or_status()
            

        '''         
            
        conditio = True
        while conditio:
                s_neu = SocketStarter(HOST,PORT, 10).start_1DExtended()
                chunk = s_neu.recv(8129) 
                measurement_1D_ongoing = True
                print("*****************Start the 1Extended Method*******************")
                while measurement_1D_ongoing:
 
                    #time.sleep(0.1)
                    chunk = s_neu.recv(8129) 
                    payload_stat = SpinsolveMessageReader(s_neu, chunk, "1DExtended")
                    #payload_status = payload_stat.readout_message()
                    messages = payload_stat.define_cases()
                    print(messages)
                    if messages["status"] == "progress":
                        if messages["message"] != "finished":
                            print("measurement is at: ", messages["message"], " %")
                        elif messages["message"] == "finished":
                            print("process has finised HAHAHAHAH")
                            time.sleep(5)
                            s_neu.close()
                            measurement_1D_ongoing = False
                            conditio = False
                    if messages["status"] == "error":
                        if messages["message"] == "busy":
                            print("device is still busy")
                            time.sleep(15)
                            s_neu.close()
                            measurement_1D_ongoing = False
        '''
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                xml_command = ot_control.start_shim()
                s.send(xml_command.encode())
                s.settimeout(10.0)
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
                    time.sleep(30)
                    print("the shim percentage is at " + str(payload["message"]) + " %")
                    if payload["message"] == "100":
                        s.close()
                        conditio = False
                        print("Messung ist durch")
                        measurement = MeasurementExtractor("C:/PROJECTS/DATA")
                        measurement.get_measurement_folder()
                    else:
                        pass
        '''            

@namespace.route("/test_automated_system")
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
        data = MeasurementExtractor("C:/PROJECTS/DATA", [{"name":"reference", "protons":2},{"name":"butanal", "protons":2}], 3)
        data.calculate_concentrations()






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


