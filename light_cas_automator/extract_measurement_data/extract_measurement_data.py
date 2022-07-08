import os
import glob
import pandas as pd
import socket
import time

path = "C:/PROJECTS/DATA"
path_new = "C:/PROJECTS/DATA/20220701-114607-1D EXTENDED+"

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


list_of_folders = glob.glob(path + "/*")

print(list_of_folders)

latest_folder = max(list_of_folders, key=os.path.getctime)

print("Der letzte Ordner ist", latest_folder)

df = pd.read_csv(path_new+"/new.csv")


print(df.head)


