"""
Created on Fri Mar 19 13:33:21 2021

@author: BKG
"""

from pathlib import Path
import os
import sqlite3
from sqlite3 import Error
import pandas as pd
import uuid

def main():
    _set_dir()
    _create_db_table()
    ask = input()
    if(ask=='y'):
        _import_alumni()
    else:
        print('^.^')



def _import_alumni():
    """
    

    Returns
    -------
    None.

    """
    
    alum_import = pd.read_csv('ImportTemplate.csv')
    for i in alum_import.index:
        alum_import.at[i,'unique_ID'] = uuid.uuid4()
        alum_import.at[i,'unique_ID'] = str(alum_import.at[i,'unique_ID'])
        i = i+1

    connection = _db_connection()
    alum_import.to_sql('Basic_Info', connection, if_exists='append',
                       index=False)
    connection.commit()
    connection.close()
    


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
    if not(cwd == 'C:\\Users\\BKG\\OneDrive\\Desktop\\GitHub\\DAT-281-CAPSTONE' or
           cwd == 'C:\\Users\\falconfoe\\Documents\\GitHub\\DAT-281-CAPSTONE'):
        while True:
            local_machine = input('Laptop or Desktop?').upper()
            if not (local_machine == 'LAPTOP' or local_machine == 'DESKTOP'):
                print('please enter only either: laptop or desktop')
                continue
            else:
                break
            
        if(local_machine == 'LAPTOP'):
            os.chdir('C:\\Users\\BKG\\OneDrive\\Desktop\\GitHub\\DAT-281-CAPSTONE')
            print('wd is now:', os.getcwd())
        else:
            os.chdir('C:\\Users\\falconfoe\\Documents\\GitHub\\DAT-281-CAPSTONE')
            print(os.getcwd())
            print('wd is now:', os.getcwd())
    else:
        print('wd already set:', os.getcwd())


        
def _create_db_table():
    '''
    Creates the tables if it doesn't exist.

    Returns
    -------
    None.

    '''
    sql_table_basic = '''CREATE table IF NOT EXISTS Basic_Info (
                        unique_ID text,
                        last_name text,
                        first_name text,
                        CORE_student text,
                        graduation_year integer,
                        phone_num text,
                        birthday text,
                        gender text,
                        address text,
                        city text,
                        state text,
                        zipcode integer,
                        email text,
                        church text,
                        highschool text,
                        college text,
                        job text,
                        health_info text,
                        parent_guardian text,
                        parent_guardian_phone_num text,
                        parent_guardian_email text,
                        emergency_contact text,
                        emergency_contact_phone_number text,
                        OPTIONS text,
                        education text,
                        athletics text,
                        performing_arts text
                        )'''
    sql_tables_contact = '''CREATE table IF NOT EXISTS Contact_Events (
                        unique_ID integer,
                        contact_date text,
                        status text,
                        need text,
                        notes text               
                        )'''
    connection = _db_connection()
    c = connection.cursor()
    c.execute(sql_table_basic)
    c.execute(sql_tables_contact)
    connection.commit()
    connection.close()

def _db_connection():
    '''
    Connects to the .db file

    Returns
    -------
    connection : sqlite db connection
        
    '''
    try:
        connection = sqlite3.connect('UIF_Alumni.db')
    except Error:
        print(Error)
    return connection


if __name__ == "__main__":
    main()