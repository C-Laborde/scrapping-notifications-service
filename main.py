import requests
from bs4 import BeautifulSoup


def main(request):
    WEEKEND = str(6)
    url1 = "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=" + WEEKEND
    page = requests.get(url1)

    # TODO change this into try / error and service logs.
    if page.status_code == 200:
        print("Page status code: %s Download correct" % page.status_code)
    else:
        print("Page status code: %s Error downloading" % page.status_code)


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
    
    weekend_id = "WEEKEND" + WEEKEND
    names_parse = {"CEV L‘HOSPITALET 'B'": "CEV LHOSPITALET B",
                   "CLUB VÒLEI LA PALMA": "CLUB VOLEY LA PALMA",
                   "VÒLEI ELS ARCS": "VOLEY ELS ARCS",
                   "CV TORELLÓ": "CV TORELLO",
                   "AEE ELISABETH SALOU": "AEE ELISABETH SALOU",
                   "OPTICALIA CV VILANOVA GROC": "OPTICALIA CV VILANOVA GROC",
                   "IGUALADA VÒLEI CLUB": "IGUALADA VOLEI CLUB",
                   "DSV CV SANT CUGAT 'D'": "DSV CV SANT CUGAT D"}

    document = {weekend_id: {}}
    for i, game in enumerate(games):
        document[weekend_id]["GAME" + str(i + 1)] = {k: names_parse.get(v[0], v[0]) for k, v in game.items()}
   
    print("DOCUMENT: ", document)
    # TODO check that all values in dics have length 1
    return document
