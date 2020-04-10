from google.cloud import firestore
import logging
from utils.comparison import doc_comparison
from utils.formatting import games_to_doc
from utils.scrapping import get_results
from utils.send_email import send_email


db = firestore.Client()

TEST = True     # False to test real behaviour, True for forcing sending email


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

    # OBS I could check just the number of games played and compare it with
    # the value in the db instead of comparing the full doc, but it's less
    # robust
    # This is to format the document into a json format
    document = games_to_doc(games)
    weekend_id = "WEEKEND" + weekend

    if TEST:
        try:
            print("DOC", document)
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
