# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 09:27:14 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""

import sqlite3
from sqlite3 import Error
import pandas as pd

def main(df):
    """
    The funcitons that are called does 3 main things: (1)Writes to db and gets
        an ID number assigned. (2)Writes all info with newly made ID number to
        the db. (3)Initializes a 'last contacted' date by making it June 1, of
        the alumnis graduation year.

    Parameters
    ----------
    df : dataframe
        A dataframe containing all information about new alumni(s).

    Returns
    -------
    None.

    """

    df = id_assign(df)
    write_info(df)
    return

def id_assign(df):
    """
    First step in writing a new alumni to the database. First it checks to make
        sure this alumni doesn't already exist. If alumni does not exist, then
        it writes the new alumni to the table "Alumni_ID" where the alumni is
        assigned an ID number in the db.

    Parameters
    ----------
    df : dataframe
        Contains the information about the new alumni.

    Returns
    -------
    df : dataframe
        Will be empty if the alumni previously existed in the db, otherwise
            contains original data.

    """

#Prepare a query for the db
    query_1 = ''' SELECT COUNT(*), first_name, last_name, birthday
                    FROM Alumni_ID
                    WHERE last_name= :last AND first_name= :first AND birthday= :bday
                    GROUP BY last_name
                '''
#Get values for the query from the dataframe
    for i in df.index:
        last_name = df.loc[i,'last_name']
        first_name = df.loc[i,'first_name']
        bday = df.loc[i,'birthday']

        connection = _db_connection() #Establish connection to database
#Gets a df from the db using the query (looking for len(sq_df) = 0)
        sq_df = pd.read_sql(query_1, params={'last': last_name,
                                    'first': first_name,
                                    'bday': bday},
                            con=connection)


        if len(sq_df) == 0:
            data = [[last_name, first_name, bday]] #list of values
            add_alumni = pd.DataFrame(data, columns = ['last_name', #new df for db
                                                       'first_name',
                                                       'birthday'])
    #Write to the table "Alumni_ID" using the newly created df
            add_alumni.to_sql('Alumni_ID', connection, index=False,
                      if_exists='append')
            connection.commit()
            connection.close()
            return df
        else:
    #If the query from the db above returns any values, then the alumni already exists
            print('\'',first_name,' ', last_name, '\' already exists..',
                  sep='')
            df = df.drop(i) #drop the 'new' alumni from the table b/c they are a duplicate
            connection.commit()
            connection.close()
            return df


def write_info(df):
    """
    If the df has a length of 0, then this stops. Otherwise, querys the db for
        the alumni's ID number. Adds the ID number to the df. Then writes the
        full df to the table "Basic_Info".
        Finally calls the function: "initialize_last_contact"

    Parameters
    ----------
    df : dataframe
        Contains the information about the new alumni.

    Returns
    -------
    None.

    """
#When the df is not empty...
    if len(df) != 0:
#Prepare a query for the db, looking to retrieve the ID_number value
        query_2 = ''' SELECT ID_number
                      FROM Alumni_ID
                      WHERE first_name= :first AND
                            last_name= :last AND
                            birthday= :bday
                            '''
        connection = _db_connection() #db connection

#get values from the df for query_2
        for i in df.index:
            last_name = df.loc[i, 'last_name']
            first_name = df.loc[i, 'first_name']
            bday = df.loc[i, 'birthday']

#query the db to get the ID number for the selected alumni
            sql_df = pd.read_sql(query_2, params={'last': last_name,
                                            'first': first_name,
                                            'bday': bday},
                                con=connection)

            df.drop(['first_name', 'last_name', 'birthday'], axis=1, inplace=True)

#If the query returns not 1 entry, then an error is thrown
            if len(sql_df) == 1:
                alum_num = int(sql_df.loc[0,'ID_number']) #get the id number
                df.at[i, 'ID_number'] = alum_num #add ID num to df

                values = df.loc[i] #get values from the first row
                new = pd.DataFrame(columns = df.columns) #new df
                new = new.append(values, ignore_index = True) #add df values to new
                new.to_sql('Basic_Info', connection, index=False,
                              if_exists='append') #write to the db table Basic_Info
                connection.commit()
                connection.close()
                initialize_last_contact(df) #call function
            else:
                print('DF error. length of:', len(sql_df))
                connection.commit()
                connection.close()

    else:
        print('Nothing to add.')


def initialize_last_contact(df):
    """
    Every alumni has a 'last contact date' of June 1, (grad_year). This is so
        that each alumni shows up on a list of alumni needed to be contacted.
        Query the db then write to the table 'Last_Contact'.

    Returns
    -------
    None.

    """
#Prepare a query for the db
    query_read = '''SELECT ID_number, graduation_year
                    FROM Basic_Info
                    WHERE ID_number= :id_num
              '''

    for i in df.index:
        id_num = df.loc[i, 'ID_number']
        connection = _db_connection()
        output = pd.read_sql(query_read, params={'id_num': id_num},
                             con=connection) #df from the db using 'query'
        connection.close()

#This creates a 'last_date' value that is equal to June 1, grad_year
        last_date = str(output.loc[i, 'graduation_year'])
        last_date = last_date + '-06-01'
        output.at[i, 'last_date'] = last_date

#convert value to datetime
        output['last_date'] = pd.to_datetime(output['last_date']).dt.strftime('%Y-%m-%d')
        output.drop(columns=['graduation_year'], inplace = True) #drop col
        output = output[['ID_number', #prepare df to write to db
                         'last_date']]

        connection = _db_connection() #establish connection to db
        output.to_sql('Last_Contact', connection, index=False,
                        if_exists='append') #write to table 'Last_Contact'
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
    # test_data = {'first_name': 'Addison',
    #               'last_name': 'Smith',
    #               'CORE_student': 'No',
    #               'graduation_year': 2008,
    #               'birthday': '1999-11-11',
    #               'gender': 'Female',
    #               'city': 'Pittsburgh',
    #               'state': 'Pennsylvania',
    #               'zipcode': 15212,
    #               'church': 'None',
    #               'OPTIONS': 'No',
    #               'education': 'No',
    #               'athletics': 'No',
    #               'performing_arts': 'No'}
    # results = pd.DataFrame(test_data, index=[0])
    # main(results)
    main()