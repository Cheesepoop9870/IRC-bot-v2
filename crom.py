import requests
import json
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
    alternateTitles {
      title
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


def addplus(arg):
    if arg > 0:
        return f"+{arg}"
    else:
        return f"{arg}"


def wikisearch(query):
    variables2 = {
      'query': f'{query}',  # term
      'noAttributions': False
    }
    response = requests.post(url=url, json={"query": body, "variables": variables2})
    if response.status_code == 200:
      output = response.content.decode('utf-8')
      output2 = json.loads(output)
      output3 = []
      output4 = {}
      output3.append(output2["data"]["searchPages"][0]["url"]) 
      output3.append(output2["data"]["searchPages"][0]["wikidotInfo"]["title"])
      output3.append(output2["data"]["searchPages"][0]["alternateTitles"])
      output3.append(output2["data"]["searchPages"][0]["wikidotInfo"]["rating"])
      output3.append(output2["data"]["searchPages"][0]["wikidotInfo"]["voteCount"])
      output3.append(output2["data"]["searchPages"][0]["wikidotInfo"]["createdAt"])
      output3.append(output2["data"]["searchPages"][0]["wikidotInfo"]["commentCount"])
      output3.append(output2["data"]["searchPages"][0]["attributions"])
      #url, title, title2, rating, total votes, created at, total comments, authors
      output4 = {
        "url": output3[0],
        "title": output3[1],
        "title2": output3[2],
        "rating": f"{addplus(output3[3])} (+{output3[3] + abs(output3[3]-output3[4])}/-{abs(output3[3]-output3[4])})", #full rating (+upvotes/-downvotes)
        "createdAt": output3[5],
        "comments": output3[6],
        "authors": output3[7]
      }
      return dict(output4)
    else: 
      return f"Error {response.status_code}"
if __name__ == "__main__":
  output = wikisearch("8981")
  for x in range (0, len(output["authors"])):
    print(dict(output["authors"][x])["user"]["name"])
  
