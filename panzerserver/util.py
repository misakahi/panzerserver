def within(x, l, r):
    """map a value within (l, r)

    :param x:
    :param l: min
    :param r: max
    :return:
    """
    minimum, maximum = min(l, r), max(l, r)
    res = x
    res = min(res, maximum)
    res = max(res, minimum)
    return res
