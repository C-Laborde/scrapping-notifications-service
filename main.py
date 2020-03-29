import requests
from bs4 import BeautifulSoup
from google.cloud import firestore
import json
import os, ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


db = firestore.Client()

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
    try:
        return sets
    except IndexError:
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


def send_email(weekend_id, document):
    print("HERE!")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_to = os.getenv("SMTP_TO")

    weekend_nr = weekend_id.split("WEEKEND")[1]
    text = '\
        Hay nuevos resultados disponibles de la jornada ' + weekend_nr
    html = f"""\
    <html>
        <body>
            <p>
            Hola, <br> Hay nuevos resultados disponibles de la <//br>
            <a href= "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=6"> jornada {weekend_nr} </a>
            </p>
            <p>
            {document}
            </p>
        </body>
    </html>
    """
    msg = MIMEText(text)
    # msg = MIMEMultipart("alternative")
    msg['Subject'] = "FCVResultats jornada " + weekend_id
    msg['From']    = smtp_username
    msg['To']      = smtp_to

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # msg.attach(part1)
    # msg.attach(part2)

    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:
        s = smtplib.SMTP(smtp_host, smtp_port)
        s.starttls(context=context)     # Secure connection
        s.login(smtp_username, smtp_password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    except Exception as e:
        print(e)
    finally:
        s.quit()
    

def main(request):
    WEEKEND = str(6)
    url1 = "http://competicio.fcvoleibol.cat/competiciones.asp?torneo=4253&jornada=" + WEEKEND
    page = requests.get(url1)

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
        return "204: No game results"
    
    # This is to format the document into a json format
    weekend_id = "WEEKEND" + WEEKEND
    names_parse = {"CEV L‘HOSPITALET 'B'": "CEV LHOSPITALET B",
                   "CLUB VÒLEI LA PALMA": "CLUB VOLEY LA PALMA",
                   "VÒLEI ELS ARCS": "VOLEY ELS ARCS",
                   "CV TORELLÓ": "CV TORELLO",
                   "AEE ELISABETH SALOU": "AEE ELISABETH SALOU",
                   "OPTICALIA CV VILANOVA GROC": "OPTICALIA CV VILANOVA GROC",
                   "IGUALADA VÒLEI CLUB": "IGUALADA VOLEI CLUB",
                   "DSV CV SANT CUGAT 'D'": "DSV CV SANT CUGAT D"}

    document = {}
    for i, game in enumerate(games):
        document["GAME" + str(i + 1)] = {k: names_parse.get(v[0], v[0])
                                         for k, v in game.items()}
    # TODO check that all values in dics have length 1

    # Now we should check for the same doc in the database.
    # If it doesn't exist: dump the doc
    doc_ref = db.collection(u'games').document(weekend_id)
    restored_doc = doc_ref.get()
    if not restored_doc.exists:
        doc_ref.set(document)
        send_email(weekend_id, document)

    # It it exists: load it and compare
    else: 
        # TODO compare restored_doc with document. Be carefull with N and None
        restored_dict = restored_doc.to_dict()
        are_equal = doc_comparison(restored_dict, document)
        if are_equal:
            return str(204)
        else:
            doc_ref.set(document)
            print("send email")
            send_email(weekend_id, document)
    return str(200)
