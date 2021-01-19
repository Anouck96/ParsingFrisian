import unicodedata
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', type=str, nargs='+', help="Enter the conllu files", required=True)
parser.add_argument('-w', '--writefile', type=str, nargs='+', help="Enter the output conllu file", required=True)
args = parser.parse_args()

def strip_accents(word):
	'''https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string'''
	return "".join(c for c in unicodedata.normalize("NFD", word)
		if unicodedata.category(c) != "Mn")

def count_diacritics(sent):
	count = 0
	diacritics = ["â", "é", "ê", "ô", "û", "ú", "è", "á", "ë", "ï", "ö", "ü", "ç", "à", "î", "ñ", "ä"]
	for word in sent:
		for letter in word:
			if letter in diacritics:
				count = count + 1
	return(count)

for writefile in args.writefile:
	filetowrite = writefile

for conlFile in args.files:
	f = open(conlFile, "r")
	f2  = open(filetowrite, "w")
	list_of_counts = []
	for line in f:
		if line[:7] == "# text ":
			newline = line[9:].split(" ")
			list_of_counts.append(count_diacritics(newline))
		if line[0].isdigit():
			sent = line.split("\t")
			word = sent[1]
			newword = strip_accents(word)
			sent[1] = newword
			newsent = "\t".join(sent)
			f2.write(newsent)
		else:
			f2.write(line)

print(len(list_of_counts))


num_of_sents = 0
num_of_diac = 0
for item in list_of_counts:
	if item != 0:
		num_of_sents = num_of_sents + 1
		num_of_diac = num_of_diac + item

print("Number of sents with at least one diacritic:",num_of_sents)
print("Total number of diacritics:", num_of_diac)