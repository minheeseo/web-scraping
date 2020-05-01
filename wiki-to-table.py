# example tables
# https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents
# https://en.wikipedia.org/wiki/List_of_counties_by_U.S._state

import pandas as pd
link = "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Alabama"
tables = pd.read_html(link,header=1)[0]
#print(tables)
tables.to_csv("data/wikiTable/Alabama.csv", sep=',')