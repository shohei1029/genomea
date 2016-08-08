#!/usr/bin/env python3

import sys
import re
import multiprocessing as mp
import logging

import requests

#biopython
from Bio import SeqIO

###Prerequisites###
# requests, biopython
# e.g.
#  $ pip install requests biopython

###使い方###
#まずprokkaで出されたgenbankファイルをスクリプトへ標準入力で読み込ませてください。
#そうするとreannotateされたgenbankが標準出力で吐き出されるようになっています。
# e.g. 
# cat prokka_hoge.gbk | python reannotate_gbk_mp.py > glinks_prokka_hoge.gbk

#2016.3.14 , created by Shohei Nagata
#Prokka出力のgbkを読み込ませ，CDSのUniProtKB IDを取得し，それでg-linksにかけて(post?)，結果を取得してrs_xf的な形式で出力する
# uniprotkb idを使う理由のは，g-linksに配列入れてもsoftware errorが出てしまうため

#環境
#anaconda, biopython

#呪文
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

num_proc = mp.cpu_count()
if num_proc > 16:
    num_proc = 16

def reannotate_gbk_record(gb_record):
    logger.info(gb_record.id)
    for gb_feature in gb_record.features:
        if 'inference' in gb_feature.qualifiers:
            infe_l = gb_feature.qualifiers['inference']
            kbid = parse_uniprotkbid(infe_l)
            if not kbid:
                continue
            logger.info("{} {}".format(gb_record.id, kbid))

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
        logger.warn("error while requesting.. retry")
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
    for out_gb_record in pool.imap(reannotate_gbk_record, gbk_records): #LOCUSの順番を保持したければ，imapじゃなくてmapを使い，結果を全てが終了するまで全部ためる。
        SeqIO.write(out_gb_record, sys.stdout, 'genbank')
        logger.info("done: {}".format(out_gb_record.id))




