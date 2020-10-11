from bs4 import BeautifulSoup
import requests

from .parsing import parse_res, parse_sets


def get_results(url, logger):
    """
    Scraps the target url to get the games results that have been uploaded.
    Returns the number of games for which there're results available and the
    corresponding results
    url = string, url to parse
    """
    page = requests.get(url)

    # TODO change this into try / error and service logs.
    if page.status_code == 200:
        logger.info(f"Page status code: {page.status_code} Download correct")
    else:
        logger.error(f"Page status code: {page.status_code} ")

    # ### Next section is about getting the results new or not
    site = BeautifulSoup(page.content, 'html.parser')

    # In theory there're 4 tables as div. resultados
    all_tables = site.select('div .resultados')
    if len(all_tables) != 4:
        logger.warning("Results table length is not 4. There might have " +
                       "been a problem during parsing")
        logger.info(f"URL: {url}")
        # TODO send an email to me if that's the case

    # The second table is the one with useful results
    table = all_tables[1].select('tr')

    # We check if we parsed the right table
    table_ok = validate_table(table)
    if not table_ok:
        logger.warning("It seems we might have parsed the wrong table")
        # TODO send an email to me if that's the case

    games = []
    games_played = 0
    # The first row are the columns labels, games details start on the 2nd row
    # We iterate over the rows (games) to parse the results per game
    for i in range(1, len(table)):
        # Game components are local, results, visitant and sets
        game_components = table[i].find_all('td')
        # Game result
        res = game_components[1].contents
        res_loc, res_vis, played = parse_res(res[0])
        games_played += played
        # Game sets
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


def validate_table(table):
    """
    Checks if the right results table is being parsed by checking the table
    length and the column names. Returns a boolean.
    table = list
    """
    first_row = table[0].find_all("td")
    columns_names = [col.contents[0].strip() for col in first_row]
    target_names = ["LOCAL", "RESUL.", "VISITANT", "SETS"]
    return (target_names == columns_names) and (len(table) == 5)
