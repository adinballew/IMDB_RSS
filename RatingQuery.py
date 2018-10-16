import json
from operator import itemgetter

with open('report.json') as f:
    data = json.load(f)

sorted_data = sorted(data, key=itemgetter("Released"), reverse=True)

for item in sorted_data:
    if "Title" in item:
        print("Title: {0}\n"
              "IMDB Rating: {1}""\n"
              "Metascore: {2}\n"
              "Release Date: {3}\n"
              .format(item["Title"],
                      item["imdbRating"],
                      item["Metascore"],
                      item["Released"]))
