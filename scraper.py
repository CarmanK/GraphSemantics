from html_requests import html_get
from bs4 import BeautifulSoup

# Top
layer1 = [
    "https://www.rcsb.org/structure/1j0o",
    "https://www.rcsb.org/structure/3mdt",
    "https://www.rcsb.org/structure/2r4x",
    "https://www.rcsb.org/structure/4il6",
    "https://www.rcsb.org/structure/19hc",
    "https://www.rcsb.org/structure/4rkm"
]

# Middle
layer2 = [
    "https://www.rcsb.org/structure/1yot",
    "https://www.rcsb.org/structure/3hhb",
    "https://www.rcsb.org/structure/1gli",
    "https://www.rcsb.org/structure/1y85",
    "https://www.rcsb.org/structure/2hhe",
    "https://www.rcsb.org/structure/1y45",
    "https://www.rcsb.org/structure/1a3n",
    "https://www.rcsb.org/structure/4hhb",
    "https://www.rcsb.org/structure/1y0b",
    "https://www.rcsb.org/structure/1xz2",
    "https://www.rcsb.org/structure/1y2z",
    "https://www.rcsb.org/structure/2hhb",
    "https://www.rcsb.org/structure/1bab"
]

# Bottom
layer3 = [
    "https://www.rcsb.org/structure/4u9b",
    "https://www.rcsb.org/structure/2z47",
    "https://www.rcsb.org/structure/2vr0",
    "https://www.rcsb.org/structure/2r4y",
    "https://www.rcsb.org/structure/3mdm"
]

layers = [layer1, layer2, layer3]
with open('scrapedText.txt', 'w') as file:
    for i in range(len(layers)):
        for j in range(len(layers[i])):
            raw_html = html_get(layers[i][j])
            if raw_html is not None:
                html = BeautifulSoup(raw_html, 'html.parser')

                html_titles = html.find(id = "primarycitation")
                if html_titles is not None:
                    title = html_titles.select('h4')[0].text
                else:
                    title = ""
                    print("Error finding title data at {0}".format(layers[i][j]))

                html_paragraphs = html.find(id = "abstractFull")
                if html_paragraphs is not None:
                    abstract = html_paragraphs.select('p')[0].text
                else:
                    abstract = ""
                    print("Error finding abstract data at {0}".format(layers[i][j]))

                file.write(str(i + 1))
                file.write("\n" + title + "\n")
                file.write(abstract + "\n")
            else:
                print("Error scraping data from {0}".format(layers[i][j]))
    file.write("EOF")