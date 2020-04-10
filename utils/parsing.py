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
    if len(sets) > 0:
        return sets
    else:
        return "-"
