import time


from light_cas_automator.arduino_adapter.spinsolve_message_reader import SpinsolveMessageReader

class ControlPanel:
    
    def __init__(self, socket, command):
        self.socket = socket
        self.command = command
        self.loop_status = {"command":"", "measurement":""}

    def update_loop_status_dict(self, command, measurement):

        self.loop_status["command"] = command
        self.loop_status["measurement"] = measurement

    def get_messages(self):
        chunk = self.socket.recv(8192)
        print("ch8nk ist", chunk)
        payload_stat = SpinsolveMessageReader(self.socket, chunk, self.command)
        messages = payload_stat.define_cases()
        return messages

    def get_status(self):

        messages = self.get_messages()
        print(messages)
        if messages["status"] == "progress":
            if messages["message"] != "finished":
                print("measurement is at: ", messages["message"], " %")
                self.update_loop_status_dict(True, True)
                return self.loop_status
            elif messages["message"] == "finished":
                time.sleep(5)
                self.socket.close()
                self.update_loop_status_dict(False, False)
                return self.loop_status
        if messages["status"] == "error":
            if messages["message"] == "busy":
                print("device is still busy")
                time.sleep(15)
                self.socket.close()
                self.update_loop_status_dict(True, False)
                return self.loop_status
        



