# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.0
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

result = soup1.select('div .resultados')
# TODO use columns names to check if right table
games = []
for i in range(1, len(result[1].select('tr'))):
    games.append(result[1].select('tr')[i])

list(games[0].find_all('td'))

games[0].find_all('td')[1].contents

url2 = "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=7"
page = requests.get(url2)
soup2 = BeautifulSoup(page.content, 'html.parser')


result2 = soup2.select('div .resultados')
games2 = []
for i in range(1, len(result2[1].select('tr'))):
    games2.append(result2[1].select('tr')[i])

list(games2[0].find_all('td'))

list(games2[0].find_all('td'))[1].contentsy


