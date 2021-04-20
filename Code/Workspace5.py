from pathlib import Path
import os
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd
import uuid
import PySimpleGUI as sg
import re

def main():
    print()
    values_page_1 = text_new_alumni_p2()
    print(values_page_1)


def text_new_alumni_p2():
    frame_gender = [[sg.Radio('Female', 'gender', key='gender_female', default=True), 
                     sg.Radio('Male', 'gender', key='gender_male')]]
    frame_street_ad = [[sg.Input(key='street_address')]]
    frame_city = [[sg.Radio('Pittsburgh', 'city', key='city_pgh', default=True),
                   sg.Radio('Other', 'city', key='city_other')]]

    layout = [[sg.T('New Alumni - Page 2')],
              [sg.Frame('Gender', frame_gender)],
              [sg.Frame('Street Address', frame_street_ad)],
              [sg.Frame('City', frame_city)]]
    
    window = sg.Window('UIF: Alumni Database', layout)
    while True:
        event, values = window.read()

        if event in ('OK', 'Cancel', sg.WIN_CLOSED):
            break







if __name__ == "__main__":
    main()