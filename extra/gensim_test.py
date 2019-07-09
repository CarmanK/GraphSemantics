from gensim.summarization import summarize
from gensim.summarization import keywords

with open('./output_data/tmp/scraped_text.txt', 'r') as scraped_input_file:
    lines = scraped_input_file.readlines()

text = ' '.join(lines)
# print(text)

print('no params')
print(summarize(text))
print('\n\n50')
print(summarize(text, word_count = 50))
print('\n\n100')
print(summarize(text, word_count = 100))
print('\n\n100')
print(summarize(text, word_count = 150))
print('\n\n100')
print(summarize(text, word_count = 200))
print('\n\nkeys')
print(keywords(text))