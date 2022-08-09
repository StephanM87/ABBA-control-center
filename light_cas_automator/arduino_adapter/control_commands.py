import socket
import time



class ControlCommands:
    
    def start_LED(self, LED):
        '''
        Enlights the LED Strip

        Parameters
        ----------
        LED: object 
            pin controller (digital pin 6) of the arduino
        
        Returns
        -------
        None
        '''
        LED.write(1)

    def stop_LED(self, LED):
        '''
        Stops the LED Strip

        Parameters
        ----------
        LED: object 
            pin controller (digital pin 6) of the arduino
        
        Returns
        -------
        None
        '''
        LED.write(1)

    def start_peristaltic_pump(self, p_pwm, p_on_off):
        '''
        Starts the peristaltic pump

        Parameters
        ----------
        p_pwm object 
            pin controller (pulse wide modulation pin 9) of the arduino
        p_on_off:
            pin controller (digital pin 2) of the arduino
        
        Returns
        -------
        None
        '''
        p_pwm.write(0.7)
        p_on_off.write(0)

    def stop_peristaltic_pump(self, p_pwm, p_on_off):
        '''
        Starts the peristaltic pump

        Parameters
        ----------
        p_pwm object 
            pin controller (pulse wide modulation pin 9) of the arduino
        p_on_off:
            pin controller (digital pin 2) of the arduino
        
        Returns
        -------
        None
        '''
        
        p_pwm.write(0.7) 
        p_on_off.write(1)

    def change_spped_peristaltic_pump(self, p_pwm, speed):
        '''
        Starts the peristaltic pump

        Parameters
        ----------
        p_pwm object 
            pin controller (pulse wide modulation pin 9) of the arduino
        speed: float
            float between 0 and 1 controlling the speed of the peristaltic pump
        
        Returns
        -------
        None
        '''

        p_pwm.write(speed)

    def change_direction_of_peristaltic_pump(self, p_direction, direction):
        '''
        chenges the direction of the peristaltic pump

        Parameters
        ----------
        p_direction: object 
            pin controller (pulse wide modulation pin 3) of the arduino
        direction: integer
            integer controlling the pump direction 1 means counterclockwise, 0 clockwise
        
        Returns
        -------
        None
        '''

        p_direction.write(direction)
        



    def start_shimm(self):
        '''
            Mehtod building the shim message to send as xml message to the Spinsolve TCP-endpoint

            Parameters
            ----------
            None

            Returns
            -------
            message: string
                xml message as string containing the commands to run a shim sample protocol
        '''
        message  = "<Message>\r\n"
        message += "   <Start protocol='SHIM 1H SAMPLE'>\r\n"
        message += "     <Option name='SampleReference' value='4.74' />\r\n"
        message += "     <Option name='Shim' value='QuickShim1' />\r\n"
        message += "   </Start>\r\n"
        message += "</Message>\r\n"

        return message


    def check_quick_scan(self):
        message = '<?xml version="1.0" encoding="UTF-8"?>'
        message+='<Message>\r\n'
        #message+= '<Set>\r\n'
        #message+= '<DataFolder>\r\n'
        #message+= '<UserFolder>\r\n'
        #message+= 'c:/PROJECTS/DATA/Waste'
        #message+= '</UserFolder>\r\n'
        #message+= '</DataFolder>\r\n'
        #message+= '</Set>\r\n'
        message += '<Start protocol="1D PROTON" >\r\n'
        message += '<Option name="Scan" value="QuickScan" />\r\n'
        message += '</Start>\r\n'
        message += '</Message>\r\n'
        return message

    def start_shim(self):
        '''
            Mehtod building the measurement message to send as xml message to the Spinsolve TCP-endpoint

            Parameters
            ----------
            None

            Returns
            -------
            message: string
                xml message as string containing the commands to run measurement
        '''
        message  = "<Message>\r\n"
        message +="<Start protocol='1D EXTENDED+'>\r\n"
        message +="<Option name='Number' value='1' />\r\n"
        #message +="<Option name='AquisitionTime' value='3.2' />\r\n"
        message +="<Option name='RepetitionTime' value='30' />\r\n"
        message +="<Option name='PulseAngle' value='90' />\r\n"
        message += "   </Start>\r\n"
        message += "</Message>\r\n"

        return message

    def check_protocols(self):

        message = "<?xml version='1.0' encoding='utf-8'?>"
        message += "<Message>"
        message += "<AvailableProtocolOptionsRequest/>"
        message += "</Message>"

        return message


    def stop_flow_pumping_in(self, p_pwm, p_on_off, p_direction):
        '''
        Starts the sequence to pump the reactor content into the NMR measurement cell

        Parameters
        ----------
        p_pwm:
            pin controller (pulse wide modulation pin 9) of the arduino
        p_on_off:
            pin controller (digital pin 2) of the arduino
        p_direction: object 
            pin controller (pulse wide modulation pin 3) of the arduino

        Returns
        -------
        None
        '''
        self.change_direction_of_peristaltic_pump(p_direction, 1)
        self.start_peristaltic_pump(p_pwm, p_on_off)
        time.sleep(5)
        self.change_spped_peristaltic_pump(p_pwm, 0.65)
        time.sleep(10)
        self.stop_peristaltic_pump(p_pwm, p_on_off)

    def stop_flow_pumping_out(self, p_pwm, p_on_off, p_direction):
        '''
        Starts the sequence to pump the reactor content into the NMR measurement cell

        Parameters
        ----------
        p_pwm:
            pin controller (pulse wide modulation pin 9) of the arduino
        p_on_off:
            pin controller (digital pin 2) of the arduino
        p_direction: object 
            pin controller (pulse wide modulation pin 3) of the arduino

        Returns
        -------
        None
        '''
        self.change_direction_of_peristaltic_pump(p_direction, 0)
        self.start_peristaltic_pump(p_pwm, p_on_off)
        time.sleep(5)
        self.change_spped_peristaltic_pump(p_pwm, 0.65)
        time.sleep(10)
        self.stop_peristaltic_pump(p_pwm, p_on_off)

        

    def stop_flow_measurement(self, p_pwm, p_on_off, p_direction):
        p_on_off.write(1)
        p_direction.write(1) # 1 is counterclockwise pumps into nmr
        p_pwm.write(0.8)
        print("pump starts")
        p_on_off.write(0)
        time.sleep(25)
        p_pwm.write(0.65)
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



    

