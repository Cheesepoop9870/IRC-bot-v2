import requests
import numpy as np
from bs4 import BeautifulSoup
from crom import wikisearch
def latest():
  URL = "https://scp-wiki.wikidot.com/most-recently-created"
  r = requests.get(URL)
  soup = BeautifulSoup(r.content, 'html5lib')
  html = soup.find_all('div', attrs = {'class':'list-pages-box'})
  output = html[2].text.strip().split("\n")
  output =  [item for item in output if item]
  print(output)
  output2 = []
  output2.append(output[3:6])
  output2.append(output[7:10])
  output2.append(output[11:14])
  print("")
  print(output2)
if __name__ == "__main__":
  latest()