from playwright.sync_api import sync_playwright
import pandas as pd
from creds import RLINK
import random
#This is function that will look at the request url and save its repsonse.
collect_data = []
def log_response(response):
    #print(f"URL: {response.url}, Resource Type: {response.request.resource_type}")
    if response.request.url == RLINK:
        print(f"Resource Type: {response.request.resource_type}")
        print(f"Resrouce found saving data...")
        #Adds all JSON's to a list called collect data
        collect_data.append(response.json())

#This makes it so that the user can set and get the excel file saving path
excel_path = ''
def set_excel_path(path):
    global excel_path
    excel_path = path
    return excel_path
def get_excel_path():
    return excel_path

#This will take the JSON list and parse the parts I care about into a dictionary, then save it to an excel file with pandas.
def parseJSON():
    print(excel_path)
    print(f'Processing data, saving to {excel_path}/data(x).xlsx...')
    data_dict = {
        "Assesment Type" : [],
        "Assesment" : [],
        "Risk Level" : [],
        "Question" : [],
        "Finding" : [],
        "Fixed?" : [],
        "Name" : [],
        "Date" : []
    }
#This will loop through the JSON list and parse the data into the dictionary
    for json_data in collect_data:
        items = json_data["DataPage"]["Items"]
        for item in items:
            data_dict["Assesment Type"].append(item[2])
            data_dict["Assesment"].append(item[8])
            data_dict["Risk Level"].append(item[5])
            data_dict["Question"].append(item[10])
            data_dict["Finding"].append(item[11])
            data_dict["Fixed?"].append(item[12])
            data_dict["Name"].append(item[13])
            data_dict["Date"].append(item[14])
#This creates the Excel File
    counter = 0 # Made this to prevent duplicate files not very effective but works good for my scale.
    counter = random.randint(1, 10000)
    df = pd.DataFrame(data_dict)
    df.to_excel(f"{excel_path}/data{counter}.xlsx", index=False)
    print(f"Data reported in {excel_path}/data(x).xlsx")


    
        






