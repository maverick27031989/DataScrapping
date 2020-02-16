import pandas as pd
import re
import requests
import urllib
from bs4 import BeautifulSoup

# Get basic players information for all players
base_url = "https://sofifa.com/players?offset="
columns = ['PlayerID', 'Name', 'Nationality', 'age', 'Photo', 'Flag', 'Overall', 'Potential', 'Club', 'Club Logo',
           'Value', 'Wage', 'ReleaseClause']
data = pd.DataFrame(columns=columns)

for offset in range(0, 300):
    url = base_url + str(offset * 61)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    table_body = soup.find('tbody')
    for row in table_body.findAll('tr'):

        td = row.findAll('td')

        pid = td[6].text.strip()
        name = td[1].findAll('a')[1].text
        nationality = td[1].find('a').get('title')
        age = td[2].text.strip()
        picture = td[0].find('img').get('data-src')
        flag_img = td[1].find('img').get('data-src')
        overall = td[3].text.strip()
        potential = td[4].text.strip()
        club = td[5].find('a').text
        club_logo = td[5].find('img').get('data-src')
        value = td[7].text.strip()
        wage = td[8].text.strip()
        release_clause = td[9].text.strip()

        player_data = pd.DataFrame([[pid, name, nationality, age, picture, flag_img, overall, potential, club,
                                     club_logo, value, wage, release_clause]])

        player_data.columns = columns
        data = data.append(player_data, ignore_index=True)
data = data.drop_duplicates()
data.to_csv('data.csv', encoding='utf-8-sig')
