#!/usr/bin/env python3
import pickle
import re
import csv
import random
import string
import mojimoji
import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

# mecabのneologd辞書のファイルパス
MECAB_NEOLOGD = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd'

def preprocessing_text(text):
    # 半角・全角の統一
    text = mojimoji.han_to_zen(text)
    # 改行、半角スペース、全角スペースを削除
    text = re.sub('\r', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('　', '', text)
    text = re.sub(' ', '', text)
    # 数字文字の一律「0」化
    text = re.sub(r'[0-9 ０-９]+', '0', text)  # 数字

    # カンマ、ピリオド以外の記号をスペースに置換
    for p in string.punctuation:
        if (p == ".") or (p == ","):
            continue
        else:
            text = text.replace(p, " ")

    return text

# 分かち書き
def tokenizer_mecab(text):
    m_t = MeCab.Tagger('-Owakati')
    try:
        f = open(MECAB_NEOLOGD, 'r')
        f.close()
    except IsADirectoryError:
         m_t = MeCab.Tagger('-Owakati -d '+MECAB_NEOLOGD)
    except FileNotFoundError:
        pass

    text = m_t.parse(text)  # これでスペースで単語が区切られる
    ret = text.strip().split()  # スペース部分で区切ったリストに変換
    return ret

# 前処理と分かち書きをまとめた関数を定義
def tokenizer_with_preprocessing(text):
    text = preprocessing_text(text)  # 前処理の正規化
    ret = tokenizer_mecab(text)  # Mecabの単語分割
    return ret

# 基本設計
class BaseCh():
    position = 0
    position_dic = {
        '村人': 0, '占い師': 1, '霊媒師': 2, '狩人': 3,
        '人狼': 4, '狂人': 5, '共有者': 6, '妖狐': 7
    }
    status = 0
    corpus = {
        'Zzz…。':[0], 'ひかり':[0], '腹筋！':[0], 'やっほー':[0],
        'こんばんはー。':[0], 'は？':[0], 'やあ':[0], 'どきどき':[0],
        'ﾑｼｬﾑｼｬﾑｼｬﾑｼｬ((´)艸(｀ ))｡ﾟ｡':[0], 'ずさー。':[0], 'おはようございます。':[0],
        'よろしくお願いします。':[0], 'こんばんわー':[0], '呼んだ？':[0], 'ズサー':[0],
        'よろしく':[0], 'ずさー':[0], '人狼なんているわけないじゃん。みんな大げさだなあ':[0],
        'ふぁーあ……ねむいな……寝てていい？':[0]
    }
    predict_positions = {}

    def __init__(self):
        pass

    # 役職から役職の番号へ
    def ch2position(self, ch):
        return self.position_dic[ch]
    
    # ch2positionの逆変換
    def position2ch(self, position):
        keys = [ k for k,v in self.position_dic.items() if v == position ]
        return keys[0] if keys else None

    # 状態からコーパス検索
    def status2seq(self):
        seq = [ s for s,v in self.corpus.items() if v[0] == self.status ]
        if seq:
            index = random.randint(0,len(seq)-1)
            return seq[index]
        return None

    # 出力
    def output(self, s):
        print(s)

class Position0(BaseCh):
    def say(self):
        seq = self.status2seq()
        self.output(seq)

if __name__ == '__main__':
    '''
    documents = [[],[]]
    with open('corpus.csv', 'r') as f:
        for row in csv.reader(f, delimiter='\t'):
            documents[0].append(tokenizer_with_preprocessing(row[0]))
            documents[1].append(row[1])

    vec = [ {} for i in range(len(documents)) ]
    for i in set(documents[0]):
        for j in range(len(documents)):
            vec[j][i] = tokenized[j].count(i)

    print(vec)

    ue = st1 = st2 = 0
    for i in tokens:
        ue += vec[0][i] * vec[1][i]
        st1 += vec[0][i] ** 2
        st2 += vec[1][i] ** 2

    print(ue / (math.sqrt(st1) * math.sqrt(st2)))
    '''

    position0 = Position0()
    while True:
        try:
            s = input()
            if s == 'quit':
                break
        except EOFError:
            break
    position0.say()
