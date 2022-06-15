from flask import Flask
from flask_restx import Namespace, Resource, Api, fields, abort
from werkzeug.exceptions import BadRequest, HTTPException
import os


from light_cas_automator.arduino_adapter.control_panel import ControlPanel



namespace = Namespace("api/nmr", description="Route whicht creates Enzymeml documents and returns them in form of omex archives")

@namespace.route("/start")
class PumpControl(Resource):
    @namespace.doc()
    def get(self):
        return "das NMR lebt"
    