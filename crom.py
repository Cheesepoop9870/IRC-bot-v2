import requests
import json
output = []
url = "https://api.crom.avn.sh"

aubody = """
query Search($query: String!) {
  searchUsers(query: $query, filter: {anyBaseUrl: "http://scp-wiki.wikidot.com"}) {
    wikidotInfo {
      displayName
      wikidotId
    }
    statistics{
      rank
      meanRating
      totalRating
      pageCount
      pageCountScp
      pageCountTale
      pageCountGoiFormat
      pageCountArtwork
    }
    authorInfos {
      authorPage {
        wikidotInfo{
          title
        }
      	url
      }
    }
    attributedPages(sort: { key: CREATED_AT, order: DESC }, first: 1) {
          edges {
            node {
              url
              wikidotInfo {
                title
                rating
              }
            }
  				}
		}
  }
}
"""

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
        "createdAt": " ".join(output3[5].split("T"))[0:len(" ".join(output3[5].split("T")))-2],
        "comments": output3[6],
        "authors": output3[7]
      }
      return dict(output4)
    else: 
      return f"Error {response.status_code}"


def ausearch(query):
  variables2 = {
    'query': f'{query}',  # term
  }
  response = requests.post(url=url, json={"query": aubody, "variables": variables2})
  if response.status_code == 200:
    output = response.content.decode('utf-8')
    output2 = json.loads(output)
    output3 = []
    output4 = {}
    output3.append(output2["data"]["searchUsers"][0]["wikidotInfo"]["displayName"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["rank"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["meanRating"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["totalRating"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["pageCount"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["pageCountScp"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["pageCountTale"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["pageCountGoiFormat"])
    output3.append(output2["data"]["searchUsers"][0]["statistics"]["pageCountArtwork"])
    output3.append(output2["data"]["searchUsers"][0]["authorInfos"][0]["authorPage"]["url"])
    output3.append(output2["data"]["searchUsers"][0]["authorInfos"][0]["authorPage"]["wikidotInfo"]["title"])
    output3.append(output2["data"]["searchUsers"][0]["attributedPages"]["edges"][0]["node"]["url"])
    output3.append(output2["data"]["searchUsers"][0]["attributedPages"]["edges"][0]["node"]["wikidotInfo"]["title"])
    output3.append(output2["data"]["searchUsers"][0]["attributedPages"]["edges"][0]["node"]["wikidotInfo"]["rating"])
    #name, rank, mean rating, total rating, page count, scp count, tale count, goi count, artwork count, author page url, author page title, last page url, last page title, last page rating
    output4 = {
      "name": output3[0],
      "rank": output3[1],
      "meanRating": output3[2],
      "totalRating": output3[3],
      "pageCount": output3[4],
      "pageCountScp": output3[5],
      "pageCountTale": output3[6],
      "pageCountGoiFormat": output3[7],
      "pageCountArtwork": output3[8],
      "pageCountOther": output3[4] - output3[5] - output3[6] - output3[7] - output3[8], #other count
      "authorPageUrl": output3[9],
      "authorPageTitle": output3[10],
      "lastPageUrl": output3[11],
      "lastPageTitle": output3[12],
      "lastPageRating": output3[13]
    }
    return output4
    
if __name__ == "__main__":
  output = ausearch("Pouf")
  print(output)


  