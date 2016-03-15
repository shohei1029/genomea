#!/usr/bin/env python3

import sys
import requests

#for multiprocessing
import multiprocessing as mp
from itertools import repeat

requests.adapters.DEFAULT_RETRIES = 3

def pmid2ref(pmid):
    #r.raise_for_status() #全部に付けるか保留
    sys.stderr.write('PMID:{}\n'.format(pmid))
    rest_args = ['au', 'year', 'title', 'journal', 'volume', 'pages']

    pool = mp.Pool(len(rest_args))
    callback = pool.starmap(get_from_togows, zip(repeat(pmid), rest_args))
    refr = {k: v for dic in callback for k, v in dic.items()}
    refr['au'] = refr['au'].replace('\n', ', ')

    ref_format = "{authors}. {year}. {title} {journal}. {volume}:{pages}.".format(authors=refr['au'], year=refr['year'], title=refr['title'], journal=refr['journal'], volume=refr['volume'], pages=refr['pages'])

    return ref_format


def get_from_togows(pmid, arg):  #return dict
    try:
        r = requests.get("http://togows.dbcls.jp/entry/pubmed/{}/{}".format(pmid, arg))
        r.raise_for_status()
        out = {arg: r.text.rstrip()}
    except: #requests.exceptions.HTTPError
        out = get_from_togows(pmid, arg)
    return out


if __name__ == '__main__':
    in_pmid = sys.stdin.readline().rstrip()
    sys.stdout.write(pmid2ref(in_pmid))
