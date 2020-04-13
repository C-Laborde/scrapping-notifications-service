import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl


def send_email(weekend, ref_url, document):
    """
    Sends email to users with document (game) content
    weekend = int, weekend nr
    ref_url = string, url to include in email for the user to go
    document = dictionary, the games information to include in email
    """
    # Email config is obtained from environment vars
    creds = get_credentials()

    # Creation of email object
    msg = MIMEMultipart("alternative")
    # TODO retrieve the subject from some email config
    msg['Subject'] = "FCVResultats jornada " + weekend
    msg['From'] = creds["smtp_username"]
    # TODO this will be queried from db
    msg['To'] = creds["smtp_to"]

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

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        s = smtplib.SMTP(creds["smtp_host"], creds["smtp_port"])
        s.starttls(context=context)     # Secure connection
        s.login(creds["smtp_username"], creds["smtp_password"])
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    # TODO should I catch this exception here too? Is catched in main to
    # add it to the logs...
    # TODO when sending multiple emails, one can fail because of an incorrect
    # email address but others should be sent
    except Exception:
        raise Exception
    finally:
        s.quit()


def get_credentials():
    return {
        "smtp_username": os.getenv("SMTP_USERNAME"),
        "smtp_password": os.getenv("SMTP_PASSWORD"),
        "smtp_port": os.getenv("SMTP_PORT"),
        "smtp_host": os.getenv("SMTP_HOST"),
        "smtp_to": os.getenv("SMTP_TO")
        }


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
