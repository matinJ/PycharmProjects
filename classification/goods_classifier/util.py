"""
Date    : 15/4/17
Author  : baylor
"""
__author__ = 'baylor'

url_suf = set(["com", "net", "org", "edu", "gov", "int", "mil", "net", "biz", "info", "pro", "name", "museum",
               "coop", "aero", "xxx", "idv", "cc", "ws", "asia", "ac", "co",
               "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar",
               "as", "at", "au", "aw", "az", "ba", "bb", "bd", "be", "bf", "bg", "bh",
               "bi", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz",
               "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co",
               "cr", "cs", "cu", "cv", "cx", "cy", "cz", "de", "dj", "dk", "dm", "do",
               "dz", "ec", "ed", "ee", "eg", "eh", "er", "es", "et", "eu", "fi", "fj",
               "fk", "fm", "fo", "fr", "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi",
               "gl", "gm", "gn", "go", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy",
               "hk", "hm", "hn", "hr", "ht", "hu", "id", "ie", "il", "im", "in", "io",
               "iq", "ir", "is", "it", "je", "jm", "jo", "jp", "ke", "kg", "kh", "ki",
               "km", "kn", "kp", "kr", "kw", "ky", "kz", "la", "lb", "lc", "li", "lk",
               "lr", "ls", "lt", "lu", "lv", "ly", "ma", "me", "mc", "md", "mg", "mh",
               "mi", "mk", "ml", "mm", "mn", "mo", "mp", "mq", "mr", "ms", "mt", "mu",
               "mv", "mw", "mx", "my", "mz", "na", "nc", "ne", "nf", "ng", "ni", "nl",
               "no", "np", "nr", "nu", "nz", "om", "or", "pa", "pe", "pf", "pg", "ph",
               "pk", "pl", "pm", "pn", "pr", "ps", "pt", "pw", "py", "qa", "re", "ro",
               "ru", "rw", "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj", "sk",
               "sl", "sm", "sn", "so", "sr", "st", "su", "sv", "sy", "sz", "tc", "td",
               "tf", "tg", "th", "tj", "tk", "tm", "tn", "to", "tp", "tr", "tt", "tv",
               "tw", "tz", "ua", "ug", "uk", "um", "us", "uy", "uz", "va", "vc", "ve",
               "vg", "vi", "vn", "vu", "wf", "ws", "ye", "yt", "yu", "za", "zm", "zr",
               "zw"])


def get_domain_f_url(url):
    url = url.replace('http://', '')
    url = url.split('/')[0]
    arr = url.split('.')
    l = len(arr) - 1

    domain = None
    while True:
        if l < 0:
            break
        s = arr[l]
        l -= 1
        if s in url_suf:
            continue
        else:
            domain = s
            break
    return domain