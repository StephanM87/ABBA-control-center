from flask import Flask
from flask_restx import Namespace, Resource, Api, fields, abort
from werkzeug.exceptions import BadRequest, HTTPException
import os
import socket
import time
import xml.etree.ElementTree as ET


#from light_cas_automator.arduino_adapter.control_panel import ControlPanel



namespace = Namespace("api/nmr", description="Route whicht creates Enzymeml documents and returns them in form of omex archives")

@namespace.route("/start")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
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
        s.send(message.encode())
        print('\r\nMessage received:')
        s.settimeout(10.0)
        conditio = True
        try:
            while True:
                time.sleep(0.2)
                chunk = s.recv(8192)
                if chunk:
                    data = chunk.decode() 
                    #print(data)
                    try:
                        root = ET.fromstring(data)
                        for i in root:
                            print("der tag ist",i.tag)
                            if i.tag == "StatusNotification":
                                #print(i.tag)
                                #print(i.attrib)
                                progress = i.iter('Progress')
                                for j in progress:
                                    attribs = j.attrib
                                    percentage = attribs["percentage"]
                                    print("the progress is "+ percentage)
                                    if percentage == "100":
                                        print("Shim completed")
                                        conditio = False
                                print("continuoe")
                            elif i.tag == "QuickShimResponse":
                                print("stop")
                                conditio=False

                    except Exception as err:
                        print(err)
                    print("Der output ist:", root)
        except socket.error as msg:
            s.settimeout(None)
            # will only get here if a timeout occurs
            print('\r\nClose connection')
            s.close()   
        s.close()   

        

        HOST = "127.0.0.1"  # Replace
        PORT = 13000 #Default port
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
        s.send(message.encode())
        print('\r\nMessage received:')
        s.settimeout(10.0)

        # read first response

        try:
            time.sleep(0.2)
            chunk = s.recv(8192)
            payload = chunk.decode()
            root = ET.fromstring(payload)
            for i in root:
                for i in root:
                    print(i.tag)
                    error = i.iter("Error")
                    print(error)
                    for j in i:
                        print("das ergebnis ist",j.tag)
                        if j.tag == "Error":
                            print("device still busy")
                            s.close()
                            time.sleep(80)
                            HOST = "127.0.0.1"  # Replace
                            PORT = 13000 #Default port
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
                            s.send(message.encode())
                            print('\r\nMessage received:')
                            s.settimeout(10.0)
                        if j.tag != "Error":
                            print("Es lebt")
        except Exception as err:
            print(err)


        try:
            while True:
                time.sleep(0.2)
                chunk = s.recv(8192)
                if chunk:
                    data = chunk.decode() 
                    print(data)
                    try:
                        root = ET.fromstring(data)
                        for i in root:
                            if i.tag == "StatusNotification":
                                print("continuoe")
                            elif i.tag == "QuickShimResponse":
                                print("stop")

                    except Exception as err:
                        print(err)
                    print("Der output ist:", root)
        except socket.error as msg:
            s.settimeout(None)
            # will only get here if a timeout occurs
            print('\r\nClose connection')
            s.close()   
        s.close()  




'''    
    def get(self):
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
        s.send(message.encode())
        print('\r\nMessage received:')
        s.settimeout(10.0)
        try:
            while True:
                time.sleep(0.2)
                chunk = s.recv(8192)
                if chunk:
                    data = chunk.decode() 
                    print(data)
                    try:
                        root = ET.fromstring(data)
                        for i in root:
                            if i.tag == "StatusNotification":
                                print("continuoe")
                            elif i.tag == "QuickShimResponse":
                                print("stop")

                    except Exception as err:
                        print(err)
                    print("Der output ist:", root)
        except socket.error as msg:
            s.settimeout(None)
            # will only get here if a timeout occurs
            print('\r\nClose connection')
            s.close()   
'''


