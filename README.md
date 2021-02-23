# ParsingFrisian
Code for the project: Challenges in Annotating and Parsing Spoken, Code-switched, Frisian-Dutch data. </br>
The code is run on data from the Fame! project by Yilmaz et al. (2016). The sentences in the output are thus from this corpus.

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
translit.py removes diacritics from the sentences. It also counts the occurences.

```
python3 translit.py --files input.conllu --writefile output.conllu
```

### Adding Orphans
The first program orphan_select.py selects sentences and creates new sentences with orphan relations. It writes them to a new file. The output should be used in replace.py. This program replaces a number of the sentences in the original file with the newly created sentences.

```
python3 orphan_select.py --files input.conllu --writefile outputorph.conllu
python3 replace.py --files input.conllu --replacefile outputorph.conllu --writefile outputreplace.conllu
```

## Evaluation
evalAccuracy.py calculates LAS, UAS, POS scores, accuracy over all labels and creates a confusion matrix. It writes the confusion matrix for the dependency relations to a csv file.

```
python3 evalAccuracy.py file1.conllu file2.conllu
```

createScoreListsDEV.py creates files for UAS, LAS, POS scores per sentence over five runs (5 random seeds) which can be used to run a bootstrap significance test.

```
python3 createScoreListsDEV.py gold.conllu run1.conllu run2.conllu run3.conllu run4.conllu run5.conllu
```

Test does the same but only for the goldfile and one run. In the program you should change datagold to your goldfile and datasystem to your systems output file.

```
python3 createScoreLists.py
```

## Outputs
In this directory all conllu outputs that are discussed in the paper can be found.

For the experiments we used MaChAmp from Van der Goot (2020). The specific commit that was used can be found in gitlogmtp.txt.


## References
* van der Goot, R., Üstün, A., Ramponi, A., & Plank, B. (2020). Massive Choice, Ample Tasks (MaChAmp): A Toolkit for Multi-task Learning in NLP. arXiv preprint arXiv:2005.14672.
* Yilmaz, E., Andringa, M., Kingma, S., Dijkstra, J., van der Kuip, F., van de Velde, H., Kampstra, F., Algra, J., van den Heuvel, H., van Leeuwen, D. (2016). A longitudinal bilingual Frisian-Dutch radio broadcast database desgined for code-wwitching research. Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC'16).
