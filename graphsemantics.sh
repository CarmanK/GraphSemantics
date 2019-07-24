echo "=== Scraping Data ==="
python3 ./scraper_patents.py
echo "=== Data Scraping Finished ==="

echo "=== Starting AutoPhrase ==="
cd AutoPhrase/
./phrasal_segmentation.sh
cd ..
echo "=== AutoPhrase Finished ==="

echo "=== Selecting Phrases ==="
python3 ./phrase_selector_stemmed.py
echo "=== Phrase Selecting Finished ==="

echo "=== Generating Summary ==="
python3 ./summarizer.py
echo "=== Summary Generating Finished ==="

# delete the output_data/tmp directory?
# don't forget to add the output_data directory back to .gitignore
# possibly create a folder for all of the binaries that must be run and only leave the shell scripts outside, the corpus_indexer was already separated to the extra directory
# requirements document