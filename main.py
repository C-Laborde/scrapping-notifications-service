# import logging
from cls.db_manager import DBManager
from cls.email_service import EmailService
from cls.logger import Logger
from cls.scrapper import Results
# from utils.db_interactions import compare_and_send
from utils.formatting import games_to_doc
# from utils.scrapping import get_results
# from utils.send_email import send_email


TEST = True     # False to test real behaviour, True for forcing sending email


def main(request):
    log = Logger()
    logger = log.logger
    email_service = EmailService()
    db = DBManager()

    # TODO get url and weekend from db
    root_urls = db.get_urls()
    weekend = str(6)
    for i in range(len(root_urls)):
        root_urls[i].append(root_urls[i][0] + weekend)

    for url_details in root_urls:
        url_id = url_details[1]
        url = url_details[2]
        results = Results(url, logger)

        # Parse games results from website
        logger.info("Parsing website")
        results.get_results()
        games_played, games = results.games_played, results.games
        logger.info("Results correctly parsed")

        logger.info("Results are analized now:")
        # If all the results are empty we can finish here. Only dump when there
        # has been a first result
        if games_played == 0:
            # TODO should I log this? It will be logged every 5 minutes before the
            # first results have been played..
            logger.info("There are no results for this weekend yet")
            return "204: No game results"

        # This is to format the document into a json format
        document = games_to_doc(games)

        # TODO remove this from deployment, useful only for local testing
        if TEST:
            try:
                logger.info("TESTING sending email")
                email_service.send_email(weekend, url, document)
                logger.info("Email sent succesfully")
            except Exception as e:
                logger.error(e)
                raise Exception(e)

        logger.info("There are results available. We compare them with previous" +
                    " results")
        # Now we should check for the same doc in the database and decide if
        # an email should be sent accordingly
        db.compare_and_send(document, url_id, weekend, logger, url, email_service)
        logger.info("Finished")
    return str(200)
