from google.cloud import firestore
from utils.comparison import doc_comparison
# from .send_email import send_email

db = firestore.Client()


# TODO could this functionality be further splitted?
def compare_and_send(document, weekend, logger, url, email_service):
    """
    Depending on the document contents and what has been stored in the db
    already, decides if an email should be sent to the users or not
    document = dictionary with games details
    weekend = int, weekend nr
    logger = logging object
    url = url required for email href content
    """
    # If it doesn't exist: dump the doc and send email
    weekend_id = "WEEKEND" + weekend
    doc_ref = db.collection(u'games').document(weekend_id)
    restored_doc = doc_ref.get()
    if not restored_doc.exists:
        logger.info("First event of this weekend has been found")
        doc_ref.set(document)
        # TODO I'm not sure if I'm handling the exceptions correctly
        try:
            email_service.send_email(weekend, url, document)
            logger.info("Email sent succesfully")
        except Exception as e:
            logger.error(e)
            raise Exception(e)

    # It it exists: load it and compare. # OBS I could check just the number
    # of games played and compare it with the value in the db instead of
    # comparing the full doc, but it's less robust
    else:
        restored_dict = restored_doc.to_dict()
        are_equal = doc_comparison(restored_dict, document)
        if are_equal:
            logger.info("No new games results were reported")
            return str(204)
        else:
            doc_ref.set(document)
            logger.info("A new game result has been reported ")
            try:
                email_service.send_email(weekend, url, document)
                logger.info("Email sent succesfully")
                # TODO should I return something here?
            except Exception as e:
                logger.error(e)
                raise Exception(e)
