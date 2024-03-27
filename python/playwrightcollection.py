from playwright.sync_api import sync_playwright
from creds import USERNAME, PASSOWRD, LINK
from functions import *
import time


class CancellationException(Exception):
    pass
#================================================================================================
#This is called main because before I made it into a app with GUIs it was just going to be a script
#But then I was like, I may need to use this at work or while out of town, I want to be able to download this anywhere and run it, 
#and it not look like a I am a dorky hacker. So I made a GUI and a exe for it. 

#Any way I wont document the function as I dont care enough to do so. But the print statements kinda give it away.
#So does playwrights's api it pretty self explaniatory.
#================================================================================================
def main(event):
    try:
        browser = None
        with sync_playwright() as p:
            print('===================STARTING===================')
            print('Launching page...')
            controller(event)
            browser = p.chromium.launch(headless=True) #False allows a visible browser
            page = browser.new_page(no_viewport=True)
            #nav to eRQA
            page.goto(LINK)
            controller(event)
            print('laoding...')
            #Login here
            page.wait_for_load_state('load')
            page.fill("input#input28", USERNAME)
            page.click(".button-primary")
            page.wait_for_load_state('load')
            page.fill("input#input53", PASSOWRD)
            page.click(".button-primary")
            #Checking events
            controller(event)
            #Swap store location/filter
            page.wait_for_load_state('domcontentloaded')
            page.click('xpath=/html/body/div[1]/div[1]/div[3]/div/div[4]/div/div[3]/div/div/div/div[1]/form[2]/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div/div')
            time.sleep(0.5)
            page.click('xpath=/html/body/span[3]/span/span/ul/li[3]')
            page.wait_for_load_state('domcontentloaded')
            page.reload()
            controller(event) #Checking events
            page.wait_for_load_state('domcontentloaded')
            page.wait_for_load_state('networkidle')
            print('Logged in...')
            print('This is the initial loading. Due to the websites instability sometimes it may timeout while waiting on the next state.\n After 30 Seconds it will time out.')
            #Find and loop through the rows
            controller(event)#Checking events
            print("Looking for the data table...")
            page.wait_for_selector("css=table > tbody > tr", timeout=30000)
            rows = page.query_selector_all("css=table > tbody > tr")
            print('=========================================================================')
            print('========== Table and Rows found beginning data collection loop ==========')
            print('=========================================================================')
            print(f'{len(rows)} - Rows')
            controller(event)#Checking events
            for i in range(len(rows)):
                print(f'Starting row {i+1}')
                page.wait_for_selector("css=table > tbody > tr", timeout=15000)
                rows = page.query_selector_all("css=table > tbody > tr")
                link = rows[i].query_selector('a')
                link.click()
                print('Routing page to find the right network activity...')
                page.wait_for_load_state('domcontentloaded')
                page.wait_for_load_state('networkidle')
                page.reload()
                page.on('response', log_response)
                page.wait_for_load_state('domcontentloaded')
                page.wait_for_load_state('networkidle')
                controller(event)#Checking events
                print('Data save...')
                page.wait_for_load_state('domcontentloaded')
                page.wait_for_load_state('networkidle')
                page.remove_listener('response', log_response)
                time.sleep(1)
                page.go_back()
                print('Routing page to default state...')
                page.wait_for_load_state('domcontentloaded')
                print('Successfull...')
                page.reload()
            print('=========================================================================')
            print('==================== Data collection loop complete ======================')
            print('=========================================================================')
            parseJSON()
    #This is to check for a cancellation request I send from the GUI.
    except CancellationException as e:
        print(f"Cancel Error: {e}")
    except Exception as e: #any other errors ig
        print(f"Error: {e}")
    finally:
        print("Closing browser...")
#What I use to periodically check for a cancellation request. Which I have to do since I think it should be synchronous.
def controller(event):
    if event.is_set():
        print("Cancellation has been requested, attempting to cancel...")
        raise CancellationException("Operation cancelled by user.")