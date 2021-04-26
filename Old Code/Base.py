"""
Created on Fri Mar 19 13:33:21 2021

@author: BKG
"""

from pathlib import Path
import os
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd
import uuid

def main():
    _set_dir()
    _create_db_table()
    mm_choice = _menu_main()
    if(mm_choice == '1'):
        _import_alumni()
        _export_alumni_name_list()
    elif(mm_choice == '2'):
        _import_new_interaction()
    elif(mm_choice == '3'):
        _export_alumni()
    elif(mm_choice == '4'):
        _edit_alumni()
    else:
        print('^.^')

def _menu_main():
    """
    Asks the user what they want to do.
    Returns the selection.

    Returns
    -------
    mm_value : str
        text of what the user wants to do.

    """
    print('What would you like to do? (pick a number)')
    print('\t1. Add new alumni.')
    print('\t2. Add new alumni interaction/call.')
    print('\t3. Query the database.')
    print('\t4. Edit values for existing alumni.')
    
    mm_value = input('Selection: ')
    return mm_value

def _import_new_interaction():
    new_call = pd.read_csv('MOCK_Data\MOCK_Contact_Event.csv')
    new_call['contact_date'] = pd.to_datetime(new_call['contact_date']).dt.strftime('%Y-%m-%d')
    connection = _db_connection()
    new_call.to_sql('Contact_Events', connection, index=False,
                    if_exists='append')
    connection.close()
    
    

def _edit_alumni():
# =============================================================================
#     f_name = input('Enter the first name of the alumni: ')
#     l_name = input('Enter the last name of the alumni: ')
#     g_date = input('Enter the graduation year of the alumni: ')
#     
#     connection = _db_connection()
#     c = connection.cursor()
#     
#     connection.close()
# =============================================================================
    
    
    print('To be finished later..')

def _import_alumni():
    """
    Reads in .csv with new alumni data. 
    Drops the Timestamp col (generated from google forms).
    Renames the columns to match the database.
    Changes the case to titlecase for these cols: address, city, state,
                       church, highschool, college, job
    Checks to make sure the alumni doesn't already exist. 
    Adds all new alumni to database where an ID number is assigned. 
    Retrieves the new ID number, adds it to the dataframe. 
    Then the dataframe containing all pertinent info is added to the database.
        
    Returns
    -------
    None.

    """
    
    alumni = pd.read_csv('MOCK_Data\\New_Alumni.csv')
    alumni.drop('Timestamp', axis=1, inplace=True)
    col_names = ["last_name",
                "first_name",
                "CORE_student",
                "graduation_year",
                "phone_num",
                "birthday",
                "gender",
                "address",
                "city",
                "state",
                "zipcode",
                "email",
                "church",
                "highschool",
                "college",
                "job",
                "health_info",
                "parent_guardian",
                "parent_guardian_phone_num",
                "parent_guardian_email",
                "emergency_contact",
                "emergency_contact_phone_number",
                "OPTIONS",
                "education",
                "athletics",
                "performing_arts"]
    alumni.columns = col_names
    title_case_list = ['address',
                       'city',
                       'state',
                       'church',
                       'highschool',
                       'college',
                       'job']
    for i in title_case_list:
        alumni[i] = alumni[i].str.title()
    
    alumni['birthday'] = pd.to_datetime(alumni['birthday']).dt.strftime('%Y-%m-%d')

    query_1 = ''' SELECT COUNT(*), first_name, last_name, birthday
                FROM Alumni_ID
                WHERE last_name= :last AND first_name= :first AND birthday= :bday
                GROUP BY last_name
                '''
    connection = _db_connection()                
    for i in alumni.index:

        last_name = alumni.loc[i,'last_name']
        first_name = alumni.loc[i,'first_name']
        bday = alumni.loc[i,'birthday']
        
        df = pd.read_sql(query_1, params={'last': last_name, 
                                        'first': first_name,
                                        'bday': bday},
                         con=connection)
        print(df)
        input()
        if len(df) == 0:
            add_alumni = alumni[['last_name','first_name','birthday']].copy()
            add_alumni.to_sql('Alumni_ID', connection, index=False,
                      if_exists='append')
        else:
            print('\'',first_name,' ', last_name, '\' already exists..',
                  sep='')
     
    
    connection.commit()        
    connection.close()
    
    
#import alumni now that IDs have been assigned
    query_2 = ''' SELECT alumni_ID
                FROM Alumni_ID
                WHERE first_name= :first AND 
                      last_name= :last AND 
                      birthday= :bday
                      '''
    connection = _db_connection()
    for i in alumni.index:
        last_name = alumni.loc[i, 'last_name']
        first_name = alumni.loc[i, 'first_name']
        bday = alumni.loc[i, 'birthday']
        
        df = pd.read_sql(query_2, params={'last': last_name,
                                        'first': first_name,
                                        'bday': bday},
                         con=connection)
        print(df)
        input()
        
        if len(df) == 1:
            alum_num = int(df.loc[0,'alumni_ID'])
            alumni.at[i, 'alumni_ID'] = alum_num
            alumni.to_sql('Basic_Info', connection, index=False,
                  if_exists='append')

        else:
            print('DF error. length of:', len(df))
    
    
    
    connection.commit()
    connection.close()
    
