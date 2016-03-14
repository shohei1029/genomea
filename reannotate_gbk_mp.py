#!/usr/bin/env python3

import sys
import re
import multiprocessing as mp

import requests

#biopython
from Bio import SeqIO

#2016.3.14 , created by Shohei Nagata
#Prokka出力のgbkを読み込ませ，CDSのUniProtKB IDを取得し，それでg-linksにかけて(post?)，結果を取得してrs_xf的な形式で出力する
# uniprotkb idを使う理由のは，g-linksに配列入れてもsoftware errorが出てしまうため

#環境
#anaconda, biopython

num_proc = 4

def reannotate_genbank(gbk): #main()かなー
    for gb_record in SeqIO.parse(gbk, 'genbank'):
        yield gb_record
        #unused func.
        
def reannotate_gbk_record(gb_record):
    sys.stderr.write(gb_record.id)
    for gb_feature in gb_record.features:
        if 'inference' in gb_feature.qualifiers:
            infe_l = gb_feature.qualifiers['inference'] 
            kbid = parse_uniprotkbid(infe_l)

            glinks_tsv_text = get_glinks_output(kbid).text

            feat_list = []
            for f_kv_s in generate_featkeyval_glinks_tsv(glinks_tsv_text):
                feat_list.append(f_kv_s)
            gb_feature.qualifiers.update({"db_xref":feat_list})
    return gb_record

p = re.compile("similar to AA sequence:UniProtKB:([A-Z0-9]+)")
def parse_uniprotkbid(infe_l):
    for v in infe_l:
        if p.match(v):
            return p.match(v).group(1)

def get_glinks_output(kbid):
    try:
        glinks_tsv = requests.get('http://link.g-language.org/{gene_id}/tsv'.format(gene_id=kbid))
    except:
        sys.stderr.write("error while requesting.. retry")
#        time.sleep(0.001)
        glinks_tsv = get_glinks_output(kbid)
    return glinks_tsv

def generate_featkeyval_glinks_tsv(glinks_tsv): #returns -> str
    for line in glinks_tsv.split('\n'):
        if line.startswith('# '):  #also removes header :D
            line = line.replace('# ', '')
            kvd = line.split('\t')
            key = kvd[0]
            val = kvd[1]
            val = val.replace(':', '_') #for GO
            yield '{k}:{v}'.format(k=key, v=val)


if __name__ == '__main__':
    gbk_records = SeqIO.parse(sys.stdin, 'genbank')
    pool = mp.Pool(num_proc)
    for out_gb_record in pool.imap(reannotate_gbk_record, gbk_records):
        SeqIO.write(out_gb_record, sys.stdout, 'genbank')




