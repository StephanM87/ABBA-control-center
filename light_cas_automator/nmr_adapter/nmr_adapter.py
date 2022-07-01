from flask import Flask
from flask_restx import Namespace, Resource, Api, fields, abort
from werkzeug.exceptions import BadRequest, HTTPException
import os
import socket
import time


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
        message += "   <QuickShimRequest/>\r\n"
        message += "</Message>\r\n"
        s.send(message.encode())
        print('\r\nMessage received:')
        s.settimeout(10.0)
        try:
            while True:
                time.sleep(0.2)
                chunk = s.recv(8192)
                if chunk:
                    print(chunk.decode())
        except socket.error as msg:
            s.settimeout(None)
            # will only get here if a timeout occurs
            print('\r\nClose connection')
            s.close()   
    