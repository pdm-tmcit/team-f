#!/usr/bin/env python
import MeCab
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

# textを単語区切りのリストへ
def words(text):
    output = []
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    node = tagger.parseToNode(text)

    while node:
        anode = node.feature.split(',')
        wtype = anode[0]
        word = node.surface

        if word == '*' and node.feature.split(",")[6].isalpha():
            word = anode[6]

        if len(word) > 0:
            output.append(word)

        node = node.next

    return output

# 標準入力
stdin = open('/dev/stdin', 'r')
documents = [ stdin.readline() ]
line = stdin.readline()
while line:
    documents.append(line)
    line = stdin.readline()
stdin.close()

# 学習セットの作成
train_data = []
for i, document in enumerate(documents):
    print(i, words(document))
    train_data.append(TaggedDocument(words=words(document), tags=[str(i)]))

# 学習モデルの生成
model = Doc2Vec(documents=train_data, min_count=1, alpha=0.005, epochs=40, sample=20, dm=1)

# 表示
for i, document in enumerate(documents):
    print(str(i), "\t", document)
    k = 0
    for j in model.docvecs.most_similar(str(i), topn=2):
        print("\t", str(j[0]), ':', str(j[1]), documents[int(j[0])])
        k += 1
        if k == 2:
            break
