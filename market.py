import requests
from bs4 import BeautifulSoup
import re
import json

from datetime import datetime

class Market:
    def __init__(self, url):
        self.url = url
        self.history = []

    def scan(self):
        try:
            # Generate CSGO market web page, parse HTML
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find Javascript with line1 var, contains market history
            script = soup.find('script', text=re.compile('var line1='))
        
        # Error parsing given URL
        except:
            return 1
        
        # Extract array data
        match = re.search(r'var line1=(\[.*?\]);', script.string, re.S)
        if match:
            array_string = match.group(1)
        else:
            print("ERROR: Market information not found.")
            return 1
        
        all_history = json.loads(array_string)
        self.parse_recent(all_history)
        return 0
    
    def parse_recent(self, all_history):
        
        # All price history in current month
        today = datetime.now()
        month = today.strftime("%b")
        for i in range(0, len(all_history)):
            if month in all_history[i][0]:
                print(f"{month}: {all_history[i][0]}")