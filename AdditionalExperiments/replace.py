import argparse
from conllu import parse


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', type=str, nargs='+', help="Enter the conllu files", required=True)
parser.add_argument('-r', '--replacefile', type=str, nargs='+', help="Enter the replacements files", required=True)
parser.add_argument('-w', '--writefile', type=str, nargs='+', help="Enter the output conllu file", required=True)
args = parser.parse_args()

# Replacefile is .conllu output of orphan_select.py

for writefile in args.writefile:
	writef = open(writefile, "w")

for conlFile in args.files:
	f = open(conlFile, "r")
	dataorg = f.read()
	orgdata = dataorg.split("\n\n")


for conlrepl in args.replacefile:
	f2 = open(conlrepl, "r")
	data = f2.read()
	data = data.split("\n\n")

sources = []
for sent in data:
	try:
		source = sent.split("\n")[0].strip()
		if source != '':
			sources.append(source)
	except IndexError:
		pass



newdict = {}
for item in orgdata:
	newsen = item.split("\n\n")
	source = newsen[0].split("\n")[0].strip()
	newdict[source] = item


for ids in sources:
 	newdict.pop(ids)

for key in newdict:
	writef.write(newdict[key] + "\n")
	writef.write("\n")


for sent in data:
	writef.write(sent + "\n")
	writef.write("\n")

