#!/usr/bin/env python3

import sys
import requests

#input  (stdin)  -> NCBI Genome List 
#output (stdout) -> Genome A reference (like) format ( \n separated)

def parse_tsv_get_pmids_l(tsv):
    for line in tsv:
        line = line.rstrip().split('\t')
        pmid = line[24]
        if pmid.isdigit():
            yield pmid

def pmid2title(pmid):
    r = requests.get("http://togows.dbcls.jp/entry/pubmed/{}/title".format(pmid))
    r.raise_for_status()
    print(r.text)

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
    for pmid in set(parse_tsv_get_pmids_l(sys.stdin)):
        sys.stdout.write(pmid2ref(pmid) + '\n')

