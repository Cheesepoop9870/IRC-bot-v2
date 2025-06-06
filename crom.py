# we have imported the requests module 
import requests
url = "https://api.crom.avn.sh"

body = """
query Search($query: String!, $noAttributions: Boolean!) {
  searchPages(query: $query, filter: { anyBaseUrl: "http://scp-wiki.wikidot.com" }) {
    url
    wikidotInfo {
      title
      rating
    }
    attributions @skip(if: $noAttributions) {
      type
      user {
        name
      }
    }
  }
}
"""

variables = {
    'query': 'SCP',  # Add your search term here
    'noAttributions': False
}

response = requests.post(url=url, json={"query": body, "variables": variables})
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)


# def wikisearch():