# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 08:45:45 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""
import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg
import re
from re import search
from datetime import datetime

def main():
    print()
    layout = [[sg.Text('Use this window to query the databse.')],
              [sg.Multiline(size=(100, 10), key='sql_input')],
              [sg.Text('_'  * 100, size=(100, 1))],
              [sg.Multiline(size=(100,10), enable_events=True,
                            do_not_clear=True, key='sql_output')],
              [sg.Button('Submit', key='query', size=(30,1)), 
               sg.T('     '),
               sg.Button('Main Menu', key='main', size=(30,1))]]
    
    window = sg.Window('UIF: Alumni Database', layout)
    
    while True:
        event, values = window.read()
        
        if event == 'query':
            answer = query_db(values['sql_input'])
            window['sql_output'].Update(answer)
        
        if event in ('main', sg.WIN_CLOSED):
            break
    window.close()

def query_db(query):
    print(query)
    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)
    
    return rows
    
def _db_connection():
    '''
    Connects to the .db file

    Returns
    -------
    connection : sqlite db connection

    '''
    try:
        connection = sqlite3.connect('Data\\UIF_Alumni_DB.db')
    except Error:
        print(Error)
    return connection    
    
    
if __name__ == "__main__":
    main()