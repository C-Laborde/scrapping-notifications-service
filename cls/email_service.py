from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.cloud import firestore
import os
import smtplib
import ssl

db = firestore.Client()


class EmailService:
    def __init__(self):
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")
        self.port = os.getenv("SMTP_PORT")
        self.host = os.getenv("SMTP_HOST")
        self.setup_connection()

    def setup_connection(self):
        # Try to log in to server and send email
        # Create a secure SSL context
        context = ssl.create_default_context()
        try:
            s = smtplib.SMTP(self.host, self.port)
            s.starttls(context=context)     # Secure connection
            s.login(self.username, self.password)
            self.s = s
        except Exception:
            raise Exception

    def get_destinations(self):
        # TODO We will need to filter by teams/url
        # TODO Optimize the query with a projection
        docs = db.collection(u'users').stream()
        emails = [doc.to_dict()["email"] for doc in docs]
        self.emails = emails

    def send_email(self, weekend, ref_url, document):
        # Creation of email object
        msg = MIMEMultipart("alternative")
        # TODO retrieve the subject from some email config
        msg['Subject'] = "FCVResultats jornada " + weekend
        msg['From'] = self.username

        # Email content
        text = text_msg(weekend, document)
        html = html_msg(weekend, ref_url, document)
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message.
        # The email client will try to render the last part first
        msg.attach(part1)
        msg.attach(part2)

        self.get_destinations()
        recipients = self.emails
        # TODO this works to send email to multiple persons but the email
        # addresses are not hidden
        # msg['To'] = ",".join(recipients)
        # try:
        #     self.s.sendmail(msg['From'], recipients, msg.as_string())
        # except Exception:
        #     raise Exception
        # finally:
        #     self.s.quit()
        for email in recipients:
            msg['To'] = email
            try:
                self.s.sendmail(msg['From'], msg['To'], msg.as_string())
            # TODO should I catch this exception here too? Is catched in main to
            # add it to the logs...
            # TODO when sending multiple emails, one can fail because of an incorrect
            # email address but others should be sent
            except Exception:
                raise Exception
            finally:
                self.s.quit()


# TODO test text email and add results besides the link
def text_msg(weekend, ref_url):
    return f"\
        Hay nuevos resultados disponibles de la jornada {weekend}\
        Puedes verlos en este link: {ref_url}"


def html_msg(weekend, ref_url, document):
    # TODO add string so repeated emails content is not hide by gmail
    return f"""\
    <html>
        <body>
            <p>
            Hola, <br> Hay nuevos resultados disponibles de la <//br>
            <a href= ref_url> jornada {weekend} </a>
            </p>
            <div class="resultados">
                <h3> RESULTATS D'AQUESTA JORNADA </h3>
                <table width="800"
                       border="0"
                       align="center"
                       cellpadding="2"
                       cellspacing="2"
                       class="tabla">
                    <tbody>
                        <tr class="tittr">
                            <td width="30%" height="13" valign="top"
                                bgcolor="#A9F5E1"> LOCAL </td>
                            <td width="4%" valign="top" bgcolor="#A9F5E1">
                                RESUL </td>
                            <td width="30%" valign="top" bgcolor="#A9F5E1">
                                VISITANT </td>
                            <td width="36%" valign="top" bgcolor="#A9F5E1">
                                SETS </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81BEF7">
                                {document["GAME1"]["LOCAL"]} </td>
                            <td bgcolor="#81BEF7" align="center">
                                {document["GAME1"]["RESULT-LOCAL"]} -
                                {document["GAME1"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81BEF7">
                                {document["GAME1"]["VISITANT"]} </td>
                            <td bgcolor="#81BEF7">
                                {document["GAME1"]["SETS"]} </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81DAF5">
                                {document["GAME2"]["LOCAL"]} </td>
                            <td bgcolor="#81DAF5" align="center">
                                {document["GAME2"]["RESULT-LOCAL"]} -
                                {document["GAME2"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81DAF5">
                                {document["GAME2"]["VISITANT"]} </td>
                            <td bgcolor="#81DAF5">
                                {document["GAME2"]["SETS"]} </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81BEF7">
                                {document["GAME3"]["LOCAL"]} </td>
                            <td bgcolor="#81BEF7" align="center">
                                {document["GAME3"]["RESULT-LOCAL"]} -
                                {document["GAME3"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81BEF7">
                                {document["GAME3"]["VISITANT"]} </td>
                            <td bgcolor="#81BEF7">
                                {document["GAME3"]["SETS"]} </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81DAF5">
                                {document["GAME4"]["LOCAL"]} </td>
                            <td bgcolor="#81DAF5" align="center">
                                {document["GAME4"]["RESULT-LOCAL"]} -
                                {document["GAME4"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81DAF5">
                                {document["GAME4"]["VISITANT"]} </td>
                            <td bgcolor="#81DAF5">
                                {document["GAME4"]["SETS"]} </td>
                        </tr>
                    </tbody>
                </table>
            </div>   
        </body>
    </html>
    """

