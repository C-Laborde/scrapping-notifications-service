import requests
from bs4 import BeautifulSoup
from google.cloud import firestore
import json
import logging
import os, ssl
from utils.send_email import send_email


db = firestore.Client()

TEST = False     # False to test real behaviour, True for forcing sending email
 
def parse_res(res):
    res = res.replace(" ", "")
    try:
        res_loc = res.split("-")[0]
        res_vis = res.split("-")[1]
        played = 1
    except IndexError:
        res_loc = "-"
        res_vis = "-"
        played = 0
    return res_loc, res_vis, played

def parse_sets(sets):
    if len(sets) > 0:
        return sets
    else:
        return "-"

def doc_comparison(restored, document):
    if not sorted(restored.keys()) == sorted(document.keys()):
        print("RESTORED KEYS: ", restored.keys())
        print("DOCUMENT KEYS: ", document.keys())
        raise KeyError("Documents have different keys")
    equal = True
    for game in restored.keys():
        results_restored = [restored[game]["RESULT-LOCAL"], restored[game]["RESULT-VISITANT"]]
        results_doc = [document[game]["RESULT-LOCAL"], document[game]["RESULT-VISITANT"]]
        if results_restored != results_doc:
            return False
    return True
   

def main(request):
    logging.basicConfig(level="INFO")
    logger = logging.getLogger(__name__)

    weekend = str(6)
    url = "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=" + weekend
    page = requests.get(url)

    # TODO change this into try / error and service logs.
    if page.status_code == 200:
        print("Page status code: %s Download correct" % page.status_code)
    else:
        print("Page status code: %s Error downloading" % page.status_code)


    #### Next section is about getting the results new or not
    soup1 = BeautifulSoup(page.content, 'html.parser')

    # Ideally there're 4 div. resultados (tables)
    all_tables = soup1.select('div .resultados')
    # TODO check if len of results is 4

    table = all_tables[1].select('tr')
    # TODO use columns names to check if right table
    # TODO check if len(useful_results is 5, the table has 5 rows)

    games = []
    played_games = 0
    # The first row are the columns labels, games details start on the second row
    for i in range(1, len(table)):
        game = table[i]
        game_components = game.find_all('td')
        res = game_components[1].contents
        res_loc, res_vis, played = parse_res(res[0])
        played_games += played
        sets = parse_sets(game_components[3].contents)
        game_struct = {"LOCAL": game_components[0].find('a', class_='discreto').contents,
                    "VISITANT": game_components[2].find('a', class_='discreto').contents,
                    "RESULT-LOCAL": res_loc,
                    "RESULT-VISITANT": res_vis,
                    "SETS": sets}
        games.append(game_struct)

    # If all the results are empty we can finish here. Only dump when there
    # has been a result
    if played_games == 0:
        # TODO should I log this? It will be logged every 5 minutes before the
        # first results have been played..
        logger.info("There are no results for this weekend yet")
        return "204: No game results"
    
    # This is to format the document into a json format
    weekend_id = "WEEKEND" + weekend
    names_parse = {"CEV L‘HOSPITALET 'B'": "CEV LHOSPITALET B",
                   "CLUB VÒLEI LA PALMA": "CLUB VOLEY LA PALMA",
                   "VÒLEI ELS ARCS": "VOLEY ELS ARCS",
                   "CV TORELLÓ": "CV TORELLO",
                   "AEE ELISABETH SALOU": "AEE ELISABETH SALOU",
                   "OPTICALIA CV VILANOVA GROC": "OPTICALIA CV VILANOVA GROC",
                   "IGUALADA VÒLEI CLUB": "IGUALADA VOLEI CLUB",
                   "DSV CV SANT CUGAT 'D'": "DSV CV SANT CUGAT D"}

    document = {}
    # TODO check that all values in dics have length 1
    for i, game in enumerate(games):
        document["GAME" + str(i + 1)] = {k: names_parse.get(v[0], v[0])
                                         for k, v in game.items()}
    if TEST:
        try:
            send_email(weekend, url, document)
            logger.info("Email sent succesfully")
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    # Now we should check for the same doc in the database.
    # If it doesn't exist: dump the doc and send email
    doc_ref = db.collection(u'games').document(weekend_id)
    restored_doc = doc_ref.get()
    if not restored_doc.exists:
        logger.info("First event of this weekend has been found")
        doc_ref.set(document)
        # TODO I'm not sure if I'm handling the exceptions correctly
        try:
            send_email(weekend, url, document)
            logger.info("Email sent succesfully")
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    # It it exists: load it and compare
    else: 
        # TODO compare restored_doc with document. Be carefull with N and None
        restored_dict = restored_doc.to_dict()
        are_equal = doc_comparison(restored_dict, document)
        if are_equal:
            logger.info("No new games results were reported")
            return str(204)
        else:
            doc_ref.set(document)
            logger.info("A new game result has been reported ")
            try:
                send_email(weekend, url, document)
                logger.info("Email sent succesfully")
            except Exception as e:
                logger.error(e)
                raise Exception(e)
    return str(200)
