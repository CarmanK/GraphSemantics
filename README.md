# GraphSemantics
Traverse an Abello fixed point. Scrape the metadata associated with each vertex. Use AutoPhrase to extract information about the data. Build a story of all of the data.

# Documentation
Note that this is currently a proof of concept and much of the code is messy and unorganized and doesn't transition fluenty yet. This documentation was also written fairly quickly.

## Step 1
1. scraper.py takes lists of urls associated with each layer (the metadata for each protein vertex) and uses the functions defined in html_requests.py to scrape the title and abstract of the associated PubMed publication.

  * This is currently specific to this component for scraping the exact paragraph and header associated with the title and abstract of the publication.
  * The output is named scrapedText.txt and is in the following format:
     * layer number
     * title
     * abstract
   * This output should probably be converted to a json list of lists where the first index is the layer number and the title and abstract are combined in another list in thatlayer.

2. The scrapedText.txt is then run through AutoPhrase, which was trained on a 1GB file containing various other PubMed abstracts, and output to segmentation.txt. This text file tags all of the important phrases obtained from step 1.1.
3. The jupiter file named step1.jpynb then extracts the phrases from segmentation.txt with regards to their respective layer and calculates the TF-IDF scores to select the top-k phrases per layer.

  * The k we chose for this proof of concept was 10. This k should be tinkered with for more efficient computations.
  * The output of this step is three separate jsons in the format "key": TF-IDF score.
     * The output of this should be converted to a json list of lists as well since the TF-IDF score is never used again and there is no point in having 3 separate files.

## Step 2
1. elastic.py then indexes all of the titles + abstracts obtained in step 1.1 to our elasticsearch index.

  * Currently, our indexing is in one file combined with the querying, and is not in function form, and should be separated and cleaned up.
  * elastic.py should use the count() method to obtain the current id for a specific index instead of just using the variable i like we did.

2. elastic.py then takes the top-k output obtained from step 1.3 and queries every possible phrase combination in each layer in our indexed abstracts. The top-k articles are then jumped to a json file.
   
  * The current output format is:
     * "phrase": phrases
     * "article": article
  * The phrase may or may not need to be saved, to be determined.
  * The output is stored in a folder named output_data, and the other outputs should also be moved to this folder.
  * The output is currently stored in a separate file per layer named layer_number_output.json, but this can also be converted to a json list.
     * This was a design choice for now because it was easier to work with smaller files for this early design, as they can get fairly big.
  * We are still currently playing around with the value of k for the pool of articles. We have tried 10 and 50 so far, but the next step is computationally heavy, so there needs to be a healthy balance.

3. The last step takes the output_data folder and computes the BM25 score to find which sentences cover the most unique phrases.

  * This step can be optimized to be more efficient.

## Thoughts/changes for future iterations
* Use greedy algorithm, choose the sentence that covers the most number of unvisited phrase or unvisted pair of phrases at each iteration instead of BM25? for step 2.3 (and other tweeks)
* fixes noted above in the other steps (in progress)
* tweek the values of our k
* upload 100MB to elasticsearch instead of only 10MB
* retrain the 1GB model in autophrase and make sure to cat the scraped titles+abstracts into it