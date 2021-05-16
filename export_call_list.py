# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 13:55:17 2021

@author: BKG
"""
import os
import sqlite3
from sqlite3 import Error
import pandas as pd

def main(location):
    # query_read = '''SELECT c.ID_number, c.first_name, c.last_name,
    #                        c.CORE_student, c.last_date, b.phone_num, b.email
    #                 FROM Last_Contact c
    #                 INNER JOIN Basic_Info b
    #                     ON c.ID_number = b.ID_number
    #                 WHERE last_date < DATE('now', '-90 days')
    #                 ORDER BY c.CORE_student DESC, c.last_date ASC
    #              '''

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