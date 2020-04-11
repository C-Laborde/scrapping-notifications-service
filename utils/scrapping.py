from bs4 import BeautifulSoup
import requests

from .parsing import parse_res, parse_sets


def get_results(url):
    """
    Scraps the target url to get the games results that have been uploaded.
    Returns the number of games for which there're results available and the
    corresponding results
    url = string, url to parse
    """
    page = requests.get(url)

    # TODO change this into try / error and service logs.
    if page.status_code == 200:
        print("Page status code: %s Download correct" % page.status_code)
    else:
        print("Page status code: %s Error downloading" % page.status_code)

    # ### Next section is about getting the results new or not
    soup = BeautifulSoup(page.content, 'html.parser')

    # Ideally there're 4 div. resultados (tables)
    all_tables = soup.select('div .resultados')
    # TODO check if len of results is 4

    table = all_tables[1].select('tr')
    # TODO use columns names to check if right table
    # TODO check if len(useful_results is 5, the table has 5 rows)

    games = []
    games_played = 0
    # The first row are the columns labels, games details start on the 2nd row
    for i in range(1, len(table)):
        game = table[i]
        game_components = game.find_all('td')
        res = game_components[1].contents
        res_loc, res_vis, played = parse_res(res[0])
        games_played += played
        sets = parse_sets(game_components[3].contents)
        game_struct = {
            "LOCAL": game_components[0].find('a',
                                             class_='discreto').contents,
            "VISITANT": game_components[2].find('a',
                                                class_='discreto').contents,
            "RESULT-LOCAL": res_loc,
            "RESULT-VISITANT": res_vis,
            "SETS": sets}
        games.append(game_struct)

    return games_played, games
