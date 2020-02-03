import pandas as pd
import re
import requests
import urllib
from bs4 import BeautifulSoup

# Get basic players information for all players
base_url = "https://sofifa.com/players?offset="
columns = ['Name', 'Nationality']
data = pd.DataFrame(columns=columns)

for offset in range(0, 300):
    url = base_url + str(offset * 61)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    table_body = soup.find('tbody')
    for row in table_body.findAll('tr'):
        td = row.findAll('td')
        nationality = td[1].find('a').get('title')
        name = td[1].findAll('a')[1].text
        player_data = pd.DataFrame([[name, nationality]])
        player_data.columns = columns
        data = data.append(player_data, ignore_index=True)
data = data.drop_duplicates()

data.to_csv('data.csv', encoding='utf-8-sig')
