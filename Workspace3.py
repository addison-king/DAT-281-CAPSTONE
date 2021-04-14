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
    sg.theme('DarkBlue3')

    layout_col = [[sg.Text('Please select an action that you would like to perform:',
                           size=(30,3),
                           font=('Courier', 15, 'bold'),
                           justification='center')],
                  [sg.Button('Close the program',
                             key='close',
                             size=(40,1))]]

    layout = [[sg.Column(layout_col, element_justification='center')]]

    window = sg.Window('UIF: Alumni Database', layout, size=(600, 400))

    while True:
        event = window.read()
        if event[0] in ('close', sg.WIN_CLOSED):
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
        connection = sqlite3.connect('MOCK_Data\\MOCK_Data.db')
    except Error:
        print(Error)
    return connection



if __name__ == "__main__":
    main()