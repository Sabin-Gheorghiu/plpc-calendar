# Auth: Sabin
# Purpose: Extract calendar entries, put them in a CSV and show a screen to user with the bins and percentages
#Calendar entries are like this: Client X Part:A (colour is tomato) = > Part A which was not held
#
#









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
from tkinter import *
import tkcalendar
from datetime import timedelta










# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

app_creds_dictionary = {"installed":{"client_id":"155870693121-bnvget35duihk36lq1mp5db7qlgs435v.apps.googleusercontent.com","project_id":"plpc-calendar","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}

#credentials_gapi = ServiceAccountCredentials.from_json_keyfile_dict(app_creds_dictionary, SCOPES)



def get_events_and_put_in_bins():
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
        # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # last_month = datetime.datetime.utcnow() + relativedelta(months=-1)

        # time_extract = last_month.isoformat() + 'Z'
        # print(now)
        # print(time_extract)
        # print('Getting the events from: ', last_month)
      

        time_from =  datetime.datetime.combine(date1.get_date(), 
                          datetime.time(0, 0)).isoformat() + 'Z'
        time_to =  datetime.datetime.combine(date2.get_date(), 
                          datetime.time(0, 0)).isoformat()  + 'Z'

        print("Extracting from %s to %s" % (time_from,time_to))
        events_result = service.events().list(calendarId='primary', 
                                              timeMin=time_from,
                                              timeMax= time_to,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No events found.')
            return

        # Generate the title
        line_for_csv = 'Time,Summary,ColourID, PC code\n'
        print(line_for_csv)
        append_csv (line_for_csv)
        
        pie_chart_categories = []


        a = [0 for key in google_calendar_colour_dict]
        for key in unique_tags_dict:
            unique_tags_dict[key].extend(a) #addd the array of categories

            
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_colour = event.get('colorId')
            line_for_csv = '%s,%s,%s,%s\n' % (start, event['summary'], event.get('colorId'),google_calendar_colour_dict[event_colour][2])
            #print(line_for_csv)
            append_csv (line_for_csv)

            #print(google_calendar_colour_dict[event_colour][0]) --THIS GIVE RGB CODE
            pie_chart_labels_percentages.append(event_colour)
            if event_colour not in pie_chart_categories:
                pie_chart_categories.append(event_colour)
                pie_chart_colours.append(google_calendar_colour_dict[event_colour][0])
            
            for key in unique_tags_dict:
                #for each key add categories as positions in array
                if key in event['summary']:
                    print (key, event['summary'])
                    if event_colour == None:
                        event_color_index = 1
                    else:
                        event_color_index = event_colour+1
                    unique_tags_dict[key][event_color_index]+=1
                      

        print("Interesting events:", unique_tags_dict)
        text_result.insert(INSERT,unique_tags_dict)
        no_labels = len(pie_chart_categories)
        print("There are %d lables " % no_labels)
        for i in pie_chart_categories:
            pie_chart_sizes.append(pie_chart_labels_percentages.count(i))
        
        #redo the labels with the names of the color from the dict
        for i in pie_chart_categories:
            pie_chart_labels.append(google_calendar_colour_dict[i][1])
    
    
    except HttpError as error:
        print('An error occurred: %s' % error)




name_csv =  datetime.datetime.utcnow().isoformat() + 'events.csv'





#Create an instance of Tkinter frame
win = Tk()
win.title('PLPC Extractor by SG')

#Set the geometry of tkinter frame
win.geometry("750x250")
pie_chart_labels_percentages = []
pie_chart_labels = []
pie_chart_colours = []
pie_chart_sizes = []

def graph():
    # pie_chart_labels = 'Done', 'In progresss', 'Not sure'
    # pie_chart_sizes = [45,20,35]
    # plt.subplot(1,2,1)
    # fig1 = plt.figure()
    # plt.pie(pie_chart_sizes, labels=pie_chart_labels,colors=pie_chart_colours)
    # plt.title("pie chart")

    plt.subplot(1,1,1) #second plot
    N = 3 #3 categories (PA,PC,PS)
    ind = np.arange(N) # the x locations for the groups
    width = 0.35
    done = (20, 35, 30)
    notdone = (25, 32, 34)
    not_sure = (20, 35, 30)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(ind, done, width, color='b')
    ax.bar(ind, notdone, width,bottom=done, color='r')
    ax.bar(ind, not_sure, width,bottom=notdone, color='g')
    ax.set_ylabel('No of meetings')
    ax.set_title('State of meetings by Part and state')
    # # ax.set_xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    # # ax.set_yticks(np.arange(0, 81, 10))
    # ax.legend(labels = unique_tags_dict.values()[0])

    plt.show()



def append_csv(line):
    with open(name_csv, 'a') as f_object:

        f_object.write(line)
    
        # Close the file object
        f_object.close()




#dict has the key as color code that the API replies with. The value for each key is an array with first the RGB color then the colour definition and then Paul's color code for events
#Fiecare PART: Verde daca s-au tinut, Albastru este undefined, Rosu daca nu, Flamingo pentru reprogramat

google_calendar_colour_dict = {
    None : ['#039be5', "DefaultBlue", "Future"],
    "1" : ['#7986cb', "Lavender", "Lavender"], #Unknown so use color 
    "2" : ['#33b679', "Sage","Sage"],
    "3" : [ '#8e24aa', "Grape", "Grape"],
    "4" :  ['#e67c73', "Flamingo", "Rescheduled"],
    "5" :  ['#f6c026', "Banana", "Banana"],
    "6" :  ['#f5511d', "Tangerine", "Tangerine"],
    "7" :  ['#039be5', "Peacock", "Peacock"],
    "8" :  ['#616161', "Graphite", "Graphite"],
    "9" :  ['#3f51b5', "Blueberry", "Blueberry"],
    "10" : ['#0b8043',  "Basil", "Held"],
    "11" :  ['#d60000', "Tomato", "Not Held"]
    
}

unique_tags_dict ={
    "P:A" : ["Initial Financial Analysis"],
    "P:C" : ["Financial Consultation"],
    "P:S" : ["Sign Off"],
}

text_about = Text(win,height=4, width=100)
text_dates = Text(win,height=4, width=100)
text_result = Text(win,height=4, width=100)


def date_range(start,stop):
    global dates # If you want to use this outside of functions
     
    dates = []
    diff = (stop-start).days
    for i in range(diff+1):
        day = start + timedelta(days=i)
        dates.append(day)
    if dates:
        print(start,stop) # Print it, or even make it global to access it outside this
        text_dates.insert(INSERT, "\nWill use: from %s to %s" % (start,stop))
    else:
        print('Make sure the end date is later than start date')
        text_dates.insert(INSERT,'\nMake sure the end date is later than start date')

    get_events_and_put_in_bins()



def about_command():
    text_about.insert(INSERT,'\n A small utility to get Calendar entries from Google API and sort them into encoded categories. \
                                Written by Sabin Gheorghiu for Paul Cuc')

Button(win, text= "About", command=about_command).pack(pady=20)
text_about.pack(padx=10,pady=10) #pack the text here

date1 = tkcalendar.DateEntry(win)
date1.pack(padx=10,pady=10)

date2 = tkcalendar.DateEntry(win)
date2.pack(padx=10,pady=10)

Button(win,text='Find Range',command=lambda: date_range(date1.get_date(),date2.get_date())).pack()

text_dates.pack(padx=10,pady=10) #pack the text here

#Create a button to show the plot
Button(win, text= "Show Graph", command= graph).pack(pady=20)

text_result.pack(padx=10,pady=10)



def main():
    win.mainloop()


if __name__ == '__main__':
    main()