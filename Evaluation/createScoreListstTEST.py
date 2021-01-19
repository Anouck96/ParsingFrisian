from conll18_ud_eval import evaluate, load_conllu
import os


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

def get_LAS(gold, syst):
	file1 = open(gold)

	goldfile = load_conllu(file1)
	file2 = open(syst)

	systemfile = load_conllu(file2)
	return(evaluate(goldfile,systemfile)["LAS"].f1)

def get_UAS(gold, syst):
	file1 = open(gold)

	goldfile = load_conllu(file1)
	file2 = open(syst)

	systemfile = load_conllu(file2)
	return(evaluate(goldfile,systemfile)["UAS"].f1)

def get_UPOS(gold, syst):
	file1 = open(gold)

	goldfile = load_conllu(file1)
	file2 = open(syst)

	systemfile = load_conllu(file2)
	return(evaluate(goldfile,systemfile)["UPOS"].f1)

def main():

	UASscores = open("UASscores.out", "w")
	LASscores = open("LASscores.out", "w")
	UPOSscores = open("UPOSscores.out", "w")
	#Create temporary files for every sentences
	LAS = []
	UAS = []
	UPOS = []
	datagold = readNorm("test/test.conllu")
	datasystem = readNorm("test/exp2.conllu")

	systemfiles = []
	goldfiles = []
	for item in range(len(datagold)):
		s = datagold[item]
		with open("{}goldtemp.conllu".format(item), "w") as f:
			goldfiles.append("{}goldtemp.conllu".format(item))
			for it in s:
				f.write(it + "\n")
			f.write("\n")
	for sent in range(len(datasystem)):
		d = datasystem[sent]
		with open("{}systemtemp.conllu".format(sent), "w") as g:
			systemfiles.append("{}systemtemp.conllu".format(sent))
			for st in d:
				g.write(st + "\n")
			g.write("\n")

	for f, b in zip(goldfiles, systemfiles):
		las = get_LAS(f, b)
		LASscores.write(str(las) + "\n")
		uas = get_UAS(f,b)
		UASscores.write(str(uas) + "\n")
		upos = get_UPOS(f,b)
		UPOSscores.write(str(upos) + "\n")

	for sf in goldfiles:
		os.remove(sf)
	for df in systemfiles:
		os.remove(df)


if __name__ == '__main__':
	main()