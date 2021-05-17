# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 08:01:11 2021

@author: BKG
"""

import sqlite3
from sqlite3 import Error
import pandas as pd



def main(df):
    """
    Takes a dataframe from the main script.
    Makes sure the date is in correct format.
    Writes the new information to the 'Contact_Events' table.
    Updates the newest date to the 'Last_Contact' table.

    Parameters
    ----------
    df : DataFrame
        Contains all info to write to the appropriate db tables.

    Returns
    -------
    None.

    """

    df['contact_date'] = pd.to_datetime(df['contact_date']).dt.strftime('%Y-%m-%d')
    
    contact_df = split_contact_events(df)
    last_df = split_last_contact(df)
    
    new_event_to_db(contact_df)
    update_last_contact(last_df)


def split_contact_events(df):
    result = df[['ID_number', 'contact_date', 'spoke', 'track',
                 'status', 'notes']]
    return result


def split_last_contact(df):
    result = df[['ID_number', 'contact_date', 'currently_employed', 
                 'occupation']]
    return result


def new_event_to_db(df):
    connection = _db_connection()
    df.to_sql('Contact_Events', connection, index=False, if_exists='append')
    connection.close()


def update_last_contact(df):
    query_read = '''SELECT ID_number, last_date
                     FROM Last_Contact
                     WHERE ID_number = :id
                 '''
    query_write_1 = '''UPDATE Last_Contact
                     SET last_date = ?,
                         currently_employed = ?,
                         occupation = ?
                     WHERE ID_number = ?
                  '''
    query_write_2 = '''UPDATE Basic_Info
                     SET job = ?
                     WHERE ID_number = ?
                  '''              
    connection = _db_connection()
    cursor = connection.cursor()
    for i in df.index:
        id_num = int(df.loc[i, 'ID_number'])

        date_df = pd.read_sql(query_read,
                              con=connection,
                              params={'id':id_num})


        if date_df.at[i, 'last_date'] < df.at[i, 'contact_date']:
            cursor.execute(query_write_1,
                           (df.at[i, 'contact_date'], 
                            df.at[i, 'currently_employed'], 
                            df.at[i, 'occupation'], id_num))
            cursor.execute(query_write_2,
                           (df.iloc[i]['occupation'], id_num))
            connection.commit()
        else:
            print(df.iloc[i]['contact_date'], 'is too old..')
    connection.close()

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
    # df = pd.DataFrame({'ID_number':1001,
    #                       'contact_date':'2020-04-20',
    #                       'spoke':'Yes',
    #                       'track':'College',
    #                       'status': 'On Track',
    #                       'currently_employed': 'Yes',
    #                       'occupation':'Processor',
    #                       'notes':'lorem ipsum.'},
    #                     index=[0])
    # main(df)
    main()