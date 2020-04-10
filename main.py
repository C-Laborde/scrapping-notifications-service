import logging
from utils.db_interactions import compare_and_send
from utils.formatting import games_to_doc
from utils.scrapping import get_results
from utils.send_email import send_email


TEST = False     # False to test real behaviour, True for forcing sending email


def main(request):
    logging.basicConfig(level="INFO")
    logger = logging.getLogger(__name__)

    # TODO add loggers
    # TODO get url and weekend from db
    weekend = str(6)
    url = "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=" + weekend

    games_played, games = get_results(url)

    # If all the results are empty we can finish here. Only dump when there
    # has been a result
    if games_played == 0:
        # TODO should I log this? It will be logged every 5 minutes before the
        # first results have been played..
        logger.info("There are no results for this weekend yet")
        return "204: No game results"

    # This is to format the document into a json format
    document = games_to_doc(games)

    if TEST:
        try:
            print("DOC", document)
            send_email(weekend, url, document)
            logger.info("Email sent succesfully")
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    # Now we should check for the same doc in the database.
    compare_and_send(document, weekend, logger, url)
    return str(200)
