echo "=== Scraping Data ==="
python3 ./scraper.py
echo "=== Data Scraping Finished ==="

echo "=== Starting AutoPhrase ==="
cd AutoPhrase/
./phrasal_segmentation.sh
cd ..
echo "=== AutoPhrase Finished ==="

echo "=== Selecting Phrases ==="
python3 ./phrase_selector.py
echo "=== Phrase Selecting Finished ==="

# echo "=== Indexing Scraped Text to Elasticsearch ==="
python3 ./elastic_indexer.py
# echo "=== Scraped Text Indexing to Elasticsearch Finished ==="

# echo "=== Pooling Top Articles ==="
python3 ./elastic_querier.py
# echo "=== Top Article Pooling Finished ==="

# echo "=== Generating Summary ==="
python3 ./summarizer.py
# echo "=== Summary Generating Finished ==="

# delete the output_data/tmp directory?
# don't forget to add the output_data directory back to .gitignore
# possibly create a folder for all of the binaries that must be run and only leave the shell scripts outside
# requirements document