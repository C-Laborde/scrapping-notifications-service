from bs4 import BeautifulSoup
import requests
from utils.parsing import parse_res, parse_sets


class Scrapper:
    def __init__(self, url, logger):
        self.url = url
        self.logger = logger
        self.get_page()

    def get_page(self):
        try:
            page = requests.get(self.url)
            self.logger.info(f"Page status code: {page.status_code} " +
                             "Download correct")
            self.page = page
            self.site = BeautifulSoup(page.content, "html.parser")
        except ConnectionError:
            self.logger.error(f"Page status code: {page.status_code} ")


class Results(Scrapper):
    def __init__(self, url, logger):
        super().__init__(url, logger)

    def get_table(self):
        # In theory there're 4 tables as div. resultados
        all_tables = self.site.select('div .resultados')
        if len(all_tables) != 4:
            self.logger.warning("Results table length is not 4. There might" +
                                " have been a problem during parsing")
            # TODO send an email to me if that's the case

        # The second table is the one with useful results
        table = all_tables[1].select('tr')

        # We check if we parsed the right table
        table_ok = validate_table(table)
        if not table_ok:
            self.logger.warning("It seems we might have parsed the wrong " +
                                "table")
            # TODO send an email to me if that's the case
        self.results_table = table

    def get_results(self):
        self.get_table()
        games = []
        games_played = 0
        # The first row are the columns labels, games details start on the 2nd
        # row.
        # We iterate over the rows (games) to parse the results per game
        for i in range(1, len(self.results_table)):
            # Game components are local, results, visitant and sets
            game_parts = self.results_table[i].find_all('td')
            # Game result
            res = game_parts[1].contents
            res_loc, res_vis, played = parse_res(res[0])
            games_played += played
            # Game sets
            sets = parse_sets(game_parts[3].contents)
            game_struct = {
                "LOCAL": game_parts[0].find('a',
                                            class_='discreto').contents,
                "VISITANT": game_parts[2].find('a',
                                               class_='discreto').contents,
                "RESULT-LOCAL": res_loc,
                "RESULT-VISITANT": res_vis,
                "SETS": sets}
            games.append(game_struct)
        self.games_played = games_played
        self.games = games
        return


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
