from creds import USERNAME,PASSOWRD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import *
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

driver = webdriver.Chrome()

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

combobox = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[4]/div/div[3]/div/div/div/div[1]/form[2]/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div/div')
combobox.click()
comboSelection = driver.find_element(By.XPATH, '/html/body/span[3]/span/span/ul/li[3]')
comboSelection.click()
driver.refresh()
time.sleep(10)

table = driver.find_element(By.CSS_SELECTOR, 'table')
rows  = driver.find_elements(By.CSS_SELECTOR, 'tr')

riskValues = []
for row in rows:
    # hiRisk = row.find_element(By.CSS_SELECTOR, 'td[data-header="# HIGH RISK"]')
    hiRisk = row.find_element(By.XPATH, '//*[@id="r171051715143367436"]/div[1]/div/div/table/tbody/tr[1]/td[4]')
    hiRiskValue = hiRisk.find_element(By.TAG_NAME, 'span')
    if hiRiskValue.text:
        riskValues.append(hiRiskValue.text)
        print(hiRiskValue.text)
    

    #PROBLEM
    #If we use the loop to click on view and retrieve the finding for the question, then it will leave the current DOM probbaly  fuckin up everything. Making the loop kinda useless.






