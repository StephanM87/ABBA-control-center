import time

from numpy import busday_count


from light_cas_automator.arduino_adapter.xml_message_extractor import XMLExtractor


class SpinsolveMessageReader:

    def __init__(self, socket, chunk, method):
        self.chunk = chunk
        self.socket = socket
        self.method = method
        #self.sleep_time = sleep_time

    def readout_message(self):
        
        #message = self.socket.recv(8129)
        payload = XMLExtractor(self.chunk)
        payload_message = payload.check_if_error_or_status()

        return payload_message

    def define_cases(self):

        message = self.readout_message()

        if message["status"] == "error":
            if message["message"] =="Device is busy":
                return {"status":"error","message":"busy"}
        
        elif message["status"] == "progress":
            if self.method == "quickscan":
                if int(message["message"]) < 70:
                    return {"status":"progress","message":message["message"]}
                elif int(message["message"]) >= 70:
                    return {"status":"progress", "message":"finished"}

            elif self.method == "sample_shim" or self.method=="1DExtended":
                if int(message["message"]) < 100:
                    return {"status":"progress","message":message["message"]}
                elif int(message["message"]) >= 100:
                    return {"status":"progress", "message":"finished"}             
