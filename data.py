# Extract Calendar information from UCD Schedule Builder
import tkinter as tk
import requests
import json
import PyPDF2, re
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def clear_entry():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    username_entry.focus_set()

def handle_login(driver, root):
    un = username_entry.get()
    pw = password_entry.get()

    username = driver.find_element(By.ID, "username")
    username.send_keys(un)

    password = driver.find_element(By.ID, "password")
    password.send_keys(pw)  # Corrected variable name to 'pw'

    # Submit user entry
    driver.find_element(By.NAME, "submit").click()

    wait = WebDriverWait(driver, 60)
    wait.until(EC.url_contains('https://my.ucdavis.edu/schedulebuilder/index.cfm'))

    error_msg = "Invalid credentials. Please make sure Caps Lock is not on."
    
    root.destroy()

# Reformat time
def reformat_time(old_time):
    tokens = old_time.split(' ')
    
    if (tokens[0] == ''):
        tokens.pop(0)
    
    time = tokens[0]
          
    if (tokens[1] == 'PM' and time.split(':')[0] != '12'):
        times = tokens[0].split(':')
        new_time = int(times[0])
        new_time += 12
        time = str(new_time) + ':' + str(times[1])
    
    return time

# Convert time to PST
def convert_time(old_time):
    times = old_time.split('-')
    start_time = times[0]
    start_time = reformat_time(start_time)
    end_time = times[1]
    end_time = reformat_time(end_time)

    return start_time, end_time

def get_URL():
    # Step 1: Go to the URL
    url = "https://my.ucdavis.edu/schedulebuilder/"

    # Check if URL is valid
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError('Requested resource not found (404 Not Found)')
    elif response.status_code != 200:
        raise ValueError(f"Server returned status code: {response.status_code}")
    
    return url

