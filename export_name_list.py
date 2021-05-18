# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12, 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

import os
import sqlite3
from sqlite3 import Error
import pandas as pd


def main(location):
    print()

    query = ''' SELECT Alumni_ID.ID_number, first_name, last_name,
                       graduation_year, CORE_student, birthday
                FROM Alumni_ID
                INNER JOIN Basic_Info on Basic_Info.ID_number = Alumni_ID.ID_number
                ORDER BY last_name ASC
              '''
    connection = _db_connection()
    output = pd.read_sql(query, con=connection)
    connection.close()

    col_names = ['ID Number', #Print friendly column names
                 'First Name',
                 'Last Name',
                 'Graduation Year',
                 'CORE?',
                 'Birthday']

    output.cloumns = col_names #rename the df col names
    file_name = 'Alumni List.csv'
    os.chdir(location)
    output.to_csv(file_name, index=False, encoding='utf-8')


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