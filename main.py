#credits:
##https://www.learndatasci.com/tutorials/ultimate-guide-web-scraping-w-python-requests-and-beautifulsoup/
##
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()

if __name__ == '__main__':
    # Get the HTML of your public TCGPLayer collection page
    html_response = requests.get(os.getenv('collection_url'))

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_response.content, 'html.parser')
    selector = '#collectionContainer table' #copied from inspect of the page
    table = soup.select_one(selector)
    print(table)