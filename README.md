Post Analyzer ver. 0.6
======================

Post Analyzer is a text processing server. It analyzes a text block (forum post - for example) and it returns a JSON
document with its analysis.  The analysis can be used to determine key phrases and whether the post contains
colloquialisms (bad words or the use of slang).  The underlying text processing engine correct misspellings and expands
net slang to full phrases during its analysis.

PostAnalyzer is based on Python 2.7 and runs as a RESTful Tornado web application and requires the use of the NLTK,
the natural language toolkit.


