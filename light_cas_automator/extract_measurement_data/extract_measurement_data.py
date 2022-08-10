from dataclasses import replace
import os
import glob
import pandas as pd
import socket
import time
import re

path = "C:/PROJECTS/DATA"
path_new = "C:/PROJECTS/DATA/20220701-114607-1D EXTENDED+"


class MeasurementExtractor:

    def __init__(self, measurements_folder_path, structures, reference_concentration):
        self.measurements_folder_path = measurements_folder_path
        self.structures = structures
        self.reference_concentration = reference_concentration
        self.payload = self.build_payload_dict()
        print("der payload nach dem constructor",self.payload)

    def build_payload_dict(self):

        payload = {}

        for i in self.structures:
            element = {"value":None, "concentration": None, "protons":i["protons"]}
            name = i["name"]
            payload[name] = element
        return payload

    def get_measurement_folders(self):
        list_of_folders = glob.glob(self.measurements_folder_path + "/*")

        return list_of_folders

    def sort_measurement_folders(self):

        folder_list = self.get_measurement_folders()
        latest_folder = max(folder_list, key=os.path.getctime)

        return latest_folder

    def extract_measurements(self):

        latest_folder = self.sort_measurement_folders()
        df = df = pd.read_csv(latest_folder+"/integrals.csv", delimiter=";")
        
        return df

    def extract_integrals(self):

        df = self.extract_measurements()
        #print(df.head())
        integrals = df["Value"]

        for i in range(len(self.structures)):
            entry = integrals[i]
            entry_dot = entry.replace(",", ".")
            #print("die zahl ist", entry_dot)
            key_dict_name = self.structures[i]["name"]

            payload_slice = self.payload[key_dict_name]
            
            payload_slice["value"] = float(entry_dot)
            self.payload[key_dict_name] = payload_slice
        #print(self.payload)
            
    def set_reference_concentration(self):

        reference = self.payload["reference"]
        reference["concentration"] = self.reference_concentration
        self.payload["reference"] = reference


    def sort_measurements(self):

        folders = glob.glob(self.measurements_folder_path + "/*")
        sorted_folders = folders.sort(key=os.path.getmtime)
        latest_file = max(sorted_folders, key=os.path.getctime)

        #print(latest_file)
    
    
    def fomula_concentration(self, Ia, Is, Cs, Ns, Na):

        signals = Ia/Is
        protons = Ns/Na
        concentration_analyte = signals*protons*Cs
        return concentration_analyte
    
    def calculate_concentrations(self):
        self.set_reference_concentration()
        self.extract_integrals()

        payload_keys = list(self.payload.keys())
        #print(payload_keys)
        del payload_keys[0]

        Is = self.payload["reference"]["value"]
        Ns = self.payload["reference"]["protons"]
        Cs = self.payload["reference"]["concentration"]

        for i in payload_keys:
            Ia = self.payload[i]["value"]
            Na = self.payload[i]["protons"]
            concentration = self.fomula_concentration(Ia, Is, Cs, Ns, Na)
            self.payload[i]["concentration"] = concentration
            #print(self.payload)
        return self.payload
        

#new = MeasurementExtractor("C:/PROJECTS/DATA", [{"name":"reference", "protons":2},{"name":"butanal", "protons":2}], 3)
#folders = new.calculate_concentrations()
#print(folders)













