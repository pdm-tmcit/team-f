import csv
import MeCab
import numpy as np
import pandas as pd
import array

pd.set_option('display.max_rows', None)
path_r = './test/testdata.csv'
path_w = './test/testdata_fixed.csv'
mecab = MeCab.Tagger("-Ochasen")
mecab.parse("")

f = pd.read_csv(path_r,header=None,usecols=['0','1','2','3','4','5','6','7'],nrows=3000,names=['0','1','2','3','4','5','6','7'],encoding='utf-8',engine="python")
f['0'] = f['0'].str.strip()
f['1'] = f['1'].str.strip()
f['2'] = f['2'].str.strip()
f['3'] = f['3'].str.strip()
f2 = f['0']+','+f['1']+','+f['2']+','+f['3'].fillna('こんにちは')+f['4'].fillna('')+f['5'].fillna('')+f['6'].fillna('')+f['7'].fillna('')
f2 = f2.str.strip()
f2 = f2.str.replace(" ","")
h = f2.to_string(index=False,header=False)
h2 = h.replace(" ","")

#print(f2.to_csv)

with open(path_w,mode='w',encoding='utf-8',newline='',errors='ignore') as r:
    f2.to_csv(r,header=False,index=False,quoting=csv.QUOTE_MINIMAL,quotechar=' ')
        #r.write(h2)
