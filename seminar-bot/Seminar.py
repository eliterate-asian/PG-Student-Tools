import time
from datetime import datetime
import pathlib
from pynput.keyboard import Controller, Key
import webbrowser
import csv
import os

# NOTES
# Sounds worse than it - well no, actually, this is I guess basically cheating.
# INSTRUCTIONS
# Make sure you have your Zoom settings as follows:
# - "Check before joining meeting" (this one usually shows up as that dialog box when you click an invite link): OFF
# - "Check before leaving meeting" : OFF
# - "Mute Mic when joining meeting" : ON
# - "Auto join Audio Settings" : ON (I prefer to leave mine off actually, but to each their own)  
# Change your itinerary with the meetings csv file. I like to use Google Sheets (I just import, update, than export) but you can use
# Excel if you're cool like that. Or Wordpad if you're hardcore. Just make sure that:
# All meetings are individually added to their OWN LINE with the format: MeetingLink,StartTime,EndTime,Date
# -- Where Times are in HH:MM format, 24 hour format and Date is in MM-DD-YY format. 
# All entries should be organized by datetime (earliest meetings first, regardless of course ID). Simultaneous meetings aren't handled. Good luck there. 

home = pathlib.Path(__file__).parent.resolve()

with open(str(home) + '\meetings.csv', 'r') as file:
    csv_reader = csv.reader(file)
    meetings = []
    for i in csv_reader:
        meetings.append(i)


keyboard = Controller()

isStarted = False

for i in meetings:

    # TODO Add functionality to skip complete same day meetings (in the event the script is rerun same day)
    if datetime.now().month != int(i[3].split('-')[0]) or datetime.now().day != int(i[3].split('-')[1]):
        print("Skipping entry for:", i[1], "to", i[2], "on", i[3])
        continue
    
    print("Pending entry for:", i[1], "to", i[2], "on", i[3])
    while True:
        if not isStarted:
            # Check for starttime, then start if ready

            # This accounts for minutes where the starttime is on th hour (because "-10" aint a valid minute)
            mincheck = 50 if (int(i[1].split(':')[1]) - 10) < 0 else (int(i[1].split(':')[1]) - 10)
            hourcheck = (int(i[1].split(':')[0]) - 1) if (int(i[1].split(':')[1]) - 10) < 0 else int(i[1].split(':')[0])
            threshhold = int((hourcheck*60)+mincheck)
            if ((datetime.now().hour*60) + datetime.now().minute) >= threshhold:
            

                duration = (((int(i[2].split(':')[0]) * 60) + int(i[2].split(':')[1])) - ((datetime.now().hour*60) + datetime.now().minute))
                watch = datetime.now()
                print("[", watch, "] Have a good meeting! Sleeping for", duration, "minutes.")
                isStarted = True
                if (duration > 0):
                    webbrowser.open(i[0])
                    time.sleep((duration * 60) - 30 )
                    print("[INFO] *yawn* Good morning!")
                else:
                    print("Nope")
                    print(isStarted)
                    continue


        else:
            # Leave the meeting using short cut (set to default) The shortcut is a shotgun.
            if datetime.now().hour >= int(i[2].split(':')[0]) and datetime.now().minute >= int(i[2].split(':')[1]):
                print("[INFO] Executing the heretics. Please standby.")
                os.system("taskkill /im Zoom.exe /f")
                time.sleep(1)
                keyboard.press(Key.enter)
                isStarted = False
                break
            else:
                time.sleep(10)
        deficit = ((int(i[1].split(':')[0])*60)+int(i[1].split(':')[1]) - ((datetime.now().hour*60)+datetime.now().minute))
        print("[INFO] The meeting is", deficit, "minutes ahead. This helper will be napping until closer to the starttime of the meetings. Honk shoo mi mi mi...")
        if (deficit <= 10):

            print("Preparing to launch... Standby with your Student Browser Active.")
            time.sleep(5)
            print("Launching.")
        
        else:
            print("Sleeping for", (deficit - 10), "minutes...")
            time.sleep((deficit - 10)*60)