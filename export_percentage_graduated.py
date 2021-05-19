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

    query = '''SELECT graduation_year, graduated
               FROM Basic_Info
               ORDER BY graduation_year asc'''
    connection = _db_connection()
    data = pd.read_sql(query, con=connection)
    connection.close()    

    for i in data.index:
        if data.at[i,'graduated'] == None:
            data.at[i,'graduated'] = 'No'
        if data.at[i,'graduation_year'] == 'None':
            data.at[i,'graduation_year'] = 0     

    result = pd.DataFrame(columns=['Graduation Year', 'Not Graduated', 'Graduated',
                                   'Total', 'Percentage Graduated'])
    
    for i in data.graduation_year.unique():
        raw_data = data.loc[data['graduation_year'] == i].value_counts(subset='graduated')
            
        
        if 'Yes' in raw_data.keys():
            yes = raw_data['Yes']
        else:
            yes = 0

        if 'No' in raw_data.keys():
            no = raw_data['No']
        else:
            no = 0

        total = no + yes
        perc_yes = round(yes/total, 3)

        dat = [i, no, yes, total, perc_yes]
        result.loc[len(result.index)] = dat
    
    result.sort_values(by=['Graduation Year'])
    
    file_name = 'Percentage_Graduated.csv'
    os.chdir(location)
    result.to_csv(file_name, index=False, encoding='utf-8')

    
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
