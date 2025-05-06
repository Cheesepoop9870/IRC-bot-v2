
import sys
sys.path.insert(0, 'local_pyscp')
import pyscp

wiki = pyscp.wikidot.Wiki('www.scpwiki.com')
p = wiki('scp-837')
print('"{}" has a rating of {}, {} revisions, and {} comments.'
    .format(p.title, p.rating, len(p.history), len(p.comments)))
