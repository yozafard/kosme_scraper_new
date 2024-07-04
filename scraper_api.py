from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# from datetime import datetime, timedelta
# import requests
# import json
import os
from dotenv import load_dotenv
import time
import locale
from dateutil import parser
import threading
import datetime
# import datetime
from pyairtable import Api
# from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from flask import Flask, jsonify
# from flask_restful import Resource, Api
import threading
# Main workflow
load_dotenv()
app = Flask(__name__)

app.config['FRESHA_PASS'] = os.getenv('FRESHA_PASS')
app.config['FRESHA_USERNAME'] = os.getenv('FRESHA_USERNAME')
app.config['AIRTABLE_TOKEN'] = os.getenv('AIRTABLE_TOKEN')
app.config['BASE_ID'] = os.getenv('BASE_ID')
app.config['HANDSON_TABLE_ID'] = os.getenv('HANDSON_TABLE_ID')
app.config['LOG_TABLE_ID'] = os.getenv('LOG_TABLE_ID')

locale.setlocale(locale.LC_ALL, '')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(executable_path= ChromeDriverManager().install(), options=options)

def login(username, password):
    driver.get(
        "https://partners.fresha.com/users/sign-in?redirectTo=%2Fsales%2Fappointments-list%2F")
    WebDriverWait(
driver, 10).until(
    EC.presence_of_element_located(
        (By.NAME, "email")))

    search_email = driver.find_element(By.NAME, "email")
    search_email.send_keys(username)
    search_email.send_keys(Keys.RETURN)

    WebDriverWait(
driver, 10).until(
    EC.element_to_be_clickable(
        (By.NAME, "password")))
    search_password = driver.find_element(By.NAME, "password")
    search_password.send_keys(password)
    WebDriverWait(driver, 5)
    search_password.send_keys(Keys.RETURN)

def apply_filter(start, end):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        ((By.CSS_SELECTOR, 'button[data-qa="open-filters-button"]'))))
    WebDriverWait(
driver, 5).until(
    EC.element_to_be_clickable(
        ((By.CSS_SELECTOR, 'button[data-qa="open-filters-button"]'))))
    apply_button = driver.find_element(
By.CSS_SELECTOR, 'button[data-qa="open-filters-button"]')
    apply_button.click()

    WebDriverWait(
driver,
20).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR,
            'select[data-qa="select-structure-native-select-appointmentStatus"]')))
    search_completed_status = driver.find_element(
By.CSS_SELECTOR,
    'select[data-qa="select-structure-native-select-appointmentStatus"]')
    select = Select(search_completed_status)
    select.select_by_visible_text("Completed")
    assert select.first_selected_option.text == "Completed"

    WebDriverWait(
driver, 10).until(
    EC.element_to_be_clickable(
        ((By.CSS_SELECTOR, 'button[data-qa="apply-filters"]'))))
    apply_button = driver.find_element(
By.CSS_SELECTOR, 'button[data-qa="apply-filters"]')
    apply_button.click()

    WebDriverWait(
driver, 20).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.Nb\\+2hY.wyvXUg.p8KH04.eoLbQK.p5ClCH.Xi7MFQ")))
    search_date_button = driver.find_element(
By.CSS_SELECTOR, "button.Nb\\+2hY.wyvXUg.p8KH04.eoLbQK.p5ClCH.Xi7MFQ")
    search_date_button.click()

    WebDriverWait(
driver, 5).until(
    EC.element_to_be_clickable(
        (By.NAME, "startDate")))
    search_start_date = driver.find_element(By.NAME, "startDate")
    search_start_date.click()
    search_start_date.send_keys(Keys.CONTROL + "a")
    search_start_date.send_keys(Keys.BACK_SPACE)
    search_start_date.send_keys(start)

    search_end_date = driver.find_element(By.NAME, "endDate")
    search_end_date.click()
    search_end_date.send_keys(Keys.CONTROL + "a")
    search_end_date.send_keys(Keys.BACK_SPACE)
    search_end_date.send_keys(end)

    WebDriverWait(
driver, 5).until(
    EC.element_to_be_clickable(
        ((By.XPATH, "//button[contains(@class, 'QATGoX') and text()='Apply']"))))
    apply_button = driver.find_element(
By.XPATH, "//button[contains(@class, 'QATGoX') and text()='Apply']")
    apply_button.click()

