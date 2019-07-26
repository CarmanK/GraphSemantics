# Automated Phrase and Sentence Mining to Develop Graph Stories


## Research Documentation

Please cite the following paper if you are using my tool, thanks!

* Kevin Carman, "[Automated Phrase and Sentence Mining to Develop Graph Stories](http://reu.dimacs.rutgers.edu/~kc1125/content/Kevin_Carman_Research_Paper.pdf)," Rutgers University, 2019.

## Related GitHub Repository

*  [AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase)

## Requirements
* g++ `$ sudo apt-get install g++`

* Java `$ sudo apt-get default-jdk`

* curl `$ sudo apt-get install curl`

* `$ pip3 install -r requirements.txt`

* `$ python3 -m nltk.downloader punkt`

## Default Run
nothing will happen unless you have data

training your data beforehand
get a big dataset 500MB or >
move the dataset into src/AutoPhrase/data directory
edit the auto_phrase.sh file raw_train and model variables accordingly
refer to autophrase if you need further instruction
adjust the phrasal segmentation.sh model location if changed above
temporarily change the TEXT_TO_SEG path to data/yourdata
adjust the single and multi phrase thresholds
now run trainers/word2vec_model_trainer.py

return the TEXT_TO_SEG path in phrasal_segmentation.sh to '../../output_data/tmp/scraped_text.txt'


A default scraper is provided that works with patent IDs.
The scraper must output to two files, titles in one file titled titles.txt, and another file called abstracts.txt in output_data/tmp
then simply run $ ./graphsemantics and the summary will be output not only to the terminal, but also to the summaries.json file in the output_data directory
