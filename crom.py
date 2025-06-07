import requests
import numpy as np
output = []
url = "https://api.crom.avn.sh"

body = """
query Search($query: String!, $noAttributions: Boolean!) {
  searchPages(query: $query, filter: {anyBaseUrl: "http://scp-wiki.wikidot.com"}) {
    url
    wikidotInfo {
      title
      rating
      createdAt
      voteCount
      commentCount
      
    }
    attributions @skip(if: $noAttributions) {
      type
      user {
        name
      }
      date
    }
  }
}
"""

def wikisearch(query):
    variables2 = {
      'query': f'{query}',  # term
      'noAttributions': False
    }
    response = requests.post(url=url, json={"query": body, "variables": variables2})
    if response.status_code == 200:
      return response.content.decode('utf-8')
    else: 
      return f"Error {response.status_code}"

if __name__ == "__main__":
  output = wikisearch("ts hu").split(",")
  print(f"-1 {output}")
  print("\n")
  urlcount = 0
  coords = 0
  print(len(output))
  for x in range (0, len(output)):
    print(f"{x} {output[x]}")
    if "url" in output[x]:
      urlcount = urlcount + 1
      if urlcount == 2:
        coords = x
        break
  print("\n")
  if urlcount >= 2:
    for x in range (len(output)-1, 0, -1):
      if coords+x < len(output):
        print(f"{x} {output[x]}")
        output.pop(coords+x)
  else:
    coords = len(output)
  print("\n")
  output2 = np.array([])  # Initialize as empty 1D array
  output3 = []
  print(f"0 {output}")
  print("\n")
  print(f"1 {output[0]}")
  print("\n")
  print(f"2 {output[0:5+(coords-5)]}")
  output4 = output[0]
  print("\n")
  output3 = output4.split('{\"data\":{\"searchPages\":[{')
  output3.pop(0)
  print(f"3 {output3[0]}")
  print("\n")
  output.pop(0)
  output.insert(0, str(output3[0]))
  print("\n")
  print(f"4 {output[0:5+(coords-5)]}")
  output2 = np.append(output2, output[0:5+(coords-5)])  # Assign the result back to output2
  print("\n")
  print(f"5 {output2}")
  ########################################
  print("\n")
  print(f"6 {output2}")
  print("\n")
  for x in range(0, len(output2)):
    print(f"{x} {output2[x]}")
  print("\n")
  output4 = output2[1]
  output3 = output4.split('\"wikidotInfo\":{')
  output3.pop(0)
  print(f"7 {output3}")
  output2[1] = output3[0]
  print("\n")
  print(f"8 {output2}")
  print("\n")
  for x in range(0, len(output2)):
    print(f"{x} {output2[x]}")
  print("\n")
  output4 = output2[6]
  output3 = output4.split('\"attributions\":[{')
  output3.pop(0)
  print(f"9 {output3}")
  print("\n")
  output2[6] = output3[0]
  for x in range(0, len(output2)):
    print(f"{x} {output2[x]}")
