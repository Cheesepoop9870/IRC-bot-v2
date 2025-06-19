import requests
import json
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time
import threading
from typing import List, Dict, Any
output = []
url = "https://api.crom.avn.sh"

# Simple in-memory cache
_cache = {}
CACHE_DURATION = 300  # 5 minutes
_cache_thread = None
_cache_running = False



def is_cache_valid(timestamp: float) -> bool:
    return time.time() - timestamp < CACHE_DURATION

def _fetch_latest_data():
    """Internal function to fetch latest data without cache checks"""
    try:
        URL = "https://scp-wiki.wikidot.com/most-recently-created"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        html = soup.find_all('div', attrs={'class': 'list-pages-box'})
        output = html[2].text.strip().split("\n")
        output = [item for item in output if item]
        
        # Skip the header (first 3 elements) and group every 3 elements
        data_without_header = output[3:]  # Remove header elements
        output2 = []
        
        # Group every 3 elements into sublists
        for i in range(0, len(data_without_header), 3):
            if i + 2 < len(data_without_header):  # Make sure we have all 3 elements
                output2.append(data_without_header[i:i+3])
        
        # Get article names for parallel fetching
        article_names = [output2[i][0] for i in range(min(5, len(output2)))]
        
        # Fetch articles in parallel using asyncio
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(fetch_latest_parallel(article_names))
            loop.close()
        except Exception as e:
            print(f"Error in parallel fetch: {e}")
            print("Falling back to sequential method")
            # Fallback to sequential method
            results = []
            for name in article_names:
                try:
                    result = wikisearch(name)
                    if result:
                        results.append(result)
                except:
                    continue
        
        return results
    except Exception as e:
        print(f"Error fetching latest data: {e}")
        return []

def _background_cache_refresh():
    """Background thread function to refresh cache every 5 minutes"""
    global _cache_running
    while _cache_running:
        try:
            print("Background: Refreshing cache...")
            results = _fetch_latest_data()
            if results:
                _cache["latest_articles"] = (results, time.time())
                print(f"Background: Cache updated with {len(results)} articles")
            else:
                print("Background: Failed to fetch new data, keeping existing cache")
        except Exception as e:
            print(f"Background cache refresh error: {e}")
        
        # Wait 5 minutes before next refresh
        for _ in range(300):  # 300 seconds = 5 minutes
            if not _cache_running:
                break
            time.sleep(1)

def start_background_cache():
    """Start the background cache refresh thread"""
    global _cache_thread, _cache_running
    if not _cache_running:
        _cache_running = True
        _cache_thread = threading.Thread(target=_background_cache_refresh, daemon=True)
        _cache_thread.start()
        print("Background cache refresh started")

def stop_background_cache():
    """Stop the background cache refresh thread"""
    global _cache_running
    _cache_running = False
    print("Background cache refresh stopped")
def refresh_cache():
    """Manually refresh the cache with fresh data"""
    global _cache
    print("Manually refreshing cache...")
    # Clear existing cache
    cache_key = "latest_articles"
    if cache_key in _cache:
        del _cache[cache_key]
    
    # Fetch fresh data
    results = _fetch_latest_data()
    
    if results:
        # Cache the new results
        _cache[cache_key] = (results, time.time())
        print(f"Cache manually refreshed with {len(results)} articles")
        return results
    else:
        print("Failed to refresh cache - no data retrieved")
        return []

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
                voteCount
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
        "rating": f"{addplus(output3[3])} (+{(output3[3] + output3[4])/2}/-{(output3[3] - output3[4])/2})", #full rating (+upvotes/-downvotes)
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
    if output2["data"]["searchUsers"][0]["authorInfos"] == []: #no author page
      output3.append("")
      output3.append("")
    else:
      output3.append(output2["data"]["searchUsers"][0]["authorInfos"][0]["authorPage"]["url"])
      output3.append(output2["data"]["searchUsers"][0]["authorInfos"][0]["authorPage"]["wikidotInfo"]["title"])
    output3.append(output2["data"]["searchUsers"][0]["attributedPages"]["edges"][0]["node"]["url"])
    output3.append(output2["data"]["searchUsers"][0]["attributedPages"]["edges"][0]["node"]["wikidotInfo"]["title"])
    output3.append(output2["data"]["searchUsers"][0]["attributedPages"]["edges"][0]["node"]["wikidotInfo"]["rating"])
    output3.append(output2["data"]["searchUsers"][0]["attributedPages"]["edges"][0]["node"]["wikidotInfo"]["voteCount"])
    #name, rank, mean rating, total rating, page count, scp count, tale count, goi count, artwork count, author page url, author page title, last page url, last page title, last page rating
    
    output4 = {
      "name": output3[0],
      "rank": output3[1],
      "meanRating": addplus(output3[2]),
      "totalRating": addplus(output3[3]),
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
      "lastPageRating": f"{addplus(output3[13])} (+{(output3[13] + output3[14])/2}/-{(output3[13] - output3[14])/2})"
    }
    return output4

async def wikisearch_async(session: aiohttp.ClientSession, query: str) -> Dict[str, Any]:
    """Async version of wikisearch"""
    
    variables2 = {
        'query': query,
        'noAttributions': False
    }
    
    try:
        async with session.post(url=url, json={"query": body, "variables": variables2}) as response:
            if response.status == 200:
                data = await response.json()
                page_data = data["data"]["searchPages"][0]
                
                # Format the same as original wikisearch
                rating = page_data["wikidotInfo"]["rating"]
                vote_count = page_data["wikidotInfo"]["voteCount"]
                
                return {
                    "url": page_data["url"],
                    "title": page_data["wikidotInfo"]["title"],
                    "title2": page_data["alternateTitles"],
                    "rating": f"{addplus(rating)} (+{(rating + vote_count)/2}/-{(rating - vote_count)/2})",
                    "createdAt": " ".join(page_data["wikidotInfo"]["createdAt"].split("T"))[0:len(" ".join(page_data["wikidotInfo"]["createdAt"].split("T")))-2],
                    "comments": page_data["wikidotInfo"]["commentCount"],
                    "authors": page_data["attributions"]
                }
            else:
                return None
    except Exception as e:
        print(f"Error in async wikisearch: {e}")
        return None

async def fetch_latest_parallel(article_names: List[str]) -> List[Dict[str, Any]]:
    """Fetch multiple articles in parallel"""
    timeout = aiohttp.ClientTimeout(total=10)  # 10 second timeout
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [wikisearch_async(session, name) for name in article_names]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None results and exceptions
        valid_results = []
        for result in results:
            if result is not None and not isinstance(result, Exception):
                valid_results.append(result)
        
        return valid_results

def latest():
    # Start background cache refresh if not already running
    start_background_cache()
    
    # Check cache first
    cache_key = "latest_articles"
    if cache_key in _cache:
        cached_data, timestamp = _cache[cache_key]
        if is_cache_valid(timestamp):
            print("Using cached data")
            return cached_data
    
    # If no valid cache, fetch fresh data immediately
    print("Fetching fresh data...")
    results = _fetch_latest_data()
    
    # Cache the results
    _cache[cache_key] = (results, time.time())
    
    return results
if __name__ == "__main__":
  output = ausearch("thew")
  print(type(output))
  print(output)


  
