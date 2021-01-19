from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, PCA #, TruncatedSVD
from sklearn.pipeline import FeatureUnion
from scipy.spatial import distance

from itertools import permutations 
import argparse

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from conllu import parse_incr


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', type=str, nargs='+', help="Enter the conllu files", required=True)
parser.add_argument('-t', '--textfile', type=str, help="Enter the text file", required=True)
#parser.add_argument('-n', '--number', type=int, default=4, help="Number of topics")
#parser.add_argument('-c', '--clusters', type=int, default=4, help="Number of clusters")
parser.add_argument('-m', '--maxSents', type=int, default=1000, help="maximum number of sentences")
args = parser.parse_args()

numberClusters = len(args.files) + 1
allData = []
allLabels = []
sents = []
sent_id = []
for lineIdx, line in enumerate(open(args.textfile)):
    if lineIdx > args.maxSents:
        break
    allData.append(line.strip())
    allLabels.append('fy')
    sent_id.append(lineIdx)
    sents.append(line.strip())
print(args.textfile)
print(len(allData))

def conlToText(path):
    full = []
    txt = []
    sent = ''
    for line in open(path):
        if len(line) < 2:
            txt.append(sent.strip())
            sent = ''
            full = [] 
        else:
            tok = line.strip().split('\t')
            full.append(tok)
            if len(tok) == 10:
                sent += tok[1] + ' '
    return txt



for conlFile in args.files:
    name = conlFile.split('/')[-1]
    name = name[:name.rfind('.')]
    for sentIdx, sent in enumerate(conlToText(conlFile)[:args.maxSents]):
        allData.append(sent)
        allLabels.append(name)
        sents.append(sent)
        sent_id.append(sentIdx)
    print(name)
    print(sentIdx)

print()


def identity(x):
    return x

def tok(x):
    return x.split(' ')


charNgr=(1,5)
wordNgr=(1,2)
wordVectorizer = CountVectorizer(strip_accents=identity, lowercase=True,
                 preprocessor=identity, tokenizer=tok, analyzer='word',
                 ngram_range=wordNgr)
charVectorizer = CountVectorizer(strip_accents=identity, lowercase=True,
                preprocessor=identity, tokenizer=identity, analyzer='char',
                ngram_range=charNgr)
vectorizer = FeatureUnion([('word', wordVectorizer), ('char', charVectorizer)])
data_vectorized = vectorizer.fit_transform(allData)

print("FEATURES MADE")

lda_model = LatentDirichletAllocation(n_components=numberClusters,
        max_iter=10,
        learning_method='batch',
        random_state=100,
        )
lda_output = lda_model.fit_transform(data_vectorized)

print("LDAMODEL MADE")



# convert scores to idxs
winners = []
for item in lda_output:

    winners.append(list(item).index(max(item)))



# print the accuracy for all clusters/all languages 
allScores = []
for lang in sorted(set(allLabels)):
    allScores.append([])
    for cluster_idx in range(numberClusters):
        total = 0
        cor = 0
        for item, gold in zip(winners, allLabels):
            if gold == lang:
                if item == cluster_idx:
                    cor += 1
                total += 1
        print(lang, cluster_idx, cor/total)
        allScores[-1].append(cor/total)



# reshape to 2d to plot
if numberClusters != 2:
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(lda_output)
else:
    pca_result = lda_output

fig, ax = plt.subplots(figsize=(8,5), dpi=300)
for lang in sorted(set(allLabels)):
    langData = []
    for gold, pred in zip(allLabels, pca_result):
        if gold == lang:
            langData.append(pred)
    ax.scatter([x[0] for x in langData], [x[1] for x in langData], label=lang)

leg = ax.legend(loc='upper right')
leg.get_frame().set_linewidth(1.5)
fig.savefig('scatter.pdf', bbox_inches='tight')

print("FIGURE MADE")

avgs = []
for i in range(numberClusters):
    total = 0.0
    instances = 0
    for gold, pred in zip(allLabels, lda_output):
        if gold == 'fy':
            total += pred[i]
            instances += 1
    avgs.append(total/instances)




ranking = []
for goldlb, pred, sentc, sentsID in zip(allLabels, lda_output, sents, sent_id):
    euc_distance = distance.euclidean(pred, avgs)
    ranking.append([euc_distance, goldlb, sentc, sentsID])#, conll])


rows = sorted(ranking)
rowsnew = []
for item in rows:
    if item[1] == "fy":
        pass
    else:
        rowsnew.append(item)


df = pd.DataFrame(rowsnew, columns =["dist", "gold", "sentence", "sent_id"])
print(df)

df.to_csv("rankingstest.csv")

print("DONE")


