from light_cas_automator.arduino_adapter.control_commands import ControlCommands
import socket

class SocketStarter:

    def __init__(self, HOST,PORT, timeout):
        #self.socket = socket
        self.HOST = HOST
        self.PORT = PORT
        self.timeout = timeout

    def start_check_quick_scan(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ot_control = ControlCommands()
        s.connect((self.HOST, self.PORT))
        xml_command = ot_control.check_quick_scan()
        s.send(xml_command.encode())
        s.settimeout(10.0)
        return s

    def start_1DExtended(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ot_control = ControlCommands()
        s.connect((self.HOST, self.PORT))
        xml_command = ot_control.start_shim()
        s.send(xml_command.encode())
        s.settimeout(10.0)
        return s

    def start_shim(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ot_control = ControlCommands()
        s.connect((self.HOST, self.PORT))
        xml_command = ot_control.start_shimm()
        s.send(xml_command.encode())
        s.settimeout(10.0)
        return s
