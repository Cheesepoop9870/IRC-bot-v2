import requests
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
      return response.content
    else: 
      return f"Error {response.status_code}"

if __name__ == "__main__":
  print(wikisearch("ts hu").split