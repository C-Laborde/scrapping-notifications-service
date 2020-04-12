def parse_res(res):
    """
    Parses the results string (res) to check if the results have been uploaded
    (played = 1) and, if so, to get the number of sets won per team
    res =  string
    """
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
    """
    Parses the sets string
    res =  string
    """
    if len(sets) > 0:
        return sets
    else:
        return "-"
