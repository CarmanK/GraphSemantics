cd src/
echo "=== Scraping Data ==="
python3 ./scraper.py

echo "=== Starting AutoPhrase ==="
cd AutoPhrase/
./phrasal_segmentation.sh
cd ..

echo "=== Selecting Phrases ==="
python3 ./phrase_selector_stemmed.py

echo "=== Generating Summary ==="
python3 ./summarizer.py
cd ..