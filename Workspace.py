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
    
    alumni = pd.read_csv('MOCK_Basic_Info.csv')
    new_alumni = alumni[['last_name','first_name','birthday']].copy()
    new_alumni['birthday'] = pd.to_datetime(new_alumni['birthday']).dt.strftime('%m-%d-%Y')

    query = ''' SELECT COUNT(*), first_name, last_name, birthday
                FROM Alumni_ID
                WHERE last_name= :last AND first_name= :first AND birthday= :bday
                GROUP BY last_name
                '''

    connection = _db_connection()
    for i in new_alumni.index:

        last_name = new_alumni.loc[i,'last_name']
        first_name = new_alumni.loc[i,'first_name']
        bday = new_alumni.loc[i,'birthday']
        
        df = pd.read_sql(query, params={'last': last_name, 
                                        'first': first_name,
                                        'bday': bday},
                         con=connection)
        if not len(df) >0:
            new_alumni.to_sql('Alumni_ID', connection, index=False,
                              if_exists='append')
            connection.commit()
        else:
            print('\'',first_name,' ', last_name, '\' already exists..',
                  sep='')
            
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