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
    """
    From the db, pulls the following columns from the listed tables, formats,
       the dataframe, then saves it to a .csv file. (see: 'query_read')
    Specifically, this gives the user a list of alumni to call next.

    Parameters
    ----------
    location : STR
        String of the path to the folder the user previously selected.

    Returns
    -------
    None.

    """

    query_read = '''SELECT Alumni_ID.ID_number, first_name, last_name,
                           CORE_student, phone_num, email, last_date
                    FROM Alumni_ID
                    INNER JOIN Basic_Info on Basic_Info.ID_number = Alumni_ID.ID_number
                    INNER JOIN Last_Contact on Last_Contact.ID_number = Alumni_ID.ID_number
                    WHERE last_date < DATE('now', '-90 days')
                    ORDER BY CORE_student DESC, last_date ASC
                 '''

    connection = _db_connection()
    contact = pd.read_sql(query_read, con=connection)
    connection.close()

    col_names = ['ID Number', #PRint friendly column names
                 'First Name',
                 'Last Name',
                 'CORE?',
                 'Phone Number',
                 'Email',
                 'Last Contact Date']
    contact.columns = col_names #rename the col nanes
    file_name = 'Alumni to Contact.csv'

    os.chdir(location)
    contact.to_csv(file_name, index=False, encoding='utf-8')


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
