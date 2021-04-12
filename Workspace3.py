# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 08:51:28 2021

@author: BKG
"""
from pathlib import Path
import os
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd
import uuid
import PySimpleGUI as sg

def main():

    alumni = pd.read_csv('MOCK_Data\\New_Alumni.csv')
    alumni.drop('Timestamp', axis=1, inplace=True)
    col_names = ["last_name",
                "first_name",
                "CORE_student",
                "graduation_year",
                "phone_num",
                "birthday",
                "gender",
                "address",
                "city",
                "state",
                "zipcode",
                "email",
                "church",
                "highschool",
                "college",
                "job",
                "health_info",
                "parent_guardian",
                "parent_guardian_phone_num",
                "parent_guardian_email",
                "emergency_contact",
                "emergency_contact_phone_number",
                "OPTIONS",
                "education",
                "athletics",
                "performing_arts"]
    alumni.columns = col_names
    title_case_list = ['address',
                       'city',
                       'state',
                       'church',
                       'highschool',
                       'college',
                       'job']
    for i in title_case_list:
        alumni[i] = alumni[i].str.title()
    
    alumni['birthday'] = pd.to_datetime(alumni['birthday']).dt.strftime('%Y-%m-%d')
    
    for i in alumni.index:
        values = alumni.loc[i]
        new = pd.DataFrame(columns = alumni.columns)
        new = new.append(values, ignore_index = True)
        print(new)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()