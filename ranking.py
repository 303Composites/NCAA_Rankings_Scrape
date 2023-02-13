# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:48:08 2023

@author: 303composites
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

teams = ['Hofstra', 'Brown', 'Syracuse', 'Harvard', 'Seton Hall', 'Siena', 'Arizona St.']

# Making a GET request
url = 'https://www.ncaa.com/rankings/basketball-men/d1/ncaa-mens-basketball-net-rankings'
r = requests.get(url)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

#name of the rankings table 
s = soup.find('table', class_='sticky')

# Obtain every title of columns with tag <th>
headers = []
for i in s.find_all('th'):
    title = i.text
    headers.append(title)

#Create Dataframe
ranking = pd.DataFrame(columns = headers)

for j in s.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(ranking)
    ranking.loc[length] = row 

#Cleaning up the table
ranking.drop(['Quad 1', 'Quad 2', 'Quad 3', 'Quad 4', 'Home','Road', 'Neutral'], inplace=True, axis=1)

#creating a table for the teams we care about
df = ranking.loc[ranking['School'].isin(teams)].reset_index(drop=True)

print(df)

#Print to a CSV if you want
#df.to_csv('Weekly_team_rankings.csv', index=False)