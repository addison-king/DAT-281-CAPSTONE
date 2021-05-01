# -*- coding: utf-8 -*-
"""
Created on Sat May  1 12:26:46 2021

@author: falconfoe
"""
from fpdf import FPDF
import pandas as pd
import sqlite3
from sqlite3 import Error


def main(alumni_number):
    # alumni = setup()

    alumni_basic = basic_info(alumni_number)
    alumni_contacts = contact_events(alumni_number)

    name = alumni_basic.at[0,'First Name'] + ' ' + alumni_basic.at[0,'Last Name']
    pdf = PDF(name)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    pdf.cell(0,15,'Basic Information', 0,1,'C')

    for i in alumni_basic.columns:
        pdf.cell(100, 8, i, 'LB', 0)
        pdf.cell(0, 8, alumni_basic.at[0,i], 'B', 1, 'R')

    pdf.add_page()

    pdf.cell(0,15,'All Contact Events', 0,1,'C')

    for i in alumni_contacts.index:
        for j in alumni_contacts.columns:
            if j == 'Notes':
                if len(alumni_contacts.at[i,j]) > 75:
                    pdf.cell(50, 8, j, 'LB', 0)
                    pdf.set_font('Arial','',10)
                    pdf.multi_cell(0, 8, alumni_contacts.at[i,j], 'B', 'L')
                    pdf.set_font('Arial', '', 12)
                else:
                    pdf.cell(50, 8, j, 'LB', 0)
                    pdf.multi_cell(0, 8, alumni_contacts.at[i,j], 'B', 'R')
            else:
                pdf.cell(50, 8, j, 'LB', 0)
                pdf.multi_cell(0, 8, alumni_contacts.at[i,j], 'B', 'R')
        pdf.ln(5)

    file_name = name + '.pdf'
    pdf.output(file_name, 'F')

class PDF(FPDF):
    def __init__(self, name):
        super(PDF, self).__init__()
        self.name = name

    def header(self):
        self.image('UIF-Logo.png', x=10, y=0, h=30)
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, self.name, 'B', 0, 'C')
        # Line break
        self.ln(15)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


# =============================================================================
# def setup():
#     raw_data = [[1001, 'Gilbert', 'Brandyn', 'No', 2008, '304-991-1031',
#                  '1989-10-31', 'Male', '1602 Lowrie St.', 'Pittsburgh', 'Pennsylvania', 15212, '1314041@gmail.com', 'None',
#                  'South', 'Ccac', 'Data Analyst', '', 'Mom - Christy', '304-863-6184', 'parent_email@gmail.com', 'Mom - Christy', '304-863-6184',
#                  'No', 'No', 'No', 'No']]
#
#     cols = ['ID_number', 'last_name', 'first_name', 'CORE_student', 'graduation_year', 'phone_num',
#             'birthday', 'gender', 'address', 'city', 'state', 'zipcode', 'email', 'church',
#             'highschool', 'college', 'job', 'health_info', 'parent_guardian', 'parent_guardian_phone_num',
#             'parent_guardian_email', 'emergency_contact', 'emergency_contact_phone_number',
#             'OPTIONS', 'education', 'athletics', 'performing_arts']
#
#     alumni = pd.DataFrame(raw_data, columns=cols)
#     alumni = alumni.applymap(str)
#
#     cols = alumni.columns.tolist()
#     cols = [i.title() for i in alumni]
#
#     for index, item in enumerate(cols):
#         cols[index] = item.replace('_', ' ')
#
#     alumni.columns = cols
#     alumni.rename(columns = {'Id Number': 'ID Number', 'Health Info': 'Special Health Concerns'},
#                   inplace = True)
#
#     return alumni
# =============================================================================


def basic_info(alumni_number):

    query = '''SELECT *
               FROM Basic_Info
               WHERE ID_number = :id
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'id':alumni_number})
    connection.close()
    results = format_basic_info(results)

    return results


def format_basic_info(df):
    df = df.applymap(str)

    cols = df.columns.tolist()
    cols = [i.title() for i in df]

    for index, item in enumerate(cols):
        cols[index] = item.replace('_', ' ')

    df.columns = cols
    df.rename(columns = {'Id Number': 'ID Number',
                         'Health Info': 'Special Health Concerns',
                         'Phone Num': 'Phone Number',
                         'Address': 'Street Address',
                         'Parent Guardian': 'Parent | Guardian',
                         'Parent Guardian Phone Num': 'P|G Phone Number',
                         'Parent Guardian Email': 'P|G Email'},
                  inplace = True)

    df = df[['First Name','Last Name','ID Number','Core Student',
             'Graduation Year','Phone Number','Email','Birthday','Gender',
             'Street Address','City','State','Zipcode','Church','Highschool',
             'College','Job','Special Health Concerns','Parent | Guardian',
             'P|G Phone Number','P|G Email','Emergency Contact',
             'Emergency Contact Phone Number','Options','Education',
             'Athletics','Performing Arts']]

    # for i in df.columns:
    #     print(i, ' - ', df.at[0,i])

    return df


def contact_events(alumni_number):
    query = '''SELECT *
               FROM Contact_Events
               WHERE ID_number = :id
               ORDER BY contact_date desc
            '''
    connection = _db_connection()
    results = pd.read_sql(query,
                          con=connection,
                          params={'id':alumni_number})
    connection.close()

    results = format_contact_events(results)
    return results


def format_contact_events(df):
    df = df.applymap(str)
    df = df[['contact_date','spoke','track','status','notes']]
    df.rename(columns = {'contact_date': 'Date of Contact',
                         'spoke': 'Spoke to?',
                         'track': 'Current track',
                         'status': 'Track status',
                         'notes': 'Notes'},
                  inplace = True)

    # for j in df.index:
    #     for i in df.columns:
    #         print(i, ' - ', df.at[j,i])
    #     print('\n\n')
    return df


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
    alumni_number = 1001
    main(alumni_number)