import os
import glob
import pandas as pd
import socket
import time
import re

path = "C:/PROJECTS/DATA"
path_new = "C:/PROJECTS/DATA/20220701-114607-1D EXTENDED+"


class MeasurementExtractor:

    def __init__(self, measurements_folder_path, structures):
        self.measurements_folder_path = measurements_folder_path
        self.structures = structures
        self.payload = self.build_payload_dict()
        print("der payload nach dem constructor",self.payload)


    
    def build_payload_dict(self):

        payload = {}

        for i in self.structures:
            element = {"value":None, "concentration": None, "protons":i["protons"]}
            name = i["name"]
            payload[name] = element

        print(payload)
        return payload


    def get_measurement_folders(self):
        list_of_folders = glob.glob(self.measurements_folder_path + "/*")
        #print(list_of_folders)
        return list_of_folders

    def sort_measurement_folders(self):

        folder_list = self.get_measurement_folders()
        latest_folder = max(folder_list, key=os.path.getctime)
        #print(latest_folder)

        return latest_folder

    def extract_measurements(self):

        latest_folder = self.sort_measurement_folders()
        df = df = pd.read_csv(latest_folder+"/integrals.csv", delimiter=";")
        return df

    def extract_integrals(self):

        df = self.extract_measurements()
        print(df.head())
        integrals = df["Value"]

        for i in range(len(self.structures)):
            entry = integrals[i]
            key_dict_name = self.structures[i]["name"]

            payload_slice = self.payload[key_dict_name]
            
            payload_slice["value"] = entry
            self.payload[key_dict_name] = payload_slice
        print(self.payload)
            


    def sort_measurements(self):

        folders = glob.glob(self.measurements_folder_path + "/*")
        sorted_folders = folders.sort(key=os.path.getmtime)
        latest_file = max(sorted_folders, key=os.path.getctime)
        print(latest_file)
    
    
    def fomula_concentration(self, Ia, Is, Ns, Na):

        signals = Ia/Is
        protons = Ns/Na
        concentration_analyte = signals*protons*2
    
    def calculate_concentrations(self):
        self.extract_integrals()

        payload_keys = list(self.payload.keys())
        print(payload_keys)
        del payload_keys[0]
        print("es kommt der Paylooad", self.payload)
        print("es kommen die keys",payload_keys)

        Is = self.payload["reference"]["value"]
        Ns = self.payload["reference"]["protons"]
        print(Is, Ns)
        
    





new = MeasurementExtractor("C:/PROJECTS/DATA", [{"name":"reference", "protons":2},{"name":"butanal", "protons":2}])
folders = new.calculate_concentrations()
print(folders)













