echo "=== Starting Scraper ==="
python3 ./scraper.py
echo "=== Scraper Finished ==="

echo "=== Starting AutoPhrase ==="
cd AutoPhrase/
./phrasal_segmentation.sh
cd ..
echo "=== AutoPhrase Finished ==="

echo "=== Starting Phrase Analysis ==="
echo "=== Phrase Analysis Finished ==="