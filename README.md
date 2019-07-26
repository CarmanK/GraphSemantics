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

## Training the models
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

## Running the Process
A default data collector and default data are included to show what an expected output looks like, but the models are not included due to their size.

If you build your own data collector, it must output the following two files to the output_data/tmp directory.
* titles.txt
* abstracts.txt

Run `$ ./graphsemantics` to begin the process.

Output will not only be shown and highlighted in the terminal, but will also be saved in output_data/summaries.json.