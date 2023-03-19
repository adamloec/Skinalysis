import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta

# Market analysis object.
#
# Parameters:
# url = Url to steam market place item.
# range = Number of days prior to current date to gather data on.
#
# Notes:
# Moving average should be less than 21 days for the most up to date market information.
class Market:
    def __init__(self, url, range=21):
        self.url = url
        self.range = range
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
        self.__parse_recent(all_history)
        return 0
    
    def __parse_recent(self, all_history):
        
        # Current date information
        today = datetime.now()
        month = today.strftime("%b")

        # Start date, 30 days prior to current date
        start_date = today - timedelta(self.range)
        start_month = start_date.strftime("%b")
        start_day = start_date.day

        # Parses all data within the past 21 days
        for i in range(0, len(all_history)):
            if month in all_history[i][0]:
                self.history.append(all_history[i])
            
            if start_month in all_history[i][0]:
                date_int = int(f"{all_history[i][0][4]}{all_history[i][0][5]}")
                if start_day <= date_int:
                    self.history.append(all_history[i])

