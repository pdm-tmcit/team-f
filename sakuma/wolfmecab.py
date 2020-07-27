import csv
import MeCab
import numpy as np
import pandas as pd
import array

pd.set_option('display.max_rows', None)
path_r = './wolf_win/village_g1422.csv'
path_w = './save_mecab_g1422_nonumber.txt'
path_w2 = './save_mecab_g1422_hatugen_nonumber.txt'
path_w3 ='./save_mecab_g1422_number.txt'
path_w4 = './save_mecab_g1422_hatugen_number.txt'
mecab = MeCab.Tagger("-Ochasen")
mecab.parse("")

f = pd.read_csv(path_r,header=None,usecols=['3'],nrows=3000,names=['0','1','2','3'],encoding='utf-8',engine="python")
g = f.to_string(index=False,header=False)
h = f.to_string()
a = mecab.parse(g)
b = mecab.parse(h)
c = str(a)

#print(f)
#print(a)

with open(path_w,mode='w',encoding='utf-8',errors='ignore') as r:
    r.write(c)

with open(path_w2,mode='w',encoding='utf-8',errors='ignore') as r:
    r.write(g)

with open(path_w3,mode='w',encoding='utf-8',errors='ignore') as r:
    r.write(b)

with open(path_w4,mode='w',encoding='utf-8',errors='ignore') as r:
    r.write(h)
