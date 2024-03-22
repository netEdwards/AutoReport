from creds import USERNAME,PASSOWRD
from playwright.sync_api import sync_playwright
import pandas as pd
import json
import time



collect_data = []
def log_response(response):
    #print(f"URL: {response.url}, Resource Type: {response.request.resource_type}")
    if response.request.url == 'https://chick-fil-a.compliancemetrix.com/rql/queue/':
        print(f"Resource Type: {response.request.resource_type}")
        print(f"Response: {response.json()}")
        collect_data.append(response.json())

def parseJSON():
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

    df = pd.DataFrame(data_dict)
    df_transposed = df.T
    df_transposed.reset_index(inplace=True)
    df_transposed.columns = ['Assesment Type', 'Assesment', 'Risk Level', 'Question', 'Finding', 'Fixed?', 'Name', 'Date']
    df_transposed.to_excel('output.xlsx', index=False)
    print('Excel file saved as output.xlsx')
        






