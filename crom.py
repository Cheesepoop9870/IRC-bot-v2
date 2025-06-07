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
  output2 = np.array([],[])
  output3 = []
  print(f"0 {output}")
  print("\n")
  print(f"1 {output[0]}")
  print("\n")
  print(f"2 {output[0:8]}")
  output4 = output[0]
  print("\n")
  output3 = output4.split('{\"data\":{\"searchPages\":[{')
  output3.pop(0)
  print(f"3 {str(output3[0])}")
  print("\n")
  output.pop(0)
  output.insert(0, str(output4))
  print("\n")
  print(f"4 {output[0:8]}")
  np.append(output2, output)
  print("\n")
  print(f"5 {output2}")
  