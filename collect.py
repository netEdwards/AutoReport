from creds import USERNAME,PASSOWRD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from functions import updateCookieFromSelenium, getTokens
import time
import requests
import re
import json


chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(options=chrome_options)


driver.get("https://chick-fil-a.compliancemetrix.com/rql/p/acfareportsallreportsvtopissuesactivator")
driver.implicitly_wait(2)
#login info
username_input = driver.find_element(By.ID, "input28") #find the input for username
username_input.send_keys(USERNAME) #input the username
next_button = driver.find_element(By.CLASS_NAME, "button-primary") #find the next button
next_button.click() # click the next button
driver.implicitly_wait(1) #let it load for a second
password_input = driver.find_element(By.ID, "input53") #find the input for password
password_input.send_keys(PASSOWRD) # insert password there
verify_button = driver.find_element(By.CLASS_NAME, 'button-primary') #find the next/verify again to be sure.
driver.implicitly_wait(1)
verify_button.click() # click the next/verify.
time.sleep(10)
#-------SET LOCATION-------#
combobox = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[4]/div/div[3]/div/div/div/div[1]/form[2]/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div/div')
combobox.click()
comboSelection = driver.find_element(By.XPATH, '/html/body/span[3]/span/span/ul/li[3]')
comboSelection.click()
driver.refresh()
time.sleep(2)
#-------FIND TABLE AND ROWS-------#
wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table')))
rows = table.find_elements(By.TAG_NAME, 'tr')

#-------DATA VAR FOR STORING RESPONSE-------#
session = requests.Session()
xhr_url = "https://chick-fil-a.compliancemetrix.com/rql/execute"

#-------LOOP THROUGH TABLE AND CLICK ON VIEW-------#
for i in range(len(rows)-1):
    row = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody tr')))[i]
    view_link = row.find_element(By.CSS_SELECTOR, 'a')
    driver.execute_script("arguments[0].click();", view_link)
    time.sleep(3)
#-------GET TOKENS AND SEND XHR REQUEST-------#
    updateCookieFromSelenium(driver, session)
    headers, data = getTokens(driver)
    response = session.post(xhr_url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Failed to retrieve data via XHR replication", response.status_code, response.text)


    #PROBLEM
    #If we use the loop to click on view and retrieve the finding for the question, then it will leave the current DOM probbaly  fuckin up everything. Making the loop kinda useless.






