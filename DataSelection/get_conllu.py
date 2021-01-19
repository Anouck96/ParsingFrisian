import argparse
import pandas as pd
from conllu import parse_incr, parse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, nargs='+', help="Enter the csv file", required=True)
parser.add_argument('-n', '--numSents', type=int, default=1000, help="Enter the number of sentences")
args = parser.parse_args()

data = pd.read_csv(args.file[0])
data = data.head(args.numSents)
print(data)

newtrainfile = open("newtrainfiletest.conllu", "w")

cfiles = data.gold.unique()
print(data['gold'].value_counts())

count = 0

toks = []
dictoftoks = {}
for file in cfiles:
    print(file)
    conlFile = open("ud/" + file + ".conllu", "r", encoding="utf-8")
    sents = list(parse_incr(conlFile))
    dictoftoks[file] = sents
print("Created dictionary of tokenlists per file")
    
for row in data.itertuples():
    id_sent = row[5]
    gold = row[3]
    conll = dictoftoks[gold][id_sent].serialize()
    newtrainfile.write(conll)
    count = count + 1
    print(count)
print("TOTAL:", count, "FINISHED")

