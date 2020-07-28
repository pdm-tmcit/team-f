#!/usr/bin/env python
import os, csv, pickle, glob
import MeCab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# textを単語区切りのリストへ
def words(text):
    output = []
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    node = tagger.parseToNode(text)

    while node:
        anode = node.feature.split(',')
        wtype = anode[0]
#       word = node.surface
        word = '*'

        if word == '*' and node.feature.split(",")[6].isalpha():
            word = anode[6]

        if wtype in ['名詞', '動詞'] and len(word) > 0:
            output.append(word)

        node = node.next

    return output

# csvから入力
print('[+] Loading datasets...', end='', flush=True)
files = glob.glob('./village_talklist/*/*.csv')
documents = []
positions = []
for filename in files:
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 4 or row[0] in [ 'プロローグ', '8日目' ]:
                continue
            while len(row) > 4:
                row[3] += ','+row[4]
                row = [ d for i,d in enumerate(row) if i != 4 ]

            positions.append(row[2])
            documents.append(row[3])
print('\t\t[\033[32mDone\033[0m]')

# 学習セットの作成
print('[+] Creating datasets...', end='', flush=True)
if not os.path.isfile('datasets_pickle.tmp'):
    train_data = []
    for i, document in enumerate(documents):
        train_data.append(TaggedDocument(words=words(document), tags=[str(i)]))
    print('\t[\033[32mDone\033[0m]')

    with open('datasets_pickle.tmp', 'wb') as f:
        pickle.dump(train_data, f)
else:
    with open('datasets_pickle.tmp', 'rb') as f:
        train_data = pickle.load(f)
    print('\t[\033[32mSkip\033[0m]')

# 学習モデルの生成
print('[+] Training model...', end='', flush=True)
if not os.path.isfile('model_pickle.tmp'):
    model = Doc2Vec(documents=train_data, min_count=1, alpha=0.005, epochs=40, sample=20, dm=1)

    with open('model_pickle.tmp', 'wb') as f:
        pickle.dump(model, f)

    print('\t\t[\033[32mDone\033[0m]')
else:
    with open('model_pickle.tmp', 'rb') as f:
        model = pickle.load(f)
    print('\t\t[\033[32mSkip\033[0m]')

# クラスタリング
data = [ model[i] for i in range(len(documents)) ]
print('[+] Clusteging...', end='', flush=True)
if not os.path.isfile('kmeans_pickle.tmp'):
    kmeans = KMeans(n_clusters=7).fit(data)

    with open('kmeans_pickle.tmp', 'wb') as f:
        pickle.dump(kmeans, f)
    print('\t\t[\033[32mDone\033[0m]')
else:
    with open('kmeans_pickle.tmp', 'rb') as f:
        kmeans = pickle.load(f)
    print('\t\t[\033[32mSkip\033[0m]')

# 表示
pca = PCA(n_components=2)
pca.fit(data)
pca_data = pca.fit_transform(data)

color = ['red', 'blue', 'green', 'black', 'orange', 'purple', '#202020']
fp = FontProperties(fname='/Users/asid/Library/Fonts/ipagp.ttf', size=14)

plt.figure()
for i in range(100):
    if positions[i] == '人狼':
        label = '■'
    elif positions[i] == '狂人':
        label = '▲'
    else:
        label = ''
    plt.plot(pca_data[i,0], pca_data[i,1], 'o', c=color[int(kmeans.labels_[i])])
    plt.annotate(label, xy=(pca_data[i,0], pca_data[i,1]), fontproperties=fp)

plt.savefig('wolf.png')
