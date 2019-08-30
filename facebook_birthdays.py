# Imports

import requests
import re
import pandas as pd
import numpy as np

# Initialising Variables

names = []
dates = []

epochs = ['1546300800', '1548979200', '1551398400', '1554076800', '1556668800', '1559347200', '1561939200', '1564617600', '1567296000', '1569888000', '1572566400', '1575158400']

# Instructions

# Copy the Address and the Headers
# Format the Headers in the standard JSON
# Remove the Value after ?date=VALUE and replace it with {}
# Do the same thing for the "path" value in the headers JSON

for epoch in epochs:
    res = requests.get(YOUR_URL_HERE.format(epoch),
                   headers = {"authority": "www.facebook.com",
                                "path": YOUR_PATH_HERE.format(epoch),
                                "scheme": "",
                                "accept": "",
                                "accept-language": "",
                                "cache-control": "",
                                "cookie": "",
                                "pragma": "",
                                "referer": "",
                                "sec-fetch-mode": "",
                                "sec-fetch-site": ""})
    data = re.findall(r'([a-z0-9 ]+)(\([0-9]*\\\/[0-9]*\))', res.content.decode('utf-8'), re.IGNORECASE)
    for element in data:
        names.append(element[0])
        dates.append(element[1])
        
# Data Cleaning and Formatting
        
birthdays = pd.DataFrame()
birthdays['NAME'] = names
birthdays['DATE'] = dates

birthdays['DATE'] = birthdays.DATE.str.replace('[\(\)\\\]', '')+'/2019'
birthdays['DATE'] = pd.to_datetime(birthdays.DATE, dayfirst = True)
birthdays = birthdays.sort_values('DATE')
birthdays = birthdays.rename(columns = {'NAME':'Subject', 'DATE':'Start Date'})
birthdays['Subject'] = birthdays.Subject.str.strip()
birthdays['End Date'] = birthdays['Start Date']
birthdays['All Day Event'] = 'TRUE'

# Create for 5 Years

temp = pd.DataFrame()
for i in range(1,6):
    birthdays_new = birthdays.copy()
    birthdays_new['Start Date'] = birthdays_new['Start Date'] + pd.DateOffset(years = i)
    birthdays_new['End Date'] = birthdays_new['End Date'] + pd.DateOffset(years = i)
    temp = temp.append(birthdays_new)
birthdays = birthdays.append(temp)

# Save to CSV
birthdays.to_csv('birthday_calendar.csv', index = False)