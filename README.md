# ParsingFrisian
Code for the project: Challenges in Annotating and Parsing Spoken, Code-switched, Frisian-Dutch data.

## Data Selection
### Selection of Frisian data
This program was used to extract Frisian sentences that we did not use in our own development and test set. In the program the file is the conllu file that contained our selection of sentences. The trainfile is the file that the program should extract the sentences from and sentences is the file that the program should write the raw data to. It can simply be run by:

```
python3 getfy.py
```


### LDA
This program takes as input conllu files and a textfile with raw sentences and finds the sentences that are most similar to the sentences in the textfile. An additional argument can be used: --maxSents. The default is 1000 sentences. The output is both a scatterplot and a csv file with the ordered sentences starting with the most similar sentence.

```
python3 lda.py --files f1.conllu f2.conllu --textfile sentences.txt
```

### Creating a new conllu file
This program takes the output of lda.py and creates a conllu file for the numSents most similar sentences.

```
python3 get_conllu.py --filew out.csv --numSents 2000
```

## Additional Experiments
### Diacritics
### Adding Orphans

## Evaluation

## Outputs
In this directory all conllu outputs that are discussed in the paper can be found.

For the experiments we used MaChAmp from Van der Goot (2020). The specific commit that was used can be found in gitlogmtp.txt.


## References
* van der Goot, R., Üstün, A., Ramponi, A., & Plank, B. (2020). Massive Choice, Ample Tasks (MaChAmp): A Toolkit for Multi-task Learning in NLP. arXiv preprint arXiv:2005.14672.
