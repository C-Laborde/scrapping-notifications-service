import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl


def send_email(weekend_id, document, logger):
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_to = os.getenv("SMTP_TO")

    weekend_nr = weekend_id.split("WEEKEND")[1]
    # TODO add text email
    text = '\
        Hay nuevos resultados disponibles de la jornada ' + weekend_nr
    html = html_msg(weekend_nr, document)

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "FCVResultats jornada " + weekend_id
    msg['From']    = smtp_username
    msg['To']      = smtp_to

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        s = smtplib.SMTP(smtp_host, smtp_port)
        s.starttls(context=context)     # Secure connection
        s.login(smtp_username, smtp_password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        # TODO avoid sending logger as argument. Check after if email was sent?
        logger.info("Email sent")
    except Exception as e:
        # TODO 
        logger.error(e)
    finally:
        s.quit()


def html_msg(weekend_nr, document):
    #TODO url needs to be sent as arg
    return f"""\
    <html>
        <body>
            <p>
            Hola, <br> Hay nuevos resultados disponibles de la <//br>
            <a href= "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=6"> jornada {weekend_nr} </a>
            </p>
            <div class="resultados">
                <h3> RESULTATS D'AQUESTA JORNADA </h3>
                <table width="800" border="0" align="center" cellpadding="2" cellspacing="2" class="tabla">
                    <tbody>
                        <tr class="tittr">
                            <td width="30%" height="13" valign="top" bgcolor="#A9F5E1"> LOCAL </td>
                            <td width="4%" valign="top" bgcolor="#A9F5E1"> RESUL </td>
                            <td width="30%" valign="top" bgcolor="#A9F5E1"> VISITANT </td>
                            <td width="36%" valign="top" bgcolor="#A9F5E1"> SETS </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81BEF7"> {document["GAME1"]["LOCAL"]} </td>
                            <td bgcolor="#81BEF7" align="center"> {document["GAME1"]["RESULT-LOCAL"]} - {document["GAME1"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81BEF7"> {document["GAME1"]["VISITANT"]} </td>
                            <td bgcolor="#81BEF7"> {document["GAME1"]["SETS"]} </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81DAF5"> {document["GAME2"]["LOCAL"]} </td>
                            <td bgcolor="#81DAF5" align="center"> {document["GAME2"]["RESULT-LOCAL"]} - {document["GAME2"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81DAF5"> {document["GAME2"]["VISITANT"]} </td>
                            <td bgcolor="#81DAF5"> {document["GAME2"]["SETS"]} </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81BEF7"> {document["GAME3"]["LOCAL"]} </td>
                            <td bgcolor="#81BEF7" align="center"> {document["GAME3"]["RESULT-LOCAL"]} - {document["GAME3"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81BEF7"> {document["GAME3"]["VISITANT"]} </td>
                            <td bgcolor="#81BEF7"> {document["GAME3"]["SETS"]} </td>
                        </tr>
                        <tr>
                            <td bgcolor="#81DAF5"> {document["GAME4"]["LOCAL"]} </td>
                            <td bgcolor="#81DAF5" align="center"> {document["GAME4"]["RESULT-LOCAL"]} - {document["GAME4"]["RESULT-VISITANT"]} </td>
                            <td bgcolor="#81DAF5"> {document["GAME4"]["VISITANT"]} </td>
                            <td bgcolor="#81DAF5"> {document["GAME4"]["SETS"]} </td>
                        </tr>
                    </tbody>
                </table>
            </div>   
        </body>
    </html>
    """