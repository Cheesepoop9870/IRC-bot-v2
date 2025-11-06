from search_ai import search
results = search("hi")
# results.markdown(
#    extend=True,
#    content_length=10,
# )
markdown = results.markdown(extend=True, content_length=10)
print(results[0])
print(results[1])
print("")
print(markdown)