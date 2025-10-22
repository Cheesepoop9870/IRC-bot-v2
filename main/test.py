import crom
authors = []

output = crom.wikisearch("SCP-6500")
print(output["url"])
print(output["title"])
print(output["title2"][0]["title"])
print(output["rating"])
print(output["createdAt"])
print(output["comments"])
print(output["authors"])
print("")

for x in range(0, len(output["authors"])): #cycles through authors
    print(dict(output["authors"][x])["user"]["name"]) if output["authors"][x]["isCurrent"] else None #prints current author(s)
    authors.append(dict(output["authors"][x])["user"]["name"]) if output["authors"][x]["isCurrent"] else None #adds to list
print("")
print(output["authors2"])
print("")

if authors:
  print(authors)
else: #attmeta fail 
  authors = []
  for x in range(0, len(output["authors2"])): #uses backup list
    print(dict(output["authors2"][x])["user"]["name"])
    authors.append(dict(output["authors2"][x])["user"]["name"])
    
  print("")  
  print(authors)