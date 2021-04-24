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

def main():
    print()
    lookup_alumni()
    

def lookup_alumni():
    
    frame_id_number = [[sg.Input(key='id_num')]]
    
    frame_first_name = [[sg.Input(key='first')]]
    
    frame_last_name = [[sg.Input(key='last')]]
    
    layout = [
        [sg.Frame('Alumni ID Number', frame_id_number)],        
        [sg.T('OR')],
        [sg.Frame('First Name', frame_first_name)],
        [sg.Frame('Last Name', frame_last_name)],
        [sg.Button('Lookup Alumni', key='lookup', size=(15,1)), sg.Cancel()]
        ]
    
    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break

        if event == 'lookup':
            if len(values['id_num']) != 0:
                alumni = sql_lookup_num(values['id_num'])
                print(alumni)
            elif le
            break
        
    window.close()
    return values


def sql_lookup_name(first, last):
    print()
    query = '''SELECT first_name, last_name, graduation_year
               FROM Basic_Info
               WHERE first_name =:first, last_name =:last
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'first':first, 'last':last})
    connection.close()
    
    return results
    
    
    
def sql_lookup_num(id_num):
    print()
    query = '''SELECT first_name, last_name, graduation_year
               FROM Basic_Info
               WHERE ID_number = :id
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'id':id_num})
    connection.close()
    
    return results
    
    
    

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