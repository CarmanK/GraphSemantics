# GraphSemantics
Traverse an Abello fixed point. Scrape the metadata associated with each vertex. Use AutoPhrase to extract information about the data. Build a story of all of the data.

# Documentation
Note that this is currently a proof of concept and much of the code is messy and unorganized and doesn't transition fluenty yet. This documentation was also written fairly quickly.

The entire process will eventually be able to run all sequentially once everything is finished in the graphsemantics.sh script. This will be machine dependant due to the use of elasticsearch!

## Step 1
1. scraper.py takes lists of urls associated with each layer (the metadata for each protein vertex) and uses the functions defined in html_requests.py to scrape the title and abstract of the associated PubMed publication.

  * This is currently specific to this component for scraping the exact paragraph and header associated with the title and abstract of the publication.
  * The output is stored in two places:
     * output_data/tmp/scraped_text.txt: each line is in the form title + ' ' + abstract for each website
     * output_data/tmp/meta_scraped_text.txt: a list of the lengths of the various layers for use in decomposing the scraped_txt file back to layers later on.

2. The scraped_text.txt is then run through AutoPhrase, which was trained on a 1GB file containing various other PubMed abstracts concatenated with the scraped text from the websites. The output is stored in ../output_data/tmp/segmentation.txt. This text file tags all of the important phrases obtained from step 1.1.
   
3. The jupiter file named phrase_selector.py then extracts the phrases from segmentation.txt with regards to their respective layer and calculates the TF-IDF scores to select the top-k phrases per layer.

  * The k we chose for this proof of concept was 10. This k should be tinkered with for more efficient computations.

## Step 2
1. elastic.py then indexes all of the titles + abstracts obtained in step 1.1 to our elasticsearch index.

  * Currently, our indexing is in one file combined with the querying, and is not in function form, and should be separated and cleaned up.
  * elastic.py should use the count() method to obtain the current id for a specific index instead of just using the variable i like we did.

2. elastic.py then takes the top-k output obtained from step 1.3 and queries every possible phrase combination in each layer in our indexed abstracts. The top-k articles are then jumped to a json file.
   
  * The current output format is:
     * "phrase": phrases
     * "article": article
  * The output is stored as ./output_data/tmp/article_pool.json.
  * We are still currently playing around with the value of k for the pool of articles. We have tried 10 and 50 so far, but the next step is computationally heavy, so there needs to be a healthy balance.

3. The last step takes the output_data folder and computes the BM25 score to find which sentences cover the most unique phrases.

  * This step can be optimized to be more efficient.

## Thoughts/changes for future iterations
* tweek the values of our k
* upload 100MB to elasticsearch instead of only 10MB
* phrase_selector.py needs to be cleaned up and be made scalable/more efficient
* The elastic search step needs to be broken into two steps
  * First, the unique, newly scraped text needs to be indexed by elasticsearch
  * Second, the pairs need to be queried and the article pool needs to be built