import json
from turtle import color

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()

import gspread
from gspread_formatting import *

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

    #Setting col widths for better readability
    col_widths = [
        ('A', 50), ('B', 50), ('C', 50), ('D', 250), 
        ('E', 100), ('F', 255), ('G', 100), ('H', 100), 
        ('I', 100), ('K', 255), ('L', 100)
    ]
    set_column_widths(sheet, col_widths)

    #Adding a table for counts of each unique value in the 'Set' column (column F)
    #That are also have a 1 in the want column (column B)
    query = "=QUERY(A:I, \"select F, count(F) where B = 1 group by F order by count(F) desc label F 'Set', count(F) 'Want Count'\", 1)"
    cell_list = sheet.range('K1')
    cell_list[0].value = query

    rsp2 = sheet.update_cells(cell_list, value_input_option='USER_ENTERED')


#FORMATTING

    #Freeze the header row
    set_frozen(sheet, 1)

    hdr_fmt = cellFormat(
        backgroundColor=color(0.75, 0.75, 0.75),
        textFormat=textFormat(bold=True),
        horizontalAlignment='CENTER'
    )

    hwt_fmt = cellFormat(
        backgroundColor=color(0.89, 0.89, 0.89),
        textFormat=textFormat(bold=True),
        horizontalAlignment='CENTER'
    )

    set_fmt = cellFormat(
        backgroundColor=color(0.89, 0.89, 0.89),
        textFormat=textFormat(bold=True),
        horizontalAlignment='LEFT'
    )

    cnt_fmt = cellFormat(
        backgroundColor=color(0.89, 0.89, 0.89),
        textFormat=textFormat(bold=False),
        horizontalAlignment='CENTER'
    )

    gen_fmt = cellFormat(
        backgroundColor=color(1, 1, 1),
        textFormat=textFormat(bold=False),
        horizontalAlignment='LEFT'
    )
    
    format_cell_ranges(
        sheet, 
        [
            ('A1:L1', hdr_fmt), 
            ('A2:C', hwt_fmt), 
            ('D2:J', gen_fmt),
            ('K2:K', set_fmt), 
            ('L2:L', cnt_fmt),
            ('M1:AA', gen_fmt)
        ]  
    )


    print("Data inserted successfully:", json.dumps(response, indent=2))
    print("Query inserted successfully:", json.dumps(rsp2, indent=2))