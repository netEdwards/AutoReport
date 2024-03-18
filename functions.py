from creds import USERNAME,PASSOWRD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests
import re
import json


def updateCookieFromSelenium(driver, session):
    session.cookies.clear()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])


def getTokens(driver):
    target_script_content = ""
    script_tags = driver.find_elements(By.TAG_NAME, 'script')
    for script_tag in script_tags:
        script_content = script_tag.get_attribute("innerHTML")
        if "__RequestVerificationToken" in script_content and "__RQLToken" in script_content:
            target_script_content = script_content
            break
    if not target_script_content:
        print("Failed to find the target script content")
    verification_token_match = re.search(r'"__RequestVerificationToken":\s*"([^"]+)"', target_script_content)
    rql_token_match = re.search(r'"__RQLToken":\s*"([^"]+)"', target_script_content)
    if verification_token_match and rql_token_match:
        verification_token = verification_token_match.group(1)
        rql_token = rql_token_match.group(1)
        print("Verification Token:", verification_token)
        print("RQL Token:", rql_token)
    else:
        print("Tokens not found in script content")
    headers = {
    '__requestverificationtoken': verification_token,
    '__rqltoken': rql_token,
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Length': '709',
    'Content-Type': 'application/json',
    'Origin': 'https://chick-fil-a.compliancemetrix.com',
    'Referer': 'https://chick-fil-a.compliancemetrix.com/rql/p/acfareportsallreportsvtopissuesactivator',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Fetch-Site': 'same-origin',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # Add 'User-Agent', 'Sec-Fetch-*', and other security headers as necessary
    }
    page_index = 0
    store_id = "str-0f168ef5db564e4aa3ac10dbad9d8140"
    data = {
        "AppName":"CFA_Reports_ScoreGroups","ViewName":"Top_Issues_ScoreGroups","PageIndex": page_index,"PageSize":200,"IncludeHiddenColumns":'true',"PageFilters":["CFA_Reports_eRQA_Periods.Top_Issues_Periods","Alias","Last Week","Seq",1,"Period","7","StoreId","str-0f168ef5db564e4aa3ac10dbad9d8140","CFA_Reports_Services.Top_Issues_Services","Service_Name","ALL","Seq","100","Queue_Seq","1","StoreId","ALL","CFA_Reports_ScoreGroups.Top_Issues_Combined_ScoreGroups","Score_Group_Desc","ALL","Score_Group_ID","ALL","Combined_Score_Group_ID","ALL","Seq","1","StoreId","ALL","CFA_Reports_ScoreGroups.Top_Issues_ScoreGroups","Score_Group_Desc","ALL","Score_Group_ID","ALL","Combined_Score_Group_ID","ALL","Seq","1","StoreId","ALL"]
    }
    return headers, data

