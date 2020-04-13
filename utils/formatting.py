import json


def games_to_doc(games):
    """
    Converts a games dictionary into a document dictionary with the right
    format to be dumped into the database
    games = dictionary
    """
    with open("utils/games_config.json", "r") as f:
        names_parse = json.load(f)

    document = {}
    # TODO check doc integrity
    for i, game in enumerate(games):
        document["GAME" + str(i + 1)] = {k: names_parse.get(v[0], v[0])
                                         for k, v in game.items()}
    return document
