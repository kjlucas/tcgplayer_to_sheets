import re
import requests
from bs4 import BeautifulSoup

rarities = []

def clean_tcg_data(text):
    #Remove apostrophes completely (Champion's - Champions)
    text = text.replace("'", "")
    
    #Convert to lowercase
    text = text.lower()
    
    #Replace any remaining non-alphanumeric blocks with a single dash
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    #Clean up the edges
    return text.strip('-')

def get_ahr_for_set(set):
    cleaned_set = clean_tcg_data(set)
    