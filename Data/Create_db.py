# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 13:52:01 2021

@author: BKG
"""

import sqlite3
from sqlite3 import Error

def main():
    _create_db_table()

def _db_connection():
    '''
    Connects to the .db file

    Returns
    -------
    connection : sqlite db connection

    '''
    try:
        connection = sqlite3.connect('Data\\Clean_db\\UIF_Alumni_DB.db')
    except Error:
        print(Error)
    return connection

def _create_db_table():
    sql_table_basic = '''CREATE table IF NOT EXISTS Basic_Info (
                        ID_number integer,
                        CORE_student text,
                        graduation_year integer,
                        phone_num text,
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
                        graduated text,
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
    sql_table_contact = '''CREATE table IF NOT EXISTS Contact_Events (
                        ID_number integer,
                        contact_date text,
                        spoke text,
                        track text,
                        status text,
                        notes text
                        )'''
    sql_table_id = '''CREATE table IF NOT EXISTS Alumni_ID (
                        ID_number integer PRIMARY KEY AUTOINCREMENT,
                        last_name text,
                        first_name text,
                        birthday text
                        )'''
    sql_table_last_d = '''CREATE table IF NOT EXISTS Last_Contact (
                            ID_number integer PRIMARY KEY AUTOINCREMENT,
                            last_date text,
                            currently_employed text,
                            occupation text
                        )'''
    sql_i_row = ''' INSERT INTO Alumni_ID (ID_number, last_name)
                    VALUES (1000, 'Test')
                    '''
    sql_delete_i_row = '''  DELETE FROM Alumni_ID
                            WHERE ID_number IS 1000 AND last_name IS 'Test'
                            '''

    connection = _db_connection()
    cursor = connection.cursor()
    cursor.execute(sql_table_basic)
    cursor.execute(sql_table_contact)
    cursor.execute(sql_table_id)
    cursor.execute(sql_table_last_d)
    cursor.execute(sql_i_row)
    cursor.execute(sql_delete_i_row)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    # os.chdir(os.path.dirname(sys.argv[0]))
    main()