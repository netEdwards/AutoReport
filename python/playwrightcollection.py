from playwright.sync_api import sync_playwright
from creds import USERNAME, PASSOWRD
from functions import *
import time
import random

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #False allows a visible browser
        page = browser.new_page()

        #nav to eRQA
        page.goto("https://chick-fil-a.compliancemetrix.com/rql/p/acfareportsallreportsvtopissuesactivator")

        rand = random.randint(2, 4)

        #Login here
        page.wait_for_load_state('load')
        page.fill("input#input28", USERNAME)
        page.click(".button-primary")
        page.wait_for_load_state('load')
        page.fill("input#input53", PASSOWRD)
        page.click(".button-primary")
        time.sleep(rand)

        #Swap store location/filter
        page.click('xpath=/html/body/div[1]/div[1]/div[3]/div/div[4]/div/div[3]/div/div/div/div[1]/form[2]/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div/div')
        time.sleep(0.5)
        page.click('xpath=/html/body/span[3]/span/span/ul/li[3]')
        page.wait_for_load_state('domcontentloaded')
        page.reload()
        time.sleep(rand)

        #Find and loop through the rows
        page.wait_for_selector("css=table > tbody > tr", timeout=30000)
        rows = page.query_selector_all("css=table > tbody > tr")
        print(len(rows))
        for i in range(len(rows)):
            page.wait_for_selector("css=table > tbody > tr", timeout=10000)
            rows = page.query_selector_all("css=table > tbody > tr")
            link = rows[i].query_selector('a')
            link.click()
            print('link clicked')
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_load_state('networkidle')
            page.reload()
            page.on('response', log_response)
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_load_state('networkidle')
            print('im here waiting 3 seconds..')
            time.sleep(3)
            page.remove_listener('response', log_response)
            time.sleep(1)
            page.go_back()
            print('going back')
            page.wait_for_load_state('domcontentloaded')
            print('Went back succesfully')
            page.reload()
            print('reloaded waiting for a...')
        page.close()    
        parseJSON()
        print('===================done===================')

                

            
            


if __name__ == '__main__':
    main()