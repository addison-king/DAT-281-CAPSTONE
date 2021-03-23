# -*- coding: utf-8 -*-
"""
Base.py Workspace
Simple code testing

@author: falconfoe
"""

from pathlib import Path
import os
import sqlite3
from sqlite3 import Error
import pandas as pd
import uuid

def main():
    _set_dir()
    
    new_call = pd.read_csv('2.csv')
    new_call['contact_date'] = pd.to_datetime(new_call['contact_date']).dt.strftime('%Y-%m-%d')
    connection = _db_connection()
    new_call.to_sql('Contact_Events', connection, index=False,
                    if_exists='append')
    connection.close()


    
    
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