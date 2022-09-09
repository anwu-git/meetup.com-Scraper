from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By

# initiating the webdriver, add headless option for dynamic content
service = ChromeService(executable_path=ChromeDriverManager().install())
options = Options()
options.headless = True
driver = webdriver.Chrome(service=service)

# open L-night group on meetup.com
driver.get("https://www.meetup.com/lnightberlin/events/past/")
driver.implicitly_wait(0.5)

# log in to access past events
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

events = driver.find_elements(By.CLASS_NAME, "eventCardHead")

# write results to a text file
textfile = open("events.txt", "w", encoding="utf-8")
for element in events:
    textfile.write(element.text + "\n\n")
textfile.close()

time.sleep(10)