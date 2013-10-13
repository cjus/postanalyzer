Post Analyzer ver. 0.6
======================

Post Analyzer is a text processing server. It analyzes a text block (forum post - for example) and it returns a JSON
document with its analysis.  The analysis can be used to determine key phrases and whether the post contains
colloquialisms (bad words or the use of slang).  The underlying text processing engine correct misspellings and expands
net slang to full phrases during its analysis.

PostAnalyzer is based on Python 2.7 and runs as a RESTful Tornado web application and requires the use of the NLTK,
the natural language toolkit.

## Example:
curl -H 'Content-Type: application/json' -X  POST 'http://localhost:8889/api/fullscan' -d '{"text":"Yo here is a tip for your ass: One of the rules that you hear a lot is to simplify your image. Sometimes, especially in street photography, you can’t simplify the scene. Sometimes the scene has to speak for itself. Whether it’s chaos or clutter, sometimes you need to just go with what you have and work with it. There are stories that can be told just by being the silent observer and recording the image at that place and time. Lori Peterson is an award winning photographer based out of the St. Louis Metro Area. Her work ranges from creative portraits to very unique fine art photography. See more at: http://digital-photography-school.com/photography-rules-finding-balance "}'

## Response:
{
   "status":"success",
   "result":{
      "has_bad_words":true,
      "richness_of_post":"0.50",
      "contacts":[
      ],
      "has_qualifier":false,
      "has_slang":true,
      "has_link":true,
      "uris":[
         "http://digital-photography-school.com/photography-rules-finding-balance"
      ],
      "subphrases":[
         "yo",
         "street photography",
         "silent observer",
         "peterson",
         "st",
         "lori peterson",
         "louis",
         "work ranges",
         "fine art",
         "art photography",
         "fine art photography"
      ],
      "has_net_lingo":false
   }
}
