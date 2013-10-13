Post Analyzer ver. 0.6
======================

Post Analyzer is a text processing server. It analyzes a text block (forum post - for example) and it returns a JSON
document with its analysis.  The analysis can be used to determine key phrases and whether the post contains
colloquialisms (bad words or the use of slang).  The underlying text processing engine performs a number of text
transformation such as: correcting misspellings and expanding net slang to full phrases during its analysis.

PostAnalyzer is based on Python 2.7 and runs as a RESTful Tornado web application and requires the use of the NLTK,
the natural language toolkit.

### Example using curl command to send (via HTTP POST) JSON to Post Analyzer server:
$ curl -H 'Content-Type: application/json' -X  POST 'http://localhost:8889/api/fullscan' -d '{"text":"One of the rules that you hear a lot is to simplify your image. Sometimes, especially in street photography, you can’t simplify the scene. Sometimes the scene has to speak for itself. Whether it’s chaos or clutter, sometimes you need to just go with what you have and work with it. There are stories that can be told just by being the silent observer and recording the image at that place and time. Lori Peterson is an award winning photographer based out of the St. Louis Metro Area. Her work ranges from creative portraits to very unique fine art photography. See more at: http://digital-photography-school.com/photography-rules-finding-balance "}'

### Response:
```javascript
{
   "status":"success",
   "result":{
      "has_bad_words":false,
      "richness_of_post":"19.73",
      "contacts":[],
      "has_qualifier":false,
      "has_slang":false,
      "has_link":true,
      "uris":[
         "http://digital-photography-school.com/photography-rules-finding-balance"
      ],
      "subphrases":[
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
```

### License
This code is offered under a BSD license.

### Code History
I started playing with textual analysis in 2009 when I was working on a kids site (educational search engine) called ZoeyBot.
I later used the Python code used here to create tweetspeedreader and twsift - tools that process Twitter streams. Along the way
I learned a lot about natural language processing and now have a need for a server which can, once again, process text. I'm offering the code here in case anyone else has that same need.

### Roadmap
Since this code is from my older Python experiences it does need some work to bring it up to modern standards.
I've recently made a pass towards PEP8 adherence, however, the code in the core engine could use some DRYing up.
Most of the features offered by the core engine are not being exposed in the server's API - so there lie opportunities.
Additionally, the core really need unit tests!  All of this requires time/effort and I may not get to this any time soon.
Contributions are welcomed!