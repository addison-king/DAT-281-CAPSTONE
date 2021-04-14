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
    query_read = '''SELECT c.ID_number, c.first_name, c.last_name,
                           c.CORE_student, c.last_date, b.phone_num, b.email
                    FROM Last_Contact c
                    INNER JOIN Basic_Info b
                        ON c.ID_number = b.ID_number
                    WHERE last_date < DATE('now', '-90 days')
                    ORDER BY c.CORE_student DESC, c.last_date ASC
                 '''

    connection = _db_connection()
    contact = pd.read_sql(query_read, con=connection)
    col_names = ['ID Number',
                 'First Name',
                 'Last Name',
                 'CORE?',
                 'Last Contact Date',
                 'Phone Number',
                 'Email']
    contact.columns = col_names

    print(contact.head())











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