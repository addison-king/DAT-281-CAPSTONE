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
    values_page_1 = text_new_alumni_p5()
    print(values_page_1)


def text_new_alumni_p5():
    frame_options = [[sg.Radio('Yes', 'options'),
                      sg.Radio('No', 'options')]]

    frame_education = [[sg.Radio('Yes', 'education'),
                        sg.Radio('No', 'education')]]

    frame_athletics = [[sg.Radio('Yes', 'athletics'),
                        sg.Radio('No', 'athletics')]]

    frame_arts = [[sg.Radio('Yes', 'arts'),
                    sg.Radio('No', 'arts')]]


    layout = [[sg.T('New Alumni - Page 5')],
              [sg.Frame('Options?', frame_options)],
              [sg.Frame('Education?', frame_education)],
              [sg.Frame('Athletics?', frame_athletics)],
              [sg.Frame('Performing Arts?', frame_arts)],
              [sg.Button('Next Page', key='next_page', size=(15,1)), sg.Cancel()],
              ]

    window = sg.Window('UIF: Alumni Database', layout)

    while True:
        event, values = window.read()

        if event in ('Cancel', sg.WIN_CLOSED):
            values = None
            break
        if event == 'next_page':
            break

    window.close()

    return values




if __name__ == "__main__":
    main()