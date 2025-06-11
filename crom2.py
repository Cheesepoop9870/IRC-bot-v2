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
  # Skip the header (first 3 elements) and group every 3 elements
  data_without_header = output[3:]  # Remove header elements
  output2 = []
  
  # Group every 3 elements into sublists
  for i in range(0, len(data_without_header), 3):
    if i + 2 < len(data_without_header):  # Make sure we have all 3 elements
      output2.append(data_without_header[i:i+3])
  
  print("")
  print(output2[:10])  # Print first 10 entries to avoid overwhelming output
if __name__ == "__main__":
  latest()