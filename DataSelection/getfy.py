from io import open
from conllu import parse_incr


def main():
	docids= []
	file = open("yourfile.conllu", 'r', encoding="utf-8")
	for tokenlist in parse_incr(file):
			docids.append(tokenlist.metadata['sent_id'])

	trainfile = open("train.txt")
	sentences = open("sentences.txt", "w")
	num = 0
	for line in trainfile:
		line = line.split("\t")
		if line[0] in docids:
			pass
		else:
			num = num + 1
			#Remove annotations from data
			sent = line[2].replace(']', '')
			sent = sent.strip()
			sent = sent.split(" ")
			new_sent = []
			for item in sent:
				if item.startswith("["):
					pass
				else:
					new_sent.append(item)
			cleansent = " ".join(new_sent)
			sentences.write(cleansent)
			sentences.write('\n')
	print(num)
if __name__ == '__main__':
	main()