
import socket


from light_cas_automator.arduino_adapter.socket_starter import SocketStarter
from light_cas_automator.arduino_adapter.control_panel import ControlPanel

class MeasurementController:
    
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT


    def start_quickscan(self):
        test_condition = True
        while test_condition:
        # Check status
            s_1d = SocketStarter(self.HOST,self.PORT, 10).start_check_quick_scan()
            payload = ControlPanel(s_1d, "quickscan").get_status() # e.g. quickscan or sample_shim or  1D
            measurement_condition = payload["measurement"]

            while measurement_condition:
                
                measurement_payload = ControlPanel(s_1d, "quickscan").get_status()
                measurement_condition = measurement_payload["measurement"]
                test_condition = measurement_payload["command"]
                print("test_condition", test_condition)

    def sample_shim(self):
        test_condition = True
        while test_condition:
        # Check status
            s_1d = SocketStarter(self.HOST,self.PORT, 10).start_shim()
            payload = ControlPanel(s_1d, "sample_shim").get_status() # e.g. quickscan or sample_shim or  1D
            measurement_condition = payload["measurement"]

            while measurement_condition:
                
                measurement_payload = ControlPanel(s_1d, "sample_shim").get_status()
                measurement_condition = measurement_payload["measurement"]
                test_condition = measurement_payload["command"]
                print("test_condition", test_condition)

    def measure_id_extended(self):
        sample_condition = True
        while sample_condition:
        # Check status
            s_shim = SocketStarter(self.HOST,self.PORT, 10).start_1DExtended()
            
            payload = ControlPanel(s_shim, "sample_shim").get_status()
            measurement_condition = payload["measurement"]

            while measurement_condition:
                
                measurement_payload = ControlPanel(s_shim, "sample_shim").get_status()
                measurement_condition = measurement_payload["measurement"]
                sample_condition = measurement_payload["command"]
