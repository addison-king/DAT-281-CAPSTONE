# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 08:55:25 2021

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
    os.chdir(os.path.dirname(sys.argv[0]))
    
    layout = [[sg.Text("Please select an action that you would like to perform.")], 
          [sg.Button('Import new alumni to the database', key='alum')],
          [sg.Button('Import new interaction with alumni', key='interaction')],
          [sg.Button('Export list of alumni with ID numbers', key='export_ID')],
          [sg.Button('Export list of next alumni to contact', key='contact')]
          [sg.Button('Close the program', key='close')]]

    window = sg.Window("UIF: Alumni Database", layout)
    
    while True:
        event, values = window.read()
        if event == 'close' or event == sg.WIN_CLOSED:
            break
        elif event == 'alum':
            window.close()
            _new_alumni_gui()
        elif event == 'interaction':
            window.close()
            #Call the import_interaction function
        elif event == 'export_ID':
            window.close()
            #Call a function to output the master list of alumni
        elif event == 'contact':
            window.close()
            #Call a fucntion to output the next call list
            
            
            
    
    window.close()

def _new_alumni_gui():
    alumni_display = pd.read_csv('MOCK_Data\\New_Alumni.csv')
    keep_cols = ['Last Name',
                 'First Name',
                 'Graduation Year']
    alumni_display = alumni_display[keep_cols]
    data = alumni_display.values.tolist()
    header_list = alumni_display.columns.tolist()
    
    layout = [[sg.Text('The following alumni will be added to the database:\n')],
              [sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))],
              [sg.Button('Confirm', key='import')],
              [sg.Button('Cancel - Do NOT Add', key='cancel')]]
    window = sg.Window('UIF: Alumni Database', layout)
    
    while True:
        event, values = window.read()
        if event == 'import' or event == sg.WIN_CLOSED:
            break
            ##call the import alumni function
        elif event == 'cancel':
            break
    window.close()
    
    
def _db_connection():
    '''
    Connects to the .db file

    Returns
    -------
    connection : sqlite db connection
        
    '''
    try:
        connection = sqlite3.connect('MOCK_Data.db')
    except Error:
        print(Error)
    return connection

def _set_dir():
    """
    Sets the working directory to the github folder.
    Also checks to see if you are in a common working dr before prompting to 
        change.
    Returns
    -------
    None.

    """
    cwd = os.getcwd()
    if not(cwd == 'C:\\Users\\BKG\\OneDrive\\Desktop\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data' or
           cwd == 'C:\\Users\\falconfoe\\Documents\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data'):
        while True:
            local_machine = input('Laptop or Desktop?').upper()
            if not (local_machine == 'LAPTOP' or local_machine == 'DESKTOP' 
                    or local_machine == 'L' or local_machine == 'D'):
                print('please enter only either: laptop or desktop')
                continue
            else:
                break
            
        if(local_machine == 'LAPTOP' or local_machine == 'L'):
            os.chdir('C:\\Users\\BKG\\OneDrive\\Desktop\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data')
            print('wd is now:', os.getcwd())
        else:
            os.chdir('C:\\Users\\falconfoe\\Documents\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data')
            print(os.getcwd())
            print('wd is now:', os.getcwd())
    else:
        print('wd already set:', os.getcwd())
if __name__ == "__main__":
    main()