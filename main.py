#credits:
##https://www.learndatasci.com/tutorials/ultimate-guide-web-scraping-w-python-requests-and-beautifulsoup/
##https://www.youtube.com/watch?v=bEEzKvkj0nI
##https://discuss.python.org/t/webscraping-and-copying-data-into-google-sheets/62021
##https://docs.gspread.org/en/v3.7.0/api.html
import json

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()

import gspread

if __name__ == '__main__':
    # Get the HTML of your public TCGPLayer collection page
    html_response = requests.get(os.getenv('collection_url'))

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_response.content, 'html.parser')
    selector = '#collectionContainer table' #get selector from inspecting the page
    table = soup.select_one(selector)

    #Transforms into a list of lists, where each inner list represents a row of data from the table
    data = []

    #Get the header row and add it to the data list
    header_row = [th.text.strip() for th in table.find('tr').find_all('th')]
    data.append(header_row)

    for row in table.find_all('tr'):
        if row.find('th'): #skip header row
            continue
        cells = row.find_all('td')
        cols = []
        
        for i, col in enumerate(cells):
            if i == 3:
                #Format as a Markdown link formula: =HYPERLINK(URL, Text)
                link_tag = col.find('a')
                link_data = f"=HYPERLINK(\"{link_tag.get('href')}\", \"{link_tag.text.strip()}\")"
                cols.append(link_data)
            else:
                cols.append(col.text.strip())
        data.append(cols)

    #Setup Google Sheets API client using gspread and the service account key
    client = gspread.service_account(filename=os.getenv('path_to_service_account_key'))
    sheet = client.open_by_key(os.getenv('google_sheet_id')).get_worksheet(0)

    #Clear the existing data in the Google Sheet
    sheet.clear()

    #Insert the data into the Google Sheet
    ##'USER_ENTERED' allows Google Sheets to interpret the formula used on line 42
    ###and properly interpret the Markdown link as a hyperlink in the sheet
    response = sheet.insert_rows(data, 1, value_input_option='USER_ENTERED') 
    print("Data inserted successfully:", json.dumps(response, indent=2))