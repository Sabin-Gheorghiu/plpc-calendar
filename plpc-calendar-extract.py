# Auth: Sabin
# Purpose: Extract calendar entries, put them in a CSV and show a screen to user with the bins and percentages


#### This is for the calendar utility imports 
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from google.auth import ServiceAccountCredentials

# This is for the graphing part
#Import the required Libraries
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

#This is for the relative date
from datetime import date
from dateutil.relativedelta import relativedelta




#Create an instance of Tkinter frame
win= Tk()
win.title('PLPC Extractor')

#Set the geometry of tkinter frame
win.geometry("750x250")
pie_chart_labels_percentages = []
pie_chart_labels = []
pie_chart_colours = []
pie_chart_sizes = []

def graph():
    # pie_chart_labels = 'Done', 'In progresss', 'Not sure'
    # pie_chart_sizes = [45,20,35]
    plt.pie(pie_chart_sizes, labels=pie_chart_labels,colors=pie_chart_colours)
    plt.show()


#Create a button to show the plot
Button(win, text= "Show Graph", command= graph).pack(pady=20)



def append_csv(line):

    with open('events.csv', 'a') as f_object:

        f_object.write(line)
    
        # Close the file object
        f_object.close()



google_calendar_colour_dict = {
    None : ['#039be5', "DefaultBlue"],
    "1" : ['#7986cb', "Lavender"],
    "2" : ['#33b679', "Sage"],
    "3" : [ '#8e24aa', "Grape"],
    "4" :  ['#e67c73', "Flamingo"],
    "5" :  ['#f6c026', "Banana"],
    "6" :  ['#f5511d', "Tangerine"],
    "7" :  ['#039be5', "Peacock"],
    "8" :  ['#616161', "Graphite"],
    "9" :  ['#3f51b5', "Blueberry"],
    "10" : ['#0b8043',  "Basil"],
    "11" :  ['#d60000', "Tomato"]
    
}



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

app_creds_dictionary = {"installed":{"client_id":"155870693121-bnvget35duihk36lq1mp5db7qlgs435v.apps.googleusercontent.com","project_id":"plpc-calendar","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}

#credentials_gapi = ServiceAccountCredentials.from_json_keyfile_dict(app_creds_dictionary, SCOPES)


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                app_creds_dictionary, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        last_month = datetime.datetime.utcnow() + relativedelta(months=-1)

        time_extract = last_month.isoformat() + 'Z'
        print(now)
        print(time_extract)
        print('Getting the events from: ', last_month)
        events_result = service.events().list(calendarId='primary', timeMin=time_extract,
                                              maxResults=350, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No events found.')
            return

        # Prints the start and name of the next 10 events
        # Generate the title
        line_for_csv = 'Time,Summary,Colour\n'
        print(line_for_csv)
        append_csv (line_for_csv)
        
        pie_chart_categories = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            line_for_csv = '%s,%s,%s\n' % (start, event['summary'], event.get('colorId'))
            event_colour = event.get('colorId')
            print(line_for_csv)
            append_csv (line_for_csv)

            print(google_calendar_colour_dict[event_colour][0])
            pie_chart_labels_percentages.append(event_colour)
            if event_colour not in pie_chart_categories:
                pie_chart_categories.append(event_colour)
                pie_chart_colours.append(google_calendar_colour_dict[event_colour][0])
        
        no_labels = len(pie_chart_categories)
        print("There are %d lables " % no_labels)
        for i in pie_chart_categories:
            pie_chart_sizes.append(pie_chart_labels_percentages.count(i))
        
        #redo the labels with the names of the color from the dict
        for i in pie_chart_categories:
            pie_chart_labels.append(google_calendar_colour_dict[i][1])


        win.mainloop()


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()