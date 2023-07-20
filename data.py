# Extract Calendar information from UCD Schedule Builder
import undetected_chromedriver as uc
import tkinter as tk
import requests
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def submit_password(driver):
    user_password = entry.get()
    password = driver.find_element(By.ID, "password")
    password.send_keys(user_password)
    root.destroy()

# Step 1: Go to the URL
url = "https://my.ucdavis.edu/schedulebuilder/"

# Check if URL is valid
response = requests.get(url)
if response.status_code == 404:
    raise ValueError('Requested resource not found (404 Not Found)')
elif response.status_code != 200:
    raise ValueError(f"Server returned status code: {response.status_code}")

service = Service('C://Program Files//chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get(url)

# Step 2: Login using UCD Credentials. If invalid, application access should be denied
un = input("Please type in your username: ")
username = driver.find_element(By.ID, "username")
username.send_keys(un)

# Create the tkinter password input window
root = tk.Tk()
root.title("Password Input")
root.geometry("300x100")

label = tk.Label(root, text="Enter your password:")
label.pack()

entry = tk.Entry(root, show="*")
entry.pack()

button = tk.Button(root, text="Submit", command=lambda: submit_password(driver))
button.pack()

root.mainloop()

# Submit user entry
# TODO: INCORRECT USER INPUT
driver.find_element(By.NAME, "submit").click()

wait = WebDriverWait(driver, 60)
wait.until(EC.url_contains('https://my.ucdavis.edu/schedulebuilder/index.cfm'))

# EMPLOY ERROR MANAGEMENT

# Step 3: Employ Web Scrape to take information in the following manner:
# Select the term you are searching for
term = 'TermSelect1'

term_str = []
available_terms = []

div_elements = driver.find_elements(By.TAG_NAME, 'div')

for div_element in div_elements:
    if div_element.get_attribute('name') == term:
        term_str.append(div_element.text)

print("Select the term you wish to view: ")

# take text after ...
# split by /n
# if there are multiple /n stop
available_terms = term_str[0].split('\n')

# clean up whitespace and unnecessary terms for proper formatting
for i in range(9):
    available_terms.pop(i)

for i in range(5):
    available_terms.pop()
    
for i in range(1, len(available_terms)):
    print(available_terms[i]+"["+str(i)+"]")

selected_term = input("Please input the number associated with your selection: ")
# ERROR MANAGEMENT FOR INCORRECT ENTRIES

# automatically select the entry associated with the number
if (selected_term == "1"):
    translated_val = 202310
elif (selected_term == "2"):
    translated_val = 202309
elif (selected_term == "3"):
    translated_val = 202308
elif (selected_term == "4"):
    translated_val = 202307
elif (selected_term == "5"):
    translated_val = 202306
elif (selected_term == "6"):
    translated_val = 202305
elif (selected_term == "7"):
    translated_val = 202303
else:
    raise ValueError("Your term value input was invalid.")

select_term = 'termCode1'
select = Select(driver.find_element(By.NAME, select_term))
select.select_by_value(str(translated_val))
driver.find_element(By.XPATH,"//button[@class='btn btn-primary']").click()

# a) Look for all divs called classTitle height-justified. Store in list
# b) Immediately after classTitle look for div called meeting clearfix.
# Scrape all text within the div
wait = WebDriverWait(driver, 15)
wait.until(EC.url_contains('https://my.ucdavis.edu/schedulebuilder/index.cfm?termCode='))

# Find all the buttons that show important details for each course
buttons = driver.find_elements(By.XPATH, "//button[contains(@title, 'Show Course Important Details')]")

# formatting tracker for discarding extra and invalid entries
tracker = 0

# Loop through the buttons and click them one by one
with open("output.txt", "w") as file:
    for button in buttons:
        if (tracker >= 6):
            break
        try:
            # Scroll the element into view before clicking
            driver.execute_script("arguments[0].scrollIntoView(true);", button)

            # Click the button using JavaScript
            driver.execute_script("arguments[0].click();", button)

            # Wait for the details to become visible
            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'meeting')][contains(., 'Lecture')]")))

            # Now you can scrape the lecture and discussion information
            course_details = button.find_element(By.XPATH, "./ancestor::div[@class='CourseItem gray-shadow-border clearfix']")
            course_title = course_details.find_element(By.CLASS_NAME, "classTitle").text
            lecture_info = course_details.find_element(By.XPATH, ".//div[contains(@class, 'meeting')][contains(., 'Lecture')]").text

            if (tracker % 2 == 1):
                file.write("Course Title: " + course_title + "\n")
                file.write("Lecture Info: " + lecture_info + "\n")
                
            tracker += 1

        except Exception as e:
            print(f"Failed to process course: {e}")
            
# Close the driver and browser window after processing
driver.quit()