def _export_alumni_name_list():
    """
    Opens a connection to the database.
    Queries the database.
    Output is put into a dataframe.
    Dataframe is written to .csv file.

    Returns
    -------
    None.

    """
    connection = _db_connection()
    c = connection.cursor()
    
    query = ''' SELECT alumni_ID, first_name, last_name, 
                       graduation_year, CORE_student
                FROM Basic_Info
                ORDER BY last_name ASC
              '''
              
    output = pd.read_sql(query, con=connection)   
    connection.close()
    col_names = ['ID Number',
                 'First Name',
                 'Last Name',
                 'Graduation Year',
                 'CORE?']
    output.columns = col_names
    file_name = 'Master Alumni List.csv'
    output.to_csv(file_name, index=False, encoding='utf-8')
    

def _export_alumni():
    """
    Asks the user to input a last name and a first name.
    Looks up the combination, then asks the user what info they want.
    Exports a .csv file containing the data.

    Returns
    -------
    None.

    """
    
    export_last_name = input('Please enter the last name of the alumni: ')
    export_first_name = input('Please enter the first name of the alumni: ')
    connection = _db_connection()
    c = connection.cursor()
    c.execute(''' SELECT first_name, last_name
                  FROM Basic_Info
                  WHERE last_name=? AND first_name=?''',
                  (export_last_name, export_first_name))
    check = c.fetchone()

    if not check is None:
        choice = input('Please choose a number: \n'
                       '\t1. Return an Alumni\'s contact info \n'
                       '\t2. Return an Alumni\'s call logs \n'
                       '\t3. Some third option \n'
                       'Selection: ')
        if choice == '1':
            print('\n\nContact Info:\n')
            query = ''' SELECT first_name, last_name, phone_num, 
                       graduation_year, highschool
                           FROM Basic_Info
                           WHERE last_name= :last AND first_name= :first                      
                       '''
            df = pd.read_sql(query, params={'last': export_last_name,
                                            'first': export_first_name},
                             con=connection)
            print(df)

            connection.close()
        elif choice == '2':
            print('\n\nCall logs:\n')
            query = ''' SELECT first_name, last_name, contact_date, status, 
                            need, notes
                        FROM Basic_Info
                        INNER JOIN Contact_Events on 
                            Contact_Events.unique_ID = Basic_Info.unique_ID
                        WHERE last_name= :last AND first_name= :first 
                        ORDER BY contact_date desc
                    '''
            df = pd.read_sql(query, params={'last': export_last_name,
                                            'first': export_first_name},
                             con=connection)
            print(df)
            file_name = export_last_name + '.' + export_first_name + '.csv'
            df.to_csv(file_name, index=False, encoding='utf-8')
            print('Exported selected data to:', file_name)
            connection.close()
        elif choice == '3':
            print('\n\nAll info:\n')
            print('To be developed later...')
            connection.close()
        else:
            print('\n\n(._.)')
            connection.close()
        
    else:
        print('bad')
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
    os.chdir(os.path.dirname(sys.argv[0]))
# =============================================================================
#     cwd = os.getcwd()
#     if not(cwd == 'C:\\Users\\BKG\\OneDrive\\Desktop\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data' or
#            cwd == 'C:\\Users\\falconfoe\\Documents\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data'):
#         while True:
#             local_machine = input('Laptop or Desktop?').upper()
#             if not (local_machine == 'LAPTOP' or local_machine == 'DESKTOP' 
#                     or local_machine == 'L' or local_machine == 'D'):
#                 print('please enter only either: laptop or desktop')
#                 continue
#             else:
#                 break
#             
#         if(local_machine == 'LAPTOP' or local_machine == 'L'):
#             os.chdir('C:\\Users\\BKG\\OneDrive\\Desktop\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data')
#             print('wd is now:', os.getcwd())
#         else:
#             os.chdir('C:\\Users\\falconfoe\\Documents\\GitHub\\DAT-281-CAPSTONE\\MOCK_Data')
#             print(os.getcwd())
#             print('wd is now:', os.getcwd())
#     else:
#         print('wd already set:', os.getcwd())
# =============================================================================
        
def _create_db_table():
    sql_table_basic = '''CREATE table IF NOT EXISTS Basic_Info (
                        alumni_ID integer,
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
    sql_table_contact = '''CREATE table IF NOT EXISTS Contact_Events (
                        alumni_ID integer,
                        last_name text,
                        first_name text,
                        contact_date text,
                        status text,
                        need text,
                        notes text               
                        )'''
    sql_table_ID = '''CREATE table IF NOT EXISTS Alumni_ID (
                        alumni_ID integer PRIMARY KEY AUTOINCREMENT,
                        last_name text,
                        first_name text,
                        birthday text
                        )'''
    sql_i_row = ''' INSERT INTO Alumni_ID (alumni_ID, last_name)
                    VALUES (1000, 'Test')
                    '''
    sql_delete_i_row = '''  DELETE FROM Alumni_ID
                            WHERE alumni_ID IS 1000 AND last_name IS 'Test'
                            '''
    
    connection = _db_connection()
    c = connection.cursor()
    c.execute(sql_table_basic)
    c.execute(sql_table_contact)
    c.execute(sql_table_ID)
    c.execute(sql_i_row)
    c.execute(sql_delete_i_row)
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
        connection = sqlite3.connect('MOCK_Data\\MOCK_Data.db')
    except Error:
        print(Error)
    return connection


if __name__ == "__main__":
    main()