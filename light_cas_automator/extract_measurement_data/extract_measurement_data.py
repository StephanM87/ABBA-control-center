import os
import glob
import pandas as pd
import socket
import time
import re

path = "C:/PROJECTS/DATA"
path_new = "C:/PROJECTS/DATA/20220701-114607-1D EXTENDED+"

'''
def shim_this_shit():
        HOST = "127.0.0.1"  # Replace
        PORT = 13000 #Default port
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

def measurement_test():
    shim_this_shit()
    time.sleep(200)
    list_of_folders = glob.glob(path + "/*")
    print(list_of_folders)  
    latest_folder = max(list_of_folders, key=os.path.getctime)
    print("Der letzte Ordner ist", latest_folder)
    df = pd.read_csv(path_new+"/new.csv")
    print(df.head)
    shim_this_shit()


#measurement_test()
'''

class MeasurementExtractor:

    def __init__(self, measurements_folder_path):
        self.measurements_folder_path = measurements_folder_path

    def get_measurement_folder(self):
        list_of_folders = glob.glob(path + "/*")
        print(list_of_folders)
        latest_file = max(list_of_folders, key=os.path.getctime)
        print("die latest file is", latest_file)
        df = pd.read_csv(latest_file+"/integrals.csv")
        print(df.head)

        return df


    def remove_shim_folders(self):
        folders = glob.glob(self.measurements_folder_path + "/*")
        sorted_folders = folders.sort(key=os.path.getmtime)
        print(sorted_folders)
        test = "C:/PROJECTS\\TEST"
        #rx = re.compile(r'C:\\PROJECTS\\.+?TEST.*')
        for i in folders:
           #print("Der ordner ist",i)
            rx = re.search("SHIM",i)
            print(rx)

    def sort_measurements(self):

        folders = glob.glob(self.measurements_folder_path + "/*")
        sorted_folders = folders.sort(key=os.path.getmtime)
        latest_file = max(sorted_folders, key=os.path.getctime)
        print(latest_file)



    '''

        list_of_folders = self.get_measurement_folder()
        print(list_of_folders)
        measurement_folders = []

        for i in list_of_folders:
            check = re.search("SHIM", i)
            test = bool(check)
            if not test:
                print("Hell Yeah", test)
                measurement_folders.append(i)
            print(check)
        return measurement_folders

    '''

    

    def extract_measurements(self):

        latest_folder = self.sort_measurements()
        print("Der letzte Ordner ist", latest_folder)
        df = pd.read_csv(path_new+"/new.csv")
        print(df.head)


'''
new = MeasurementExtractor("C:/PROJECTS/DATA")
folders = new.get_measurement_folder()
print(folders)
'''













