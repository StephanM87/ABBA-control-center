from flask import Flask
from flask_restx import Api, Resource
from flask_cors import CORS
import pyfirmata



# Hier werden Python eigenen Libraries importiert
# Selbst definierten Packages importiert

from assets.configurations import Configurations 
from light_cas_automator.arduino_adapter.control_arduino import namespace as pump_control
#from light_cas_automator.arduino_adapter.control_panel import ControlPanel
from light_cas_automator.nmr_adapter.nmr_adapter import namespace as nmr_control


#class AppInitializer(): # TODO #2
'''
    Intatiates the app and api classes required to run the REST-API

    Params:
        none

    This class is essential, because: 
    - it instatiates the app required for the webserver to work
    - it instatiates the api required for REST-API functionalities and the Swagger documentation
    - it sets the CORS 
    - it adds the namespaces to the api object
'''

def create_app():
    '''
    initiates the app, api and CORS object for the REST-Api
    Params:
        none
    Returns:
        app(Object): Central object and entrypoint for the REST-API
    '''
    app = Flask(__name__)
    api = Api(app)
    api.add_namespace(pump_control)
    api.add_namespace(nmr_control)
    config = Configurations.get_configuarations()
    CORS(app, resources=config["CORS"])
    return app
    

if __name__ == '__main__':
    app = create_app()
    app.run()
