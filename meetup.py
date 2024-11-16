# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# How to use:
#
# Create a file called creds.txt in the same folder where the 1st line is the e-mail of your MeetUp
# account and the 2nd one your password. An account is needed to to access past MeetUp events.
# Don't upload this file to GitHub ever, obviously.
#
# This script will open a Chrome window and keep scrolling to the end of the page until all events are loaded.
# It will then save all events in the file events.txt in the following line format:
# 1. Time + Date
# 2. Event Title
# 3. Junk
# 4. Empty Line
#
# At the current time MeetUp does not list the locations anymore in these results but these can be parsed
# easily from within the text.
#
# <16-Nov-2024>
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from seleniumbase import Driver
import time


### Access events on MeetUp
# Initiate the webdriver
driver = Driver()

# Open L-night's past events page
driver.get("https://www.meetup.com/lnightberlin/events/past/")
driver.implicitly_wait(0.5)

# Log in to access past events
with open("creds.txt") as f:
    creds = f.readlines()

userid = creds[0]
username = driver.find_element("id","email")
username.send_keys(userid)

pw = creds[1]
password = driver.find_element("id","current-password")
password.send_keys(pw)

driver.find_element("name","submitButton").click()

time.sleep(1)


### Keep scrolling to the end of the page until all past events have been loaded
# Get scroll height after first time page load
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1300);")
    # Wait to load page
    time.sleep(2)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    # Finish when no new content is being loaded


### Select all elements and save them
# This will select all events on this page by their classes "flex w-full flex-col space-y-3", including our desired group events and some unwanted suggested events at the end of the page.
all_events = driver.find_elements(".flex.w-full.flex-col.space-y-3")
    
# We'll filter out the unwanted suggested events by their parent classes "li.w-full min-w-\[300px\]" and exclude them by their number of elements at the end of our result list.
unwanted_events = driver.find_elements("li.w-full.min-w-\[300px\]")
group_events = all_events[:-len(unwanted_events)]

# Write results to a text file
textfile = open("events.txt", "w", encoding="utf-8")
for element in group_events:
    textfile.write(element.text + "\n\n")
textfile.close()

time.sleep(3)