def unfold_data():
    start_time = time.time()  # Capture the start time

    results_text_element = WebDriverWait(
driver,
15).until(
    EC.visibility_of_element_located(
        (By.XPATH,
            "//span[contains(text(), 'Showing ') and contains(text(), ' results')]")) )
    parts = results_text_element.text.split()

    # Continue looping until the desired condition or timeout
    while (int(parts[1]) != int(parts[3])):
        # Check if 2 minutes have passed
        if time.time() - start_time > 120:  # 120 seconds = 2 minutes
            print("Stopping due to timeout.")
            break  # Exit the loop

        # Try to find the "Load 100 more" link and click it
        try:
            load_more = WebDriverWait(driver, 20).until( EC.element_to_be_clickable(
                (By.XPATH, "//a[span[contains(text(), 'Load ') and contains(text(), ' more')]]")) )
            load_more.click()
        except Exception as e:
            print(f"Failed to click 'Load more': {e}")
            continue  # If fail to click, skip iteration

        # Update text element and parts after loading more results
        results_text_element = WebDriverWait(
driver,
20).until(
    EC.visibility_of_element_located(
        (By.XPATH,
            "//span[contains(text(), 'Showing ') and contains(text(), ' results')]")) )
        parts = results_text_element.text.split()

def get_ref():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-referenceNumber'] a")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-referenceNumber'] a")

    # Extract the text inside span elements for each link
    reference_numbers = [
link.find_element(
    By.TAG_NAME,
        "span").text for link in links]

    # Print out all reference numbers
    return reference_numbers

def get_client():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-customerName'] a")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-customerName'] a")

    # Extract the text inside span elements for each link
    client_names = [
link.find_element(
    By.TAG_NAME,
        "span").text for link in links]

    # Print out all reference numbers
    return client_names

def get_service():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-serviceName']")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-serviceName']")

    # Extract the text inside span elements for each link
    services = [
link.find_element(
    By.CSS_SELECTOR,
        "div[data-qa='text:").text for link in links]

    # Print out all reference numbers
    return services

def get_created_by():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-createdBy']")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-createdBy']")

    # Extract the text inside span elements for each link
    created = [
link.find_element(
    By.CSS_SELECTOR,
        "div[data-qa='text:").text for link in links]

    # Print out all reference numbers
    return created

def get_created_date():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-createdOn']")) )

    # Retrieve all elements matching the selector
    elements = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-createdOn'] div[data-qa='date-time:']")

    # Prepare list for holding formatted dates
    formatted_dates = []

    # Extract and format the date from each element
    for element in elements:
        date_str = element.text  # e.g., '1 May 2024, 13:18'
        # Parse the date
        date_obj = parser.parse(date_str)

        # date_obj = datetime.strptime(date_str, "%d %B %Y, %H:%M")
        # Format the date
        formatted_date = date_obj.strftime("%m-%d-%Y")
        formatted_dates.append(formatted_date)

    return formatted_dates

def get_scheduled_date():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-scheduledOn']")) )

    # Retrieve all elements matching the selector
    elements = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-scheduledOn'] div[data-qa='date-time:']")

    # Prepare list for holding formatted dates
    formatted_dates = []

    # Extract and format the date from each element
    for element in elements:
        date_str = element.text  # e.g., '1 May 2024, 13:18'
        # Parse the date
        date_obj = parser.parse(date_str)

        # date_obj = datetime.strptime(date_str, "%d %B %Y, %H:%M")
        # Format the date
        formatted_date = date_obj.strftime("%m-%d-%Y")
        formatted_dates.append(formatted_date)

    return formatted_dates

def get_staff():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-employeeName']")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-employeeName']")

    # Extract the text inside span elements for each link
    created = [
link.find_element(
    By.CSS_SELECTOR,
        "div[data-qa='text:").text for link in links]

    # Print out all reference numbers
    return created

