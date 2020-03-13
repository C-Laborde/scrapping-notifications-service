# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
# Tutorial in https://www.dataquest.io/blog/web-scraping-tutorial-python/

import requests
from bs4 import BeautifulSoup

# +
# check netlify

# +
url1 = "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=6"
page = requests.get(url1)

# TODO change this into try / error and service logs.
if page.status_code == 200:
    print("Page status code: %s Download correct" % page.status_code)
else:
    print("Page status code: %s Error downloading" % page.status_code)

# -

soup1 = BeautifulSoup(page.content, 'html.parser')

# Ideally there're 4 div. resultados (tables)
resultados = soup1.select('div .resultados')
# TODO check if len of results is 4

useful_results = resultados[1].select('tr')
# TODO use columns names to check if right table
print(useful_results[0])
# TODO check if len(useful_results is 5, the table has 5 rows)

# +
games_results = []
table_rows = []
games = []
# The first row are the columns labels, games details start on the second row
for i in range(1, len(useful_results)):
    table_rows.append(useful_results[i])

for game in table_rows:
    game_components = game.find_all('td')
    res = game_components[1].contents
    game_struct = {"LOCAL": game_components[0].find('a', class_='discreto').contents,
                   "VISITANT": game_components[2].find('a', class_='discreto').contents,
                   "RESUL": res,
                   "SETS": game_components[3].contents}
    games_results.append(res)
    games.append(game_struct)

# TODO check that all values in dics have length 1
# -

games

url2 = "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=7"
page = requests.get(url2)
soup2 = BeautifulSoup(page.content, 'html.parser')

# Ideally there're 4 div. resultados (tables)
resultados = soup2.select('div .resultados')
# TODO check if len of results is 4

useful_results = resultados[1].select('tr')
# TODO use columns names to check if right table
print(useful_results[0])
# TODO check if len(useful_results is 5, the table has 5 rows)

# +
games_results2 = []
table_rows = []
games2 = []
# The first row are the columns labels, games details start on the second row
for i in range(1, len(useful_results)):
    table_rows.append(useful_results[i])

for game in table_rows:
    game_components = game.find_all('td')
    res = game_components[1].contents
    game_struct = {"LOCAL": game_components[0].find('a', class_='discreto').contents,
                   "VISITANT": game_components[2].find('a', class_='discreto').contents,
                   "RESUL": res,
                   "SETS": game_components[3].contents}
    games_results2.append(res)
    games2.append(game_struct)

# TODO check that all values in dics have length 1
# -

games2
