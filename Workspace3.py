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


    layout = [[sg.Text('Please select an action that you would like to perform:',
                       size=(25,3),
                       font=('Arial', 15))],
          [sg.Button('Import new alumni to the database', 
                     key='alum',
                     size=(30,1))],
          [sg.Button('Import new interaction with alumni', 
                     key='interaction',
                     size=(30,1))],
          [sg.Text('_'  * 100, size=(32, 1))],
          [sg.Button('Export list of alumni with ID numbers', 
                     key='export_ID',
                     size=(30,1))],
          [sg.Button('Export list of next alumni to contact', 
                     key='contact',
                     size=(30,1))],
          [sg.Text('_'  * 100, size=(32, 1))],
          [sg.Button('Close the program', 
                     key='close',
                     size=(30,1))]]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event = window.read()
        print(event[0])
# =============================================================================
#         print(event)
# =============================================================================
        if event[0] == sg.WIN_CLOSED:
            break
# =============================================================================
#         if event == 'alum':
#             window.close()
#             
#         elif event == 'interaction':
#             window.close()
#             
#         elif event == 'export_ID':
#             window.close()
#             
#         elif event == 'contact':
#             window.close()
#             #Call a fucntion to output the next call list
#         elif event in('close', sg.WIN_CLOSED):
#             break
# =============================================================================

    window.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()