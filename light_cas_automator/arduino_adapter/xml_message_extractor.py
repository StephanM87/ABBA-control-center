import xml.etree.ElementTree as ET


tree = ET.parse('assets\error_nmr_measurement.xml')
tree_end = ET.parse('assets\\xml_test_end.xml')
tree_shim_intermediate = ET.parse("assets\cml_test_intermediate.xml")
mixed_tree = ET.parse("assets\mixed_retun.xml")
root = tree.getroot()
root_end = tree_shim_intermediate.getroot()



class XMLExtractor:
    '''
        Extracts the XML messages send by the Spinsolve software and extracts the status update (error or progress) from the XML message

        Attributes
        ----------
        root:string
            XML message from Spinsolve as string
        status:dict
            predefined dict, which serves as standardised carrier for the return of the status. The status key can be progress or error, the message key device is busy or a percentage 
            

    '''

    def __init__(self, root):
        self.root = root
        self.status = {"status":"", "message":""}


    def status_setter(self, message):
        '''
        Extracts the message from Spinsovle and returns the attribute status

        Parameters
        ----------
        message: object
            object describing the xml schema of Spinsolve
        
        Returns
        -------
        None
        '''

        for i in message.iter():
            #print(i.tag)
            if i.tag == "Error":
                error = i.attrib
                self.status["status"] = "error"
                self.status["message"]= error["error"]
            elif i.tag == "Progress":
                progress = i.attrib
                self.status["status"] = "progress"
                self.status["message"] = progress["percentage"]


    def check_if_error_or_status(self):
        '''
        Receives the XML message from Spinsolve and extracts the status update (error or progress) and returns the status attribute
        
        Parameters
        ----------
        root: string 
            XML message from Spinsolve as string
        
        Returns
        -------
        status: dict
            dict describing if spinsolve returned an error or a status update
        
        
        '''
        try:
            response = ET.fromstring(self.root)
            #message = response.getroot()
            self.status_setter(response)
            #print("return status")
            #print("das response objekt ist", self.status)
            return self.status
        except Exception as e:
            print("error")
            print(self.root)
            print(e)
            raise

    

#new = XMLExtractor("assets\cml_test_intermediate.xml").check_if_error_or_status()


#print(new)