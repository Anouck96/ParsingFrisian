from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix
import numpy
import sys
import pandas as pd


if len(sys.argv) < 3:
	print('please provide 2 conllu files')
	exit(1)


uas = 0
las = 0
total = 0
pos = 0
posTotal = 0
posConfusions = {}
relConfusions = {}
poslist1 = []
poslist2 = []
rellist1 = []
rellist2 = []
for line1, line2 in zip(open(sys.argv[1]), open(sys.argv[2])):
	if len(line1.split('\t')) == 10:
		tok1 = line1.split('\t')
		tok2 = line2.split('\t')
		rel1 = tok1[7].split(':')[0]
		rel2 = tok2[7].split(':')[0]
		pos1 = tok1[3]
		head1 = tok1[6]
		head2 = tok2[6]
		pos2 = tok2[3]
		rellist1.append(rel1)
		rellist2.append(rel2)
		if pos1 != '_' and pos2  != '_':
			poslist1.append(pos1)
			poslist2.append(pos2)
			if pos1 == pos2:
				pos += 1
			else:
				error = pos1 + '-' + pos2
				if error not in posConfusions:
					posConfusions[error] = 0
				posConfusions[error] += 1
			posTotal += 1
		if rel1 == '_' or rel2 == '_':
			continue
		if head1 == head2:
			uas +=1
			if rel1 == rel2:
				las += 1
			else:
				error = rel1 + '-' + rel2
				if error not in relConfusions:
					relConfusions[error] = 0
				relConfusions[error] += 1

		total += 1

for error in sorted(posConfusions.items(), key=lambda i: i[1], reverse=True)[:10]:
	print(error)
print()

for error in sorted(relConfusions.items(), key=lambda i: i[1], reverse=True)[:10]:
	print(error)
print()

print('UAS:', uas/total)
print('LAS:', las/total)
print('POS:', pos/posTotal)

print("Classification report and confusion matrix for POS")

for n, i in enumerate(rellist1):
	if i == "disclocated":
		rellist1[n] = "dislocated"
	if i == "nsbuj":
		rellist1[n] = "nsubj"
	if i == "de":
		rellist1[n] = "det"
for a, b in enumerate(rellist2):
	if b == "disclocated":
		rellist2[a] = "dislocated"
	if b == "nsbuj":
		rellist2[a] = "nsubj"
	if i == "de":
		rellist2[a] == "det"


print(classification_report(poslist1, poslist2))
print(confusion_matrix(poslist1, poslist2))

rlist = list(dict.fromkeys(rellist1))
rlist2 = list(dict.fromkeys(rellist2))


sortlist = sorted(rlist)
sortlist2 = sorted(rlist2)

for it in sortlist2:
	if it not in sortlist:
		sortlist.append(it)
finallabels = sorted(sortlist)


print("Classification report and confusion matrix for Dependency labels")

print(classification_report(rellist1, rellist2))
print(confusion_matrix(rellist1, rellist2))
cm = confusion_matrix(rellist1, rellist2)
pd.DataFrame(cm).to_csv("out.csv", header=finallabels, index=finallabels)
