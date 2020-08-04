#!/usr/bin/env python3
# 基本設計
class BaseCh():
    position = 0
    position_dic = {
        '村人': 0, '占い師': 1, '霊媒師': 2, '狩人': 3,
        '人狼': 4, '狂人': 5, '共有者': 6, '妖狐': 7
    }
    corpus = []
    predict_positions = {}

    # 役職から役職の番号へ
    def ch2position(self, ch):
        return self.position_dic[ch]
    
    # ch2positionの逆変換
    def position2ch(self, position):
        keys = [ k for k,v in self.position_dic if v == position ]
        return keys[0] if keys else None

    # 出力
    def output(self, s):
        print(s)

#lass Position0(BaseCh):

if __name__ == '__main__':
    test = BaseChar()
