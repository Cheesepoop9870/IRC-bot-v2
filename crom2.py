import requests
from bs4 import BeautifulSoup
from crom import wikisearch
def latest():
  URL = "https://scp-wiki.wikidot.com/most-recently-created"
  r = requests.get(URL)
  soup = BeautifulSoup(r.content, 'html5lib')
  html = soup.find_all('div', attrs = {'class':'list-pages-box'})
  output = html[2].text.strip().split("\n")
  output =  [item for item in output if item]
  # Skip the header (first 3 elements) and group every 3 elements
  data_without_header = output[3:]  # Remove header elements
  output2 = []
  
  # Group every 3 elements into sublists
  for i in range(0, len(data_without_header), 3):
    if i + 2 < len(data_without_header):  # Make sure we have all 3 elements
      output2.append(data_without_header[i:i+3])
  output3 = []
  for i in range(0, len(output2)):
    output3.append(wikisearch(latest()[i][0]))
  return output3[:5]
if __name__ == "__main__":
  print(latest())