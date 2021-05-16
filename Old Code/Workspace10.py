# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 12:08:34 2021

@author: BKG
"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg
import re
from re import search
from datetime import datetime

def main(alumni):

    print(alumni, '\n')
    temp_query = '''UPDATE Basic_Info'''

    for i, value in enumerate(alumni):
        if value != 'ID_number':
            print(i)
            if i-1 == len(alumni.columns):
                print('LAST ONE')
                temp = '''\nSET ''' + value + ''' = ''' + alumni.at[0, value]
            else:
                temp = '''\nSET ''' + value + ''' = ''' + alumni.at[0, value] + ',f'
            temp_query = temp_query + value
    print(temp_query)
            
    
    
    
    
    
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
    test_data = {'ID_number': 1001,
             'first_name': 'Addison',
             'gender': 'Female'}
    results = pd.DataFrame(test_data, index=[0])
    main(results)