echo "=== Scraping Data ==="
# python3 ./scraper.py
echo "=== Data Scraping Finished ==="

echo "=== Starting AutoPhrase ==="
cd AutoPhrase/
./phrasal_segmentation.sh
cd ..
echo "=== AutoPhrase Finished ==="

echo "=== Selecting Phrases ==="
python3 ./phrase_selector.py
echo "=== Phrase Selecting Finished ==="

# echo "=== Starting to Index Text to Elasticsearch ==="
# echo "=== Indexing Text to Elasticsearch Finished ==="