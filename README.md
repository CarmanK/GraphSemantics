# Automated Phrase and Sentence Mining to Develop Graph Stories


## Research Documentation

Please cite the following paper if you are using my process, thanks!
* Kevin Carman, "[Automated Phrase and Sentence Mining to Develop Graph Stories](http://reu.dimacs.rutgers.edu/~kc1125/content/Kevin_Carman_Research_Paper.pdf)," Rutgers University, 2019.

## Related GitHub Repository

*  [AutoPhrase](https://github.com/shangjingbo1226/AutoPhrase)

## Requirements
Ubuntu 18.04:
* g++ `$ sudo apt-get install g++`
* Java `$ sudo apt-get default-jdk`
* curl `$ sudo apt-get install curl`
* `$ pip3 install -r requirements.txt`
* `$ python3 -m nltk.downloader punkt`

## Training the models
You must train the AutoPhrase and word2vec model before running my process! Refer to the AutoPhrase repository linked above for more information regarding the thresholds.

1. Gather a large corpus of data, preferably >500MB
2. Move the dataset into src/AutoPhrase/data
3. Edit the auto_phrase.sh MODEL and RAW_TRAIN variables where necessary
4. Run `$ ./auto_phrase.sh` from the src/AutoPhrase directory
5. Edit the phrasal_segmentation.sh MODEL variable if necessary
6. Temporarily change the TEXT_TO_SEG path to data/training_data.txt
7. Adjust the HIGHLIGHT_SINGLE and HIGHLIGHT_MULTI variables to your liking
8. Run `$ ./phrasal_segmentation.sh`
9. Return the TEXT_TO_SEG path back to ../../output_data/tmp/titles.txt
10. Run `$ python3 word2vec_model_trainer.py` from the src/word2vec_models directory

## Running the Process
A default data collector and default data are included to show what an expected output looks like, but the models are not included due to their size.

If you build your own data collector, it must output the following two files to the output_data/tmp directory.
* titles.txt
* abstracts.txt

Run `$ ./graphsemantics` to begin the process.

Output will not only be shown and highlighted in the terminal, but will also be saved in output_data/summaries.json.
