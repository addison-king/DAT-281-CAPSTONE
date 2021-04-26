# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 08:51:28 2021
Developed for UIF to more easily handle the growing number of alumni they have,
    and to track interactions with said alumni.
Final Project for CCAC DAT-281
@author: BKG
"""
import sqlite3
from sqlite3 import Error
import pandas as pd
import PySimpleGUI as sg
import re


def main():
#initialize for upcoming IF checker
    values_page_1 = None
    values_page_2 = None
    values_page_3 = None
    values_page_4 = None
    values_page_5 = None

#get values from the user (if the user preses "Cancel", returns None, and stops)
    values_page_1 = text_new_alumni_p1()
    if values_page_1 != None:
        values_page_2 = text_new_alumni_p2()
    if values_page_2 != None:
        values_page_3 = text_new_alumni_p3()
    if values_page_3 != None:
        values_page_4 = text_new_alumni_p4()
    if values_page_4 != None:
        values_page_5 = text_new_alumni_p5()

#clean up each page's values
    if not None in [values_page_1, values_page_2, values_page_3, 
                    values_page_4, values_page_5]:
        values_page_1 = clean_page_1(values_page_1)  
        values_page_2 = clean_page_2(values_page_2)
        values_page_3 = clean_page_3(values_page_3)
        values_page_4 = clean_page_4(values_page_4)
        values_page_5 = clean_page_5(values_page_5)
        
#merge the 5 dictionaries together
        alumni_values = merge_dicts(values_page_1, values_page_2,
                                    values_page_3, values_page_4,
                                    values_page_5)
        
#convert the dictionary to a dataframe
        alumni = pd.DataFrame([alumni_values], columns=alumni_values.keys())
        
#rename all cols and reorder cols
        alumni = format_df(alumni)
        
#Sanity check
        for i in alumni:
            print(i, '-', alumni[i][0])
        
        return alumni
        
    else:
        print('None value. Quitting..')
        return None
        



def merge_dicts(p1, p2, p3, p4, p5):
    p1.update(p2) 
    p1.update(p3) 
    p1.update(p4) 
    p1.update(p5) 
    
    return p1

def format_df(df):
    df.rename(columns={'first': 'first_name', 
                       'last': 'last_name',
                       'core': 'CORE_student',
                       'grad_year': 'graduation_year',
                       'street_address': 'address',
                       'parent': 'parent_guardian',
                       'health': 'health_info',
                       'parent_phone': 'parent_guardian_phone_num',
                       'parent_email': 'parent_guardian_email',
                       'e_contact': 'emergency_contact',
                       'e_phone': 'emergency_contact_phone_number',
                       'options': 'OPTIONS',
                       'arts': 'performing_arts'
                       }, inplace=True)
    
    df = df[['last_name', 'first_name', 'CORE_student', 'graduation_year',
             'phone_num', 'birthday', 'gender', 'address', 'city', 'state',
             'zipcode', 'email', 'church', 'highschool', 'college', 'job',
             'health_info', 'parent_guardian', 'parent_guardian_phone_num',
             'parent_guardian_email', 'emergency_contact',
             'emergency_contact_phone_number', 'OPTIONS', 'education',
             'athletics', 'performing_arts']]
    
    df = df.fillna('None')
    
    title_case_list = ['last_name',
                       'first_name'
                       'address',
                       'city',
                       'state',
                       'church',
                       'highschool',
                       'college',
                       'job']
    
    for i in title_case_list:
        df[i] = df[i].str.title()
        
    df['birthday'] = pd.to_datetime(df['birthday']).dt.strftime('%Y-%m-%d')
        
    return df

def clean_page_1(values):
    if values['core_yes'] == True:
        values.pop('core_no', None)
        values.pop('core_yes', None)
        values['core'] = 'Yes'
    elif values['core_no'] == True:
        values.pop('core_no', None)
        values.pop('core_yes', None)
        values['core'] = 'No'
    
    if not '' in (values['phone1'], values['phone2'], values['phone3']):
        phone = values['phone1'] + '-' + values['phone2'] + '-' + values['phone3']
    else:   
        phone = ''
    
    values.pop('phone1', None)
    values.pop('phone2', None)
    values.pop('phone3', None)
    
    values['phone_num'] = phone
    
    return values

def clean_page_2(values):
    if values['gender_female'] == True:
        values.pop('gender_female', None)
        values.pop('gender_male', None)
        values['gender'] = 'Female'
        
    elif values['gender_male'] == True:
        values.pop('gender_female', None)
        values.pop('gender_male', None)
        values['gender'] = 'Male'
    
    if values['city_pgh'] == True:
        values['city'] = 'Pittsburgh'
        values.pop('city_pgh', None)
        values.pop('city_other', None)
        values.pop('city_input', None)
        
    elif values['city_other'] == True:
        values['city'] = values['city_input']
        values.pop('city_pgh', None)
        values.pop('city_other', None)
        values.pop('city_input', None)
        
    if values['state_pa'] == True:
        values['state'] = 'Pennsylvania'
        values.pop('state_pa', None)
        values.pop('state_other', None)
        values.pop('state_input', None)

    elif values['state_other'] == True:
        values['state'] = values['state_input']
        values.pop('state_pa', None)
        values.pop('state_other', None)
        values.pop('state_input', None)
        
    
    if not '' in (values['bday_month'],values['bday_day'],values['bday_year']):
        birthday = (values['bday_year'] + '-' +
                    values['bday_month'] + '-' +
                    values['bday_day'])
    else:
        birthday = ''
        
    values.pop('bday_month', None)
    values.pop('bday_day', None)
    values.pop('bday_year', None)
    
    values['birthday'] = birthday
    
    return values

def clean_page_3(values):
    if values['church_acac'] == True:
        values['church'] = 'ACAC'
        values.pop('church_acac', None)
        values.pop('church_none', None)
        values.pop('church_input', None)
        values.pop('church_other', None)
        
    elif values['church_none'] == True:
        values['church'] = 'None'
        values.pop('church_acac', None)
        values.pop('church_none', None)
        values.pop('church_input', None)
        values.pop('church_other', None)
        
    elif values['church_other'] == True:
        values['church'] = values['church_input']
        values.pop('church_acac', None)
        values.pop('church_none', None)
        values.pop('church_input', None)
        values.pop('church_other', None)
        
    return values

def clean_page_4(values):
    values.pop('e_parent', None)
    values.pop('e_number', None)
    
    if not '' in (values['parent_phone1'],
                  values['parent_phone2'],
                  values['parent_phone3']):
        parent_phone = (values['parent_phone1'] + '-' + 
                        values['parent_phone2'] + '-' + 
                        values['parent_phone3'])
    else:
        parent_phone = ''
        
    values.pop('parent_phone1', None)
    values.pop('parent_phone2', None)
    values.pop('parent_phone3', None)
    values['parent_phone'] = parent_phone
    
    if not '' in (values['e_phone1'],
                  values['e_phone2'],
                  values['e_phone3']):
    
        e_phone = (values['e_phone1'] + '-' + 
                   values['e_phone2'] + '-' + 
                   values['e_phone3'])
    else:
        e_phone = ''
        
    values.pop('e_phone1', None)
    values.pop('e_phone2', None)
    values.pop('e_phone3', None)
    values['e_phone'] = e_phone
    
    return values

def clean_page_5(values):
    if values['options_yes'] == True:
        values['options'] = 'Yes'
        values.pop('options_yes', None)
        values.pop('options_no', None)
    else:
        values['options'] = 'No'
        values.pop('options_yes', None)
        values.pop('options_no', None)
    
    if values['education_yes'] == True:
        values['education'] = 'Yes'
        values.pop('education_yes', None)
        values.pop('education_no', None)
    else:
        values['education'] = 'No'
        values.pop('education_yes', None)
        values.pop('education_no', None)
        
    if values['athletics_yes'] == True:
        values['athletics'] = 'Yes'
        values.pop('athletics_yes', None)
        values.pop('athletics_no', None)
    else:
        values['athletics'] = 'No'
        values.pop('athletics_yes', None)
        values.pop('athletics_no', None)
        
    if values['arts_yes'] == True:
        values['arts'] = 'Yes'
        values.pop('arts_yes', None)
        values.pop('arts_no', None)
    else:
        values['arts'] = 'No'
        values.pop('arts_yes', None)
        values.pop('arts_no', None)
    
    return values
    

def text_new_alumni_p1():

    frame_first_name = [[sg.Input(key='first')]]
    
    frame_last_name = [[sg.Input(key='last')]]

    frame_core_student = [[sg.Radio('Yes', 'CORE', key='core_yes'),
                          sg.Radio('No', 'CORE', key='core_no', default=True)]]

    frame_grad_year = [[sg.Input(key='grad_year', size=(13,1),
                                 change_submits=True, do_not_clear=True),
                       sg.T('', key='error_grad_year', text_color='purple', size=(26,1))]]

    frame_phone_number = [[sg.In(key='phone1', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='phone2', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='phone3', size=(5,1),
                                 change_submits=True, do_not_clear=True)]]
    
    frame_email = [[sg.In(key='email')]]
    
    frame_missing_val = [[sg.T('', key='main_error', 
                               text_color='white', size=(43,1))]]

    layout = [[sg.Text('New Alumni - Page 1')],
          [sg.Frame('First Name *', frame_first_name)],
          [sg.Frame('Last Name *', frame_last_name)],
          [sg.Frame('CORE Student? *', frame_core_student)],
          [sg.Frame('Graduation Year *', frame_grad_year)],
          [sg.Frame('Phone Number', frame_phone_number)],
          [sg.Frame('Email', frame_email)],
          [sg.Frame('Error Checking', frame_missing_val)],
          [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel(),
           sg.T('* Required', text_color='red')] ]

    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break

        if event == 'next_page':
#first name cannot be empty
            if len(values['first']) == 0:
                    window['main_error'].Update('Please input a First Name')
                    window['main_error'].Widget.config(background='red')  
#last name cannot be empty
            elif len(values['last']) == 0:
                    window['main_error'].Update('Please input a Last Name')
                    window['main_error'].Widget.config(background='red')
#graduation year must be 4 digits
            elif len(values['grad_year']) != 4:
                    window['main_error'].Update('Please input a Graduation Year')
                    window['main_error'].Widget.config(background='red')
#phone number must be empty OR ###-###-####
            elif ((sum([len(values['phone1']),
                       len(values['phone2']),
                       len(values['phone3'])]) != 0) and
                 (len(values['phone1']) !=3 or 
                  len(values['phone2']) !=3 or 
                  len(values['phone3']) !=4)):
                    window['main_error'].Update('Please complete the Phone Number')
                    window['main_error'].Widget.config(background='red')
#No errors, break, continue to next page  
            elif (sum([len(values['last']), 
                       len(values['first'])]) >= 2 and
                  len(values['grad_year']) == 4 and 
                  sum([len(values['phone1']),
                       len(values['phone2']),
                       len(values['phone3'])]) in [0,10]):
                    window['main_error'].Update('')
                    window['main_error'].Widget.config(background='#64778D')
                    break

        if event in ('grad_year', 'phone1', 'phone2', 'phone3'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        if event == 'grad_year' and len(window[event].Get()) >= 1:
            if not re.match('^20[0-4]{1}\d{1}$', window[event].Get()):
                window['error_grad_year'].Update('Please enter a valid graduation year.')
                window['grad_year'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_grad_year'].Update('')
                window['grad_year'].Widget.configure(highlightcolor='white')
                window['phone1'].SetFocus()

        if event == 'phone1' and len(window[event].Get()) == 3:
            window['phone2'].SetFocus()
        if event == 'phone2' and len(window[event].Get()) == 3:
            window['phone3'].SetFocus()
        if event == 'phone3' and len(window[event].Get()) == 4:
            window['email'].SetFocus()

    window.close()

    return values

def text_new_alumni_p2():
    frame_birthday = [[sg.In(key='bday_month', size=(3,1),
                         change_submits=True, do_not_clear=True),
                   sg.T('-', pad=(0,0)),
                   sg.In(key='bday_day', size=(3,1),
                         change_submits=True, do_not_clear=True),
                   sg.T('-', pad=(0,0)),
                   sg.In(key='bday_year', size=(5,1),
                         change_submits=True, do_not_clear=True),
                   sg.T('', key='error_bday', text_color='purple', size=(25,2))]]

    frame_gender = [[sg.Radio('Female', 'gender', key='gender_female'),
                     sg.Radio('Male', 'gender', key='gender_male')]]

    frame_street_ad = [[sg.In(key='street_address', size=(49,1))]]

    frame_city = [[sg.Radio('Pittsburgh', 'city', key='city_pgh', default=True),
                   sg.Radio('Other', 'city', key='city_other', enable_events=True),
                   sg.In(key='city_input', size=(25,1))]]

    frame_state = [[sg.Radio('Pennsylvania', 'state', key='state_pa', default=True),
                    sg.Radio('Other', 'state', key='state_other', enable_events=True),
                    sg.In(key='state_input', size=(23,1))]]

    frame_zipcode = [[sg.In(key='zipcode', size=(6,1),
                            change_submits=True, do_not_clear=True),
                      sg.T('', key='error_zipcode', text_color='purple', size=(36,2))]]

    frame_missing_val = [[sg.T('', key='main_error', 
                               text_color='white', size=(43,1))]]   

    layout = [[sg.T('New Alumni - Page 2')],
              [sg.Frame('Birthday (mm-dd-yyyy) *', frame_birthday)],
              [sg.Frame('Gender *', frame_gender)],
              [sg.Frame('Street Address', frame_street_ad)],
              [sg.Frame('City *', frame_city)],
              [sg.Frame('State *', frame_state)],
              [sg.Frame('Zipcode *', frame_zipcode)],
              [sg.Frame('Error Checking', frame_missing_val)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel(),
               sg.T('* Required', text_color='red')]
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'next_page':
#Birthday field must be empty or mm-dd-yyyy
            if (len(values['bday_month']) !=2 or 
                  len(values['bday_day']) !=2 or 
                  len(values['bday_year']) !=4):
                    window['main_error'].Update('Please complete the Birthday')
                    window['main_error'].Widget.config(background='red')
#Gender field must have 1 option selected
            elif sum([values['gender_male'], values['gender_female']]) == 0:
                    window['main_error'].Update('Please select a Gender')
                    window['main_error'].Widget.config(background='red')
#Zipcode must be a 5-digit number    
            elif len(values['zipcode']) != 5:
                window['main_error'].Update('Please input a 5-digit Zipcode')
                window['main_error'].Widget.config(background='red')  
#All conditions met, break, move to next page
            elif (len(values['zipcode']) == 5 and
                  sum([values['gender_male'], values['gender_female']]) != 0 and
                (len(values['bday_month']) ==2 or 
                 len(values['bday_day']) ==2 or 
                 len(values['bday_year']) ==4)):
                        window['main_error'].Update('')
                        window['main_error'].Widget.config(background='#64778D')
                        break
            
        if event == 'city_other':
            window['city_input'].SetFocus()
        if event == 'state_other':
            window['state_input'].SetFocus()

        if event in ('bday_month', 'bday_day', 'bday_year', 'zipcode'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        if event == 'bday_month' and len(window[event].Get()) >= 1:
            if not re.match('^0[1-9]|1[0-2]$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid month\n(e.g. Feb = 02).')
                window['bday_month'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')
                window['bday_day'].SetFocus()

        if event == 'bday_day' and len(window[event].Get()) >= 1:
            if not re.match('^0[1-9]|1[0-9]|2[0-9]|3[0-1]$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid day\n(e.g. 3rd of month = 03).')
                window['bday_month'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')
                window['bday_year'].SetFocus()

        if event == 'bday_year' and len(window[event].Get()) >= 1:
            if not re.match('^19\d{2}|20[0-4]{1}\d{1}$', window[event].Get()):
                window['error_bday'].Update('Please enter a valid year\n(e.g. 1999.)')
                window['bday_month'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_bday'].Update('')
                window['bday_month'].Widget.configure(highlightcolor='white')

        if event == 'zipcode' and len(window[event].Get()) >= 1:
            if not re.match('^\d{5}$', window[event].Get()):
                window['error_zipcode'].Update('Please enter a 5 digit zipcode\n(e.g. 15212).')
                window['zipcode'].Widget.configure(highlightcolor='purple', highlightthickness=2)
            else:
                window['error_zipcode'].Update('')
                window['zipcode'].Widget.configure(highlightcolor='white')


    window.close()

    return values


def text_new_alumni_p3():
    frame_church = [[sg.Radio('ACAC', 'church', key='church_acac', enable_events=True),
                     sg.Radio('None', 'church', key='church_none', enable_events=True)],
                     [sg.Radio('Other', 'church', key='church_other', enable_events=True),
                      sg.In(key='church_input')]]

    frame_highschool = [[sg.In(key='highschool', size=(55,1))]]

    frame_college = [[sg.In(key='college', size=(55,1))]]

    frame_job = [[sg.In(key='job', size=(55,1))]]

    frame_health = [[sg.In(key='health', size=(55,1))]]
    
    frame_missing_val = [[sg.T('', key='main_error', 
                               text_color='white', size=(43,1))]]


    layout = [[sg.T('New Alumni - Page 3')],
              [sg.Frame('Church Affiliation *', frame_church)],
              [sg.Frame('Highschool', frame_highschool)],
              [sg.Frame('College', frame_college)],
              [sg.Frame('Occupation', frame_job)],
              [sg.Frame('Special Health Concerns', frame_health)],
              [sg.Frame('Error Checking', frame_missing_val)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel(),
               sg.T('* Required', text_color='red')],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'next_page':
#One of the church options must be selected
            if sum([values['church_acac'], values['church_none'],
                    values['church_other']]) == 0:
                window['main_error'].Update('Please select a church affiliation')
                window['main_error'].Widget.config(background='red')
#If 'Other' church option, then the field must be filled in
            elif (values['church_other'] == True and 
                 len(values['church']) == 0):
                 window['main_error'].Update('Please complete the \'Other\' church field.')
                 window['main_error'].Widget.config(background='red')
#All conditions met, break, go to next page
            elif (sum([values['church_acac'], values['church_none']]) != 0 or
                 (values['church_other'] == True and len(values['church']) != 0)):
                        window['main_error'].Update('')
                        window['main_error'].Widget.config(background='#64778D')   
                        break

        if event in ('church_acac', 'church_none'):
            window['highschool'].SetFocus()

        if event == 'church_other':
            window['church_input'].SetFocus()

    window.close()

    return values


def text_new_alumni_p4():
    frame_parent = [[sg.In(key='parent')]]
    frame_parent_phone = [[sg.In(key='parent_phone1', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='parent_phone2', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='parent_phone3', size=(5,1),
                                 change_submits=True, do_not_clear=True)]]
    frame_parent_email = [[sg.In(key='parent_email')]]
    frame_emergency_contact = [[sg.In(key='e_contact')],
                               [sg.Checkbox('Use Parent/Guardian name from above',
                                            key='e_parent',
                                            enable_events=True)]]
    frame_emergency_phone = [[sg.In(key='e_phone1', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='e_phone2', size=(4,1),
                                 change_submits=True, do_not_clear=True),
                           sg.T('-', pad=(0,0)),
                           sg.In(key='e_phone3', size=(5,1),
                                 change_submits=True, do_not_clear=True)],
                             [sg.Checkbox('Use Parent/Guardian phone number from above',
                                          key='e_number',
                                          enable_events=True)]]
    frame_missing_val = [[sg.T('', key='main_error', 
                               text_color='white', size=(43,1))]]

    layout = [[sg.T('New Alumni - Page 4')],
              [sg.Frame('Parent/Guardian Full Name', frame_parent)],
              [sg.Frame('Parent/Guardian Phone Number', frame_parent_phone)],
              [sg.Frame('Parent/Guardian Email', frame_parent_email)],
              [sg.Frame('Emergency Contact Full Name', frame_emergency_contact)],
              [sg.Frame('Emergency Contact Phone Number', frame_emergency_phone)],
              [sg.Frame('Error Checking', frame_missing_val)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel()],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'next_page':
#Parent Phone Number must be either empty or ###-###-####
            if ((sum([len(values['parent_phone1']),
                       len(values['parent_phone2']),
                       len(values['parent_phone3'])]) != 0) and
                 (len(values['parent_phone1']) !=3 or 
                  len(values['parent_phone2']) !=3 or 
                  len(values['parent_phone3']) !=4)):
                    window['main_error'].Update(
                        'Please complete the Parent/ Guardian Phone Number')
                    window['main_error'].Widget.config(background='red')
#Emergency Phone Number must be either empty or ###-###-####
            elif ((sum([len(values['e_phone1']),
                       len(values['e_phone2']),
                       len(values['e_phone3'])]) != 0) and
                 (len(values['e_phone1']) !=3 or 
                  len(values['e_phone2']) !=3 or 
                  len(values['e_phone3']) !=4)):
                    window['main_error'].Update(
                        'Please complete the Emergency Contact Phone Number')
                    window['main_error'].Widget.config(background='red')
#When all conditions met, break, move to next page
            elif (sum([len(values['parent_phone1']),
                       len(values['parent_phone2']),
                       len(values['parent_phone3'])]) in [0,10] and
                  sum([len(values['e_phone1']),
                       len(values['e_phone2']),
                       len(values['e_phone3'])]) in [0,10]):
                        window['main_error'].Update('')
                        window['main_error'].Widget.config(background='#64778D')  
                        break
            
        if event in ('parent_phone1', 'parent_phone2', 'parent_phone3',
                     'e_phone1', 'e_phone2', 'e_phone3'):
            window[event].Update(re.sub("[^0-9]", "", values[event]))

        if event == 'e_parent':
            window['e_contact'].Update(values['parent'])
        if event == 'e_number':
            window['e_phone1'].Update(values['parent_phone1'])
            window['e_phone2'].Update(values['parent_phone2'])
            window['e_phone3'].Update(values['parent_phone3'])

        if event == 'parent_phone1' and len(window[event].Get()) == 3:
            window['parent_phone2'].SetFocus()
        if event == 'parent_phone2' and len(window[event].Get()) == 3:
            window['parent_phone3'].SetFocus()
        if event == 'parent_phone3' and len(window[event].Get()) == 4:
            window['parent_email'].SetFocus()

        if event == 'e_phone1' and len(window[event].Get()) == 3:
            window['e_phone2'].SetFocus()
        if event == 'e_phone2' and len(window[event].Get()) == 3:
            window['e_phone3'].SetFocus()


    window.close()

    return values

def text_new_alumni_p5():
    frame_options = [[sg.Radio('Yes', 'options', key='options_yes'),
                      sg.Radio('No', 'options', key='options_no')]]

    frame_education = [[sg.Radio('Yes', 'education', key='education_yes'),
                        sg.Radio('No', 'education', key='education_no')]]

    frame_athletics = [[sg.Radio('Yes', 'athletics', key='athletics_yes'),
                        sg.Radio('No', 'athletics', key='athletics_no')]]

    frame_arts = [[sg.Radio('Yes', 'arts', key='arts_yes'),
                    sg.Radio('No', 'arts', key='arts_no')]]
    
    frame_missing_val = [[sg.T('', key='main_error', 
                               text_color='white', size=(43,1))]]


    layout = [[sg.T('New Alumni - Page 5')],
              [sg.Frame('Options? *', frame_options)],
              [sg.Frame('Education? *', frame_education)],
              [sg.Frame('Athletics? *', frame_athletics)],
              [sg.Frame('Performing Arts? *', frame_arts)],
              [sg.Frame('Error Checking', frame_missing_val)],
              [sg.Button('Finish', key='finish', size=(15,1)), sg.Cancel(),
               sg.T('* Required', text_color='red')],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'finish':
#Each option must have a choice selected
            if sum([values['options_yes'], values['options_no'],
                    values['education_yes'], values['education_no'],
                    values['athletics_yes'], values['athletics_no'],
                    values['arts_yes'], values['arts_no']]) in [0,1,2,3]:
                        window['main_error'].Update(
                            'Please select one option for each field above')
                        window['main_error'].Widget.config(background='red')
#When all conditions met, break, complete import
            elif    sum([values['options_yes'], values['options_no'],
                         values['education_yes'], values['education_no'],
                         values['athletics_yes'], values['athletics_no'],
                         values['arts_yes'], values['arts_no']]) == 4:
                            window['main_error'].Update('')
                            window['main_error'].Widget.config(background='#64778D') 
                            break

    window.close()

    return values


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