# from search_ai import search

# results = search('pypi')

# print(results[0])

import requests

output = requests.get("https://pastebin.com")
print(output.content)
print(output.status_code)