def get_loc():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-locationName']")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-locationName']")

    # Extract the text inside span elements for each link
    created = [
link.find_element(
    By.CSS_SELECTOR,
        "div[data-qa='text:']").text for link in links]

    # Print out all reference numbers
    return created

def get_status():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-status']")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-status']")

    # Extract the text inside span elements for each link
    created = [
link.find_element(
    By.CSS_SELECTOR,
        "span._-wKXe2._3\\-CGH2.ZCv8t2.KfKqA2.font\\-default\\-body\\-xs\\-medium").text for link in links]

    # Print out all reference numbers
    return created

def get_duration():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-duration']")) )

    # Retrieve all elements matching the selector
    elements = driver.find_elements(
By.CSS_SELECTOR,
    'td[data-qa="report-table-column-duration"]')

    # Extract the text inside div elements for each link
    durations = [
        element.find_element(By.CSS_SELECTOR, "div[data-qa='duration:']").text
        for element in elements
    ]

    # Convert each duration string to minutes
    minutes = []
    for duration in durations:
        total_minutes = 0
        parts = duration.split()
        for part in parts:
            if 'h' in part:
                # Extract number of hours and convert to minutes
                hours = int(part.replace('h', ''))
                total_minutes += hours * 60
            elif 'min' in part:
                # Extract number of minutes
                minutes_only = int(part.replace('min', ''))
                total_minutes += minutes_only

        minutes.append(total_minutes)

    return minutes

def get_price():
    WebDriverWait(driver, 10).until( EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "td[data-qa='report-table-column-price']")) )

    # Retrieve all elements matching the selector
    links = driver.find_elements(
By.CSS_SELECTOR,
    "td[data-qa='report-table-column-price']")

    # Extract the text inside span elements for each link
    created = [float((link.find_element(
        By.CSS_SELECTOR, "div[data-qa='money:']").text).split()[-1]) for link in links]

    # Print out all reference numbers
    return created

def retrieve_data(username, password, start, end):
    login(username, password)
    apply_filter(start, end)
    unfold_data()

    ref_list = get_ref()

    # Ensuring all functions return lists of the same length
    client_list = get_client()
    service_list = get_service()
    created_by_list = get_created_by()
    # created_date_list = get_created_date()
    scheduled_date_list = get_scheduled_date()
    staff_list = get_staff()
    location_list = get_loc()
    duration_list = get_duration()
    price_list = get_price()

    staffs = {
        'Amberly Bong': 'Amberly',
        'Chloe Mok': 'Chloe',
        'Christine Liew': 'Christine',
        'Elaine Lau': 'Elaine Lau',
        'Else Yee': 'Else Yee',
        'Emily Nai': 'Emily ',
        'Fiona Yu': 'Fiona',
        'Ivy Seah': 'Ivy',
        'Jae Ong': 'Jae Ong',
        'Jasmine': 'Jasmine',
        'Jeslyn': 'Jeslyn',
        'Kate Fom': 'Kate',
        'Mandy Ong': 'Mandy',
        'May Cheah': 'Huey May',
        'Mico': 'Mico',
        'Natalie Leong': 'Natalie Leong ',
        'Queennie Tang': 'Queenie Tang ',
        'Rin Cheong': 'Rin Cheong',
        'Sharon Lew': 'Sharon Lew',
        'Shireen Ling': 'Shireen',
        'Shu Jun Lim': 'Shu Jun'
    }

    def get_nickname(full_name, staffs_dict):
        return staffs_dict.get(full_name, full_name)

    staff_nickname_list = []
    for staff in staff_list:
        staff_nickname_list.append(get_nickname(staff, staffs))
    # Creating a dictionary where each 'ref' maps to its corresponding data
    output = {}
    for index, ref in enumerate(ref_list):
        if ref not in output:  # Making sure the 'ref' is unique in the dictionary
            output[ref] = {
                "Ref": ref_list[index],
                "Client": client_list[index],
                # "Consultant Name": staff_list[index],
                # "Link to Commission Count": staff_list[index],
                # "Link to Commission Count New": scheduled_date_list[index],

                # "Client Membership": client_list[index][1],
                "Service (from Fresha)": service_list[index],
                # "Created By": created_by_list[index],
                # "Created Date": created_date_list[index],
                "Scheduled Date": scheduled_date_list[index],
                "Consultant (from Fresha)": staff_nickname_list[index],
                "Location": location_list[index],
                "Duration": duration_list[index],
                "Price": price_list[index]
            }
    driver.close()
    return output

