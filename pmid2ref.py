#!/usr/bin/env python3

import sys
import requests

def pmid2ref(pmid):
    #r.raise_for_status() #全部に付けるか保留
    r_au     = requests.get("http://togows.dbcls.jp/entry/pubmed/{}/au".format(pmid))
    r_year   = requests.get("http://togows.dbcls.jp/entry/pubmed/{}/year".format(pmid))
    r_title  = requests.get("http://togows.dbcls.jp/entry/pubmed/{}/title".format(pmid)) 
    r_journal= requests.get("http://togows.dbcls.jp/entry/pubmed/{}/journal".format(pmid)) #雑誌名をGenomeA論文のrefに合わせられない。。。。
    r_volume = requests.get("http://togows.dbcls.jp/entry/pubmed/{}/volume".format(pmid))
    r_pages  = requests.get("http://togows.dbcls.jp/entry/pubmed/{}/pages".format(pmid))

    au_2 = r_au.text.replace('\n', ', ').rstrip(', ')

    ref_format = "{authors}. {year}. {title} {journal}. {volume}:{pages}.".format(authors=au_2, year=r_year.text.rstrip(), title=r_title.text.rstrip(), journal=r_journal.text.rstrip(), volume=r_volume.text.rstrip(), pages=r_pages.text.rstrip())

    return ref_format


if __name__ == '__main__':
    in_pmid = sys.stdin.readline().rstrip()
    sys.stdout.write(pmid2ref(in_pmid))
