from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import csv

# last names of aldermen (2005-2019) and their unique ids
name_and_id = []
name_and_id.append(["roddy", 1316])
name_and_id.append(["flowers", 1301])
name_and_id.append(["tyus", 1300])
name_and_id.append(["middlebrook", 1525])
name_and_id.append(["bosley", 1514])
name_and_id.append(["moore", 1303])
name_and_id.append(["hubbard", 1304])
name_and_id.append(["ingrassia", 1305])
name_and_id.append(["coatar", 1500])
name_and_id.append(["rice", 1526])
name_and_id.append(["guenther", 1515])
name_and_id.append(["vollmer", 1309])
name_and_id.append(["martin", 1520])
name_and_id.append(["arnowitz", 1311])
name_and_id.append(["murphy", 1312])
name_and_id.append(["howard", 1313])
name_and_id.append(["green", 1314])
name_and_id.append(["oldenburg", 1516])
name_and_id.append(["kennedy", 1317])
name_and_id.append(["davis", 1318])
name_and_id.append(["spencer", 1511])
name_and_id.append(["muhammad", 1517])
name_and_id.append(["boyd", 1321])
name_and_id.append(["vaccaro", 1322])
name_and_id.append(["ogilvie", 1323])
name_and_id.append(["cohn", 1324])
name_and_id.append(["williamson", 1325])
name_and_id.append(["pboyd", 1518])
name_and_id.append(["navarro", 1521])
name_and_id.append(["reed", 1328])

year = []
for i in range(2005, 2019):
    year.append(str(i) + "-" + str(i + 1))

print(year)