# app = FastAPI()

class AirtableRequest(BaseModel):
    username: str
    password: str
    start_date: str
    end_date: str

def run_with_timeout(func, args=(), kwargs={}, timeout_duration=600):
    """Runs a function with a timeout using threading."""
    class FuncThread(threading.Thread):
        def __init__(self):
            super().__init__()
            self.result = None

        def run(self):
            self.result = func(*args, **kwargs)

    thread = FuncThread()
    thread.start()
    thread.join(timeout_duration)
    if thread.is_alive():
        thread_result = None
        timed_out = True
    else:
        thread_result = thread.result
        timed_out = False
    return thread_result, timed_out

# @app.post("/send-to-airtable/")
def send_to_airtable(username, password, startdate, enddate):
    # def send_to_airtable(username, start_date, end_date):
    token = app.config['AIRTABLE_TOKEN']
    api = Api(token)
    base_id = app.config['BASE_ID']
    table_id = app.config['HANDSON_TABLE_ID']

    log_table_id = app.config['LOG_TABLE_ID']
    log_table = api.table(base_id, log_table_id)

    # Capture the datetime of the function call
    call_datetime = datetime.datetime.now().isoformat()

    # Create an initial log entry
    log_entry = {
        # "Username": username,
        # "Scrape Start Date": start_date,
        # "Scrape End Date": end_date,
        # "Status": "In Progress",
        # "Scrape Datetime": call_datetime,  # Log the datetime of the function call
        "Username": username,
        "Scrape Start Date": startdate,
        "Scrape End Date": enddate,
        "Status": "In Progress",
        "Scrape Datetime": call_datetime,  # Log the datetime of the function call
    }
    log_record = log_table.create(log_entry)

    def update_airtable():
        try:
            # data = retrieve_data(username, start_date, end_date)
            data = retrieve_data(username, password, startdate, enddate)
            table = api.table(base_id, table_id)
            existing_records = {
rec["fields"].get("Ref"): rec["id"] for rec in table.all()}
            error_details = []

            all_failed = True
            for ref, fields in data.items():
                try:
                    if ref in existing_records:
                        record_id = existing_records[ref]
                        table.update(record_id, fields)
                        all_failed = False
                    else:
                        table.create(fields)
                        all_failed = False
                except Exception as e:
                    error_details.append(f"Ref {ref}: {str(e)}")

            status = "Failed" if all_failed else "Partial Failure" if error_details else "Completed"
            log_table.update(log_record["id"], {
                "Error Logs": "\n".join(error_details),
                "Status": status
            })

        except Exception as e:
            return e

    result, timed_out = run_with_timeout(
update_airtable, timeout_duration=1200)  # Timeout after 5 minutes
    if timed_out:
        log_table.update(log_record["id"], {
            "Status": "Time Out",
            "Error Logs": "Scraper Timeout. Please select smaller dataset."
        })
        print("Function execution timed out")
    elif isinstance(result, Exception):
        # Manage exceptions caught during normal function execution
        log_table.update(log_record["id"], {
            "Error Logs": str(result),
            "Status": "Failed"
        })
        print(f"Critical failure: {result}")

# Example usage for testing
# Replace 'retrieve_data' with your actual data retrieval function
# start_scrape(startdate, enddate)
# return


@app.route('/scrape/<startdate>/<enddate>', methods=['GET', 'POST'])
def start_scrape(startdate, enddate):
    try:
        username = app.config['FRESHA_USERNAME']
        password = app.config['FRESHA_PASS']
        print(
            f"Starting scrape from {startdate} to {enddate} with user {username}")
        threading.Thread(
    target=send_to_airtable,
    args=(
        username,
        password,
        startdate,
         enddate)).start()
        return jsonify({"message": "Scraping started successfully"}), 200
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return jsonify({"error": error_message}), 500
           # send_to_airtable(username, password, startdate, enddate)


if __name__ == '__main__':
    app.run()
