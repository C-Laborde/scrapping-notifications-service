import json


def games_to_doc(games):
    with open("utils/games_config.json", "r") as f:
        names_parse = json.load(f)
    print("NAMES ", names_parse)
    document = {}
    # TODO check that all values in dics have length 1
    for i, game in enumerate(games):
        document["GAME" + str(i + 1)] = {k: names_parse.get(v[0], v[0])
                                         for k, v in game.items()}
    return document