from conll18_ud_eval import evaluate, load_conllu
import sys
import os

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

def create_lists(datagold, datasystem):
	LAS = []
	UAS = []
	UPOS = []

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
		LAS.append(las)
		uas = get_UAS(f,b)
		UAS.append(uas)
		upos = get_UPOS(f,b)
		UPOS.append(upos)

	for sf in goldfiles:
		os.remove(sf)
	for df in systemfiles:
		os.remove(df)
	return LAS, UAS, UPOS

def main():
	if len(sys.argv) < 7:
		print("Please provide a goldfile and five system output conllu files")
		exit(1)


	finalLAS = []
	finalUAS = []
	finalUPOS = []
	# 1
	datagold = readNorm(sys.argv[1])
	datasystem = readNorm(sys.argv[2])
	print(sys.argv[1], sys.argv[2])
	LAS1, UAS1, UPOS1 = create_lists(datagold, datasystem)

	#2
	datasystem2 = readNorm(sys.argv[3])
	print(sys.argv[1], sys.argv[3])
	LAS2, UAS2, UPOS2 = create_lists(datagold, datasystem2)

	#3
	datasystem3 = readNorm(sys.argv[4])
	print(sys.argv[1], sys.argv[4])
	LAS3, UAS3, UPOS3 = create_lists(datagold, datasystem3)

	#4
	datasystem4 = readNorm(sys.argv[5])
	print(sys.argv[1], sys.argv[5])
	LAS4, UAS4, UPOS4 = create_lists(datagold, datasystem4)

	#5
	datasystem5 = readNorm(sys.argv[6])
	print(sys.argv[1], sys.argv[6])
	LAS5, UAS5, UPOS5 = create_lists(datagold, datasystem5)


	for h, i, j, k, l in zip(LAS1, LAS2, LAS3, LAS4, LAS5):
		newscore = h + i + j + k + l
		finalLASscore = newscore/5
		finalLAS.append(finalLASscore)


	for a, b, c, d, e in zip(UAS1, UAS2, UAS3, UAS4, UAS5):
		newscoreUAS = a + b + c + d + e
		finalUASscore = newscoreUAS/5
		finalUAS.append(finalUASscore)


	for o, p, q, r ,s in zip(UPOS1, UPOS2, UPOS3, UPOS4, UPOS5):
		newscoreUPOS = o + p + q + r + s
		finalUPOSscore = newscoreUPOS/5
		finalUPOS.append(finalUPOSscore)

	print(len(finalLAS))
	print(len(finalUAS))
	print(len(finalUPOS))

	UASscores = open("UASscores.out", "w")
	LASscores = open("LASscores.out", "w")
	UPOSscores = open("UPOSscores.out", "w")

	for score in finalLAS:
		LASscores.write(str(score) + "\n")

	for uscore in finalUAS:
		UASscores.write(str(uscore) + "\n")

	for pscore in finalUPOS:
		UPOSscores.write(str(pscore) + "\n")
if __name__ == '__main__':
	main()








