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
    connection = _db_connection()

    query = ''' SELECT ID_number, first_name, last_name,
                       CORE_student, graduation_year
                FROM Basic_Info
                ORDER BY last_name ASC
              '''

    output = pd.read_sql(query, con=connection)
    connection.close()
    col_names = ['ID_number',
                 'first_name',
                 'last_name',
                 'CORE_student',
                 'graduation_year']
    output.columns = col_names

    for i in output.index:
        last_date = str(output.iloc[i,4])
        last_date = last_date + '-06-01'
        output.at[i, 'last_date'] = last_date

    output['last_date'] = pd.to_datetime(output['last_date']).dt.strftime('%Y-%m-%d')
    output.drop(columns=['graduation_year'], inplace = True)
    output = output[['ID_number',
                     'last_name',
                     'first_name',
                     'CORE_student',
                     'last_date']]
    connection = _db_connection()
    output.to_sql('Last_Contact', connection, index=False,
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
        connection = sqlite3.connect('MOCK_Data\\MOCK_Data.db')
    except Error:
        print(Error)
    return connection



if __name__ == "__main__":
    main()