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
    column_to_be_centered = [  [sg.Text('My Window')],
                [sg.Input(key='-IN-')],
                [sg.Text(size=(30,1), key='-OUT-')],
                [sg.Button('Go'), sg.Button('Exit')]  ]

    layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0,0),key='-EXPAND2-'),              # the thing that expands from left
               sg.Column(column_to_be_centered, vertical_alignment='center', justification='center',  k='-C-')]]

    window = sg.Window('Window Title', layout, resizable=True,finalize=True, size=(600,400))
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    while True:             # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Go':
            window['-OUT-'].update(values['-IN-'])
    window.close()










def _db_connection():
    '''
    Connects to the .db file

    Returns
    -------
    connection : sqlite db connection

    '''
    try:
        connection = sqlite3.connect('MOCK_Data\\MOCK_Data.db')
    except Error:
        print(Error)
    return connection



if __name__ == "__main__":
    main()