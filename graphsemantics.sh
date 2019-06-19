echo "=== Starting Scraper ==="
python3 ./scraper.py
echo "=== Scraper Finished ==="

echo "=== Starting AutoPhrase ==="
cd AutoPhrase/
./phrasal_segmentation.sh
cd ..
echo "=== AutoPhrase Finished ==="

echo "=== Starting Phrase Selector ==="
python3 ./phrase_selector.py
echo "=== Phrase Selector Finished ==="

# echo "=== Starting to Index Text to Elasticsearch ==="
# echo "=== Indexing Text to Elasticsearch Finished ==="