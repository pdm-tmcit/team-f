#!/usr/bin/env python3
import random

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
    position0 = Position0()
    while True:
        s = input('> ')
        if s == 'quit':
            break
        position0.say()
