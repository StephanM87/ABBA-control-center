
from light_cas_automator.arduino_adapter.spinsolve_message_reader import SpinsolveMessageReader

class ControlPanel:
    
    def check_measurement(self):

        def __init__(self, socket, command):
            self.socket = socket
            self.command = command

        def get_messages(self):
            chunk = self.socket.recv(8129)
            payload_stat = SpinsolveMessageReader(self.socket, chunk, self.command)
            messages = payload_stat.define_cases()
            return messages

        def get_status(self):

            messages = self.get_messages()
            



