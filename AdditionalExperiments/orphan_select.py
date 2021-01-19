import argparse
from itertools import islice


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', type=str, nargs='+', help="Enter the conllu files", required=True)
parser.add_argument('-w', '--writefile', type=str, nargs='+', help="Enter the output conllu file", required=True)
args = parser.parse_args()

def take(n, iterable):
# From: https://stackoverflow.com/questions/7971618/return-first-n-keyvalue-pairs-from-dict
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def readNorm(inPath):
    data = []
    curSent = []
    for line in open(inPath):
        if len(line.strip()) < 1:
            data.append(curSent)
            curSent = []
        else:
            curSent.append(line[:-1])

    #in case file does not end with empty line
    if len(curSent) > 0:
        data.append(curSent)
    return data

#Gets all sentences that contain SCONJ and CCONJ
def get_SCONJCCONJ(data):
	sconj_cconjs = []
	for conllusent in data:
		for line in conllusent:
			if "\tSCONJ\t" in line or "\tCCONJ\t" in line:
				sconj_cconjs.append(conllusent)
	return(sconj_cconjs)

# Creates a list of lists for all sentences
def create_listinlist(conjlist):
	newlist = []
	for item in sconj_cconjs:
		new = []
		for sents in item:
			new.append(sents.split("\t"))
		newlist.append(new)
	return(newlist)

#Creates an orphan and cuts the sentences after that. Also checks if it is not the first word.
def createorphanandcut(listinlist, cuttedlist):
	for completesentence in listinlist:
		counter = 0
		for lins in completesentence:
			if str(lins[0]).startswith("#"):
				counter = counter + 1

		for rule in completesentence:
			if len(rule) >1:
				if rule[3] == "CCONJ" or rule[3] == "SCONJ":
					if rule[0] != "1":
						rule[7] = "orphan"
						cutnum = int(rule[0]) + counter
						cuttedlist.append(completesentence[:cutnum])
					else:
						pass
	return(cuttedlist)


#Removes sentences that have no root
def removeNoRoots(cuttedlist):
	noRoots = []
	for cutsent in cuttedlist:
		for row in cutsent:
			if len(row) > 1:
				if row[7] == "root":
					noRoots.append(cutsent)
				else:
					pass
	return(noRoots)

# Checks which number in list contains the root
def findNumbers(noRootslist):
	roots_ids = []
	for noRootline in noRootslist:
		for rows in noRootline:
			if len(rows) > 1:
				if rows[6] == "0":
					rowWithRoot = rows
		roots_ids.append(int(rowWithRoot[0]))
	return(roots_ids)

def percentage(p, w):
	return (float(w) / 100) * float(p)



for writefile in args.writefile:
	filetowrite = writefile

for f in args.files:
	totalfinals = []
	cuttedlist = []
	data = readNorm(f)
	nusents = len(data)
	sconj_cconjs = get_SCONJCCONJ(data)
	listinlist = create_listinlist(sconj_cconjs)
	cuttedlist = createorphanandcut(listinlist, cuttedlist)
	noRoots = removeNoRoots(cuttedlist)
	listOfIdsRoots = findNumbers(noRoots)

	numberpercen = percentage(9, nusents)
	nump = int(round(numberpercen))


	f2 = open(filetowrite, "w")
	for l, i in zip(noRoots, listOfIdsRoots):
		finallist = []
		maxNr = int(l[-1][0])
		for s in l:
			if len(s) > 1:
				if int(s[6]) > maxNr:
					s[6] = str(i)
					finallist.append(s)
				else:
					finallist.append(s)
			else:
				finallist.append(s)
		totalfinals.append(finallist)


	newdict = {}
	for rules in totalfinals:
		sc = rules[0][0]
		newdict[sc] = rules


	n_items = take(nump, newdict.items())

	print(len(n_items))

	for n_it in n_items:
		for st in n_it[1]:
			if len(n_it[1]) > 1:
				newline = '\t'.join(st) + "\n"
				f2.write(newline)
			else:
				newline = n_it[1][0]
				f2.write(newline)
		f2.write('\n')















