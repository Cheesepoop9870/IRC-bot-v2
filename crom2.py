#note: this is deprecated, use crom.py instead
import requests
from bs4 import BeautifulSoup
from crom import wikisearch
import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Any

# Simple in-memory cache
_cache = {}
CACHE_DURATION = 300  # 5 minutes

def is_cache_valid(timestamp: float) -> bool:
    return time.time() - timestamp < CACHE_DURATION

async def wikisearch_async(session: aiohttp.ClientSession, query: str) -> Dict[str, Any]:
    """Async version of wikisearch"""
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
    
    variables = {
        'query': query,
        'noAttributions': False
    }
    
    try:
        async with session.post(url, json={"query": body, "variables": variables}) as response:
            if response.status == 200:
                data = await response.json()
                page_data = data["data"]["searchPages"][0]
                
                # Format rating like the original
                rating = page_data["wikidotInfo"]["rating"]
                vote_count = page_data["wikidotInfo"]["voteCount"]
                upvotes = rating + abs(rating - vote_count)
                downvotes = abs(rating - vote_count)
                
                return {
                    "url": page_data["url"],
                    "title": page_data["wikidotInfo"]["title"],
                    "title2": page_data["alternateTitles"],
                    "rating": f"+{rating} (+{upvotes}/-{downvotes})" if rating >= 0 else f"{rating} (+{upvotes}/-{downvotes})",
                    "createdAt": " ".join(page_data["wikidotInfo"]["createdAt"].split("T"))[0:-2],
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
    # Check cache first
    cache_key = "latest_articles"
    if cache_key in _cache:
        cached_data, timestamp = _cache[cache_key]
        if is_cache_valid(timestamp):
            print("Using cached data")
            return cached_data
    
    print("Fetching fresh data...")
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
        # Fallback to sequential method
        results = []
        for name in article_names:
            try:
                result = wikisearch(name)
                if result:
                    results.append(result)
            except:
                continue
    
    # Cache the results
    _cache[cache_key] = (results, time.time())
    
    return results

if __name__ == "__main__":
    print(latest())
