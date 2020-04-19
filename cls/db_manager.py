from google.cloud import firestore
from utils.comparison import doc_comparison


class DBManager:
    def __init__(self):
        self.db = firestore.Client()

    def get_urls(self):
        docs = self.db.collection(u'teams').where(u'followers',
                                                  u'>', 0).stream()
        # self.teams = {doc.to_dict() for doc in docs}
        # urls = set([[doc.to_dict()["root_url"], doc.to_dict()["root_url_id"]]
        #             for doc in docs])
        urls = []
        for doc in docs:
            doc = doc.to_dict()
            info = [doc["root_url"], doc["root_url_id"]]
            if info not in urls:
                urls.append(info)
        self.urls = urls
        return urls

    def get_teams(self, url):
        print("URL", url)
        docs = self.db.collection(u'teams').where(u'root_url',
                                                  u'==', url).stream()
        teams = [doc.to_dict()["team"] for doc in docs]
        return teams

    def compare_and_send(self, document, url_id, weekend, logger, url,
                         email_service, teams):
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
        # doc_ref = self.db.collection(u'games').document(weekend_id)
        # TODO the url collection needs to be created already
        doc_ref = self.db.collection(u'games').document(url_id).collection(u'games').document(weekend_id)
        restored_doc = doc_ref.get()
        if not restored_doc.exists:
            logger.info("First event of this weekend has been found")
            doc_ref.set(document)
            # TODO I'm not sure if I'm handling the exceptions correctly
            try:
                email_service.send_email(weekend, url, document, teams)
                logger.info("Email sent succesfully")
            except Exception as e:
                logger.error(e)
                raise Exception(e)

        # It it exists: load it and compare. # OBS I could check just the
        # number of games played and compare it with the value in the db
        # instead of comparing the full doc, but it's less robust
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
                    email_service.send_email(weekend, url, document, teams)
                    logger.info("Email sent succesfully")
                    # TODO should I return something here?
                except Exception as e:
                    logger.error(e)
                    raise Exception(e)
