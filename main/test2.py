import os
import glob

# Set LD_LIBRARY_PATH to find libstdc++
gcc_paths = glob.glob('/nix/store/*-gcc-*/lib')
if gcc_paths:
    os.environ['LD_LIBRARY_PATH'] = f"{gcc_paths[0]}:{os.environ.get('LD_LIBRARY_PATH', '')}"

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