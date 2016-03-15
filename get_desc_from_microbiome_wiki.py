#!/usr/bin/env python3

import sys
import re

#anaconda
import requests
from bs4 import BeautifulSoup

#標準入力-> 種名 or 属名等
#標準出力-> 結果，microbewiki の Description_and_significance の一段落目のみを出力する

#memo
#

def get_description_and_significance(target_name):
    url = 'https://microbewiki.kenyon.edu/index.php/{}'.format(target_name)
    r = requests.get(url, verify=False)
    r.raise_for_status()
    soup = BeautifulSoup(r.text,'lxml')
    ds_h = soup.find(id="Description_and_significance")
    if not ds_h:
        ds_h = soup.find(id="Description_and_Significance") #あまり表記ゆれがあるようだったら，正規表現にする。
    ds = ds_h.next_element.next_element.next_element #一段落目のみ
    
    return ds.text

def remove_ref_parenthesis(txt):
    return re.sub(r'\(\d{,2}\)', '', txt) #3桁以上の引用はないと信じている
    

if __name__ == '__main__':
    target_name = sys.stdin
#    target_name =  'Legionella_pneumophila'
    out = get_description_and_significance(target_name)
    out2 = remove_ref_parenthesis(out)
    sys.stdout.write(out2)