def fetch_driver(url):
    # TODO: Automatically fetch & download driver in target area that corresponds to current Chrome version
    service = Service('C://Program Files//chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    return driver


def login(driver):
    global username_entry, password_entry # Declare as global variables
    root = tk.Tk()
    root.title('Login to UCD Schedule Builder')
    root.geometry('750x550')
    root.configure(bg='#022851')
    root.bind('<Return>', lambda event: handle_login(driver, root))

    frame = tk.Frame(bg='#022851')
    login_label = tk.Label(frame, bg='#022851', fg='#FFFFFF', text='Login using your UCD Credentials', font=("Times New Roman", 30))
    username_label = tk.Label(frame, text='Username', bg='#022851', fg='#FFFFFF', font=("Times New Roman", 16))
    password_label = tk.Label(frame, text='Passphrase', bg='#022851', fg='#FFFFFF', font=("Times New Roman", 16))

    username_entry = tk.Entry(frame, font=("Times New Roman", 16))
    password_entry = tk.Entry(frame, show="*", font=("Times New Roman", 16))

    login_button = tk.Button(frame, text="Login", bg="#FFBF00", fg="#FFFFFF", command=lambda event: handle_login(driver, root), font=("Times New Roman", 16))

    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    frame.pack()

    root.mainloop()

    wait = WebDriverWait(driver, 60)
    wait.until(EC.url_contains('https://my.ucdavis.edu/schedulebuilder/index.cfm'))

def select_terms(driver):
    # Select the term you are searching for
    term = 'TermSelect1'
    selectname = 'termCode1'

    term_str = []
    options = []
    available_terms = []

    div_elements = driver.find_elements(By.TAG_NAME, 'div')
    select_element = driver.find_element(By.NAME, 'termCode1')

    for div_element in div_elements:
        if div_element.get_attribute('name') == term:
            term_str.append(div_element.text)

    select = Select(select_element)

    # Extract option values
    options = [option.get_attribute('value') for option in select.options if option.get_attribute('value')]

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
    # available_terms[selected_term - 1] is the selection

    # automatically select the entry associated with the number
    if (selected_term == "1"):
        translated_val = options[0]
    elif (selected_term == "2"):
        translated_val = options[1]
    elif (selected_term == "3"):
        translated_val = options[2]
    elif (selected_term == "4"):
        translated_val = options[3]
    elif (selected_term == "5"):
        translated_val = options[4]
    elif (selected_term == "6"):
        translated_val = options[5]
    elif (selected_term == "7"):
        translated_val = options[6]
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

    return buttons, available_terms, selected_term

# PDF Parser 
# Read contents of PDF File into a list, tokenized by word 
# Sort through the list for the keyword
# Read contents immediately after keyword: we are looking for 'Instruction begins'
def parsePDF(compared_term):
    # Open the PDF file
    pdfFileObj = open('calendar-master-2023-2024.pdf', 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # Extract text from all pages and concatenate it into one string
    text = ""
    for page in pdfReader.pages:
        text += page.extract_text()

    # Tokenize the text into words (split by space or newline)
    words = re.split(r'\s+|\\n', text)

    # Filter out empty strings and other non-word characters
    words = [word for word in words if re.match(r'^\w', word)]

    # split up compared term into a list for comparison
    compared_terms = compared_term.split(' ')

    # when scanning the file, keep a boolean value that tracks if the compared term has been passed yet
    scan = False

    for i in range(len(words) - 4):
        if (words[i] == compared_terms[0] and words[i + 1] == compared_terms[1]):
            scan = True
        if (scan and words[i] == 'Instruction' and words[i + 1] == 'Begins'):
            start_day = words[i + 2]
            start_date = words[i + 3]
            break

    # Close the PDF file
    pdfFileObj.close()

    # the keyword was not found in the scan
    if (scan == False):
        raise ValueError('Could not find your selection in the current PDF. Try going to https://registrar.ucdavis.edu/calendar/web/master and downloading the latest version into your working repository.')

    return start_day, start_date

def daysToVals(quarter_start_day):
    if (quarter_start_day == 'M'):
        start_day = 1
    elif (quarter_start_day == 'T'):
        start_day = 2
    elif (quarter_start_day == 'W'):
        start_day = 3
    elif (quarter_start_day == 'R'):
        start_day = 4
    elif (quarter_start_day == 'F'):
        start_day = 5
    else:
        start_day = 0
    
    return start_day

def calculateDate(quarter_start_day, quarter_start_date, lecture_start_day, year):
    # Convert the days into values
    start_day = daysToVals(quarter_start_day)
    target_day = daysToVals(lecture_start_day)

    # Take the difference
    if (target_day > start_day):
        difference = target_day - start_day
    else:
        difference = 7 - start_day - target_day
    
    date_vals = quarter_start_date.split('/')
    day = date_vals[1]
    month = date_vals[0]

    # Add difference to date

    # February
    if (int(day) + difference > 29 and month == '2' and int(year) % 4 == 0):
        # Leap Year
        month = '3'
        overlap = difference - (29 - int(day))
        day = str(overlap)

    elif (int(day) + difference > 28 and month == '2'):
        month = '3'
        overlap = difference - (28 - int(day))
        day = str(overlap)
    
    # 30 Day Months: April (4), June (6), September (9), November (11)
    elif (int(day) + difference > 30 and (month == '4' or month == '6' or month == '9' or month == '11')):
        month = int(month) + 1
        month = str(month)

        overlap = difference - (30 - int(day))
        day = str(overlap)

    # 31 Day Months
    elif (int(day) + difference > 31 and (month == '1' or month == '3' or month == '5' or month == '7' or month == '8' or month == '10' or month == '12')):
        month = int(month) + 1
        month = str(month)

        overlap = difference - (31 - int(day))
        day = str(overlap)

        # December
        if (month == '12'):
            year = int(year) + 1
            year = str(year)

    # Simply add Difference
    else:
        day = int(day) + difference
        day = str(day)

    date = year + '-' + month + '-' + day

    return date

def get_results(buttons, driver, available_terms, selected_term):
    # formatting tracker for discarding extra and invalid entries
    tracker = 0
    course_info_list = []
    # Prompt users for email entries
    primary_email = input("Please enter in an email address: ")
    secondary_email = input("Enter in a secondary email. If you don't have one, just press Enter: ")

    # TODO: Look at classes with 1 and 3 units that may not have discussion sections or multiple lectures

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
                # Find the "Final Exam" div element and extract the text
                finals_element = course_details.find_element(By.XPATH, ".//div[contains(.//span[@class='boldTitle'], 'Final Exam:')]")
                finals_info = finals_element.text.strip().split(": ")[1]
                
                if (tracker % 2 == 1):
                    discussion_session = True

                    # parse lecture_info by \n or space
                    lecture = lecture_info.split('\n')
                    finals = finals_info.split(' ')

                    # error checking
                    if len(lecture) < 8:
                        discussion_session = False
                
                    # Account for more scenarios with more functions
                    if ((len(lecture) < 8 or len(finals) < 2) and discussion_session):
                        # if discussion info is simply not available
                        raise IndexError('Parsed information is not formatted properly.')

                    # Parse Data
                    # Get the first day of instruction for the quarter selected: available_terms[selected_term - 1]
                    # If after 2024, go to https://registrar.ucdavis.edu/calendar/web/master and download the pdf for use here
                    comparable_terms = available_terms[int(selected_term)].split(" ")
                    if (len(comparable_terms) < 10):
                        raise IndexError('Term information is not readable')
                    compared_term = comparable_terms[7] + " " + comparable_terms[9]

                    quarter_start_day, quarter_start_date = parsePDF(compared_term)

                    # Lecture Scheduling
                    for i in range(len(lecture[2])):
                        # convert time to PST
                        conversion = convert_time(lecture[1])
                        start_time = conversion[0]
                        end_time = conversion[1]
                        lecture_date = calculateDate(quarter_start_day, quarter_start_date, lecture[2][i], comparable_terms[9])

                        course_info = {
                            "summary": course_title + " Lecture",
                            "location": lecture[3],
                            "description": "lecture",
                            "start": {
                                "dateTime": lecture_date + 'T' + start_time + ':00-07:00',
                                "timeZone": "America/Los_Angeles"
                            },
                            "end": {
                                "dateTime": lecture_date + 'T' + end_time + ':00-07:00',
                                "timeZone": "America/Los_Angeles"
                            },
                            "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=10"],
                            "attendees": [
                            { "email": primary_email },
                            { "email": secondary_email }
                        ],
                        # I'm not sure what the minutes part below means, but will prompt below
                        "reminders": {
                            "useDefault": False,
                            "overrides": [
                            { "method": "email", "minutes": 1440 },
                            { "method": "popup", "minutes": 10 }
                            ]
                        }
                        }
                        course_info_list.append(course_info)
                    
                    # Discussion Scheduling
                    # convert time to PST
                    if (discussion_session):
                        conversion = convert_time(lecture[5])
                        start_time = conversion[0]
                        end_time = conversion[1]
                        discussion_date = calculateDate(quarter_start_day, quarter_start_date, lecture[6], comparable_terms[9])

                        course_info = {
                            "summary": course_title + " Discussion",
                            "location": lecture[7],
                            "description": "discussion",
                            "start": {
                                "dateTime": discussion_date + 'T' + start_time + ':00-07:00',
                                "timeZone": "America/Los_Angeles"
                            },
                            "end": {
                                "dateTime": discussion_date + 'T' + end_time + ':00-07:00',
                                "timeZone": "America/Los_Angeles"
                            },
                            "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=10"],
                            "attendees": [
                            { "email": primary_email },
                            { "email": secondary_email }
                        ],
                        # I'm not sure what the minutes part below means, but will prompt below
                        "reminders": {
                            "useDefault": False,
                            "overrides": [
                            { "method": "email", "minutes": 1440 },
                            { "method": "popup", "minutes": 10 }
                            ]
                        }
                        }

                        course_info_list.append(course_info)

                    # Finals Scheduling
                    finish_times = finals[1].split(':')
                    prefix = finals[2]
                    finish_time = int(finish_times[0]) + 2

                    # Switch am and pm after noon and midnight
                    if (finish_time >= 12 and int(finish_times[0]) < 12):
                        if (prefix == 'AM'):
                            prefix == 'PM'
                        else:
                            prefix == 'AM'
                
                    final_finish = str(finish_time) + ':' + finish_times[1]

                    date_str = finals[0].split('/')
                    year = date_str[2]
                    month = date_str[0]
                    day = date_str[1]

                    date = day + '-' + month + '-' + year

                    # Finals Scheduling
                    course_info = {
                        "summary": course_title + " Finals",
                        "location": "",
                        "description": "finals",
                        "Final Date": finals[0],
                        "Final Time": date + "T" + reformat_time(finals[1] + " " + finals[2]),
                        "Finals End": date + "T" + reformat_time(final_finish + " " + prefix),
                    }

                    course_info_list.append(course_info)
                    file.write("Course Title: " + course_title + "\n")
                    file.write("Lecture Info: " + lecture_info + "\n")
                    file.write("Finals: " + finals_info + "\n")
                    
                tracker += 1

            except Exception as e:
                print(f"Failed to process course: {e}") 

        # Write the course information list to a JSON file
        with open("output.json", "w") as json_file:
            json.dump(course_info_list, json_file, indent=4)
                
    # Close the driver and browser window after processing
    driver.quit()

def main():
    url = get_URL()
    driver = fetch_driver(url)
    login(driver)
    buttons, available_terms, selected_term = select_terms(driver)
    get_results(buttons, driver, available_terms, selected_term)

if __name__ == "__main__":
    main()
