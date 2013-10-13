"""server.py: entry point for post analyzer server
Post Analyzer is a text processing server. It analyzes a text block (forum post - for example) and it returns a JSON
document with its analysis.  The analysis can be used to determine key phrases and whether the post contains
colloquialisms (bad words or the use of slang).  The underlying text processing engine correct misspellings and expands
net slang to full phrases during its analysis.

Copyright (c) 2013, Carlos Justiniano
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = ('Carlos Justiniano (carlos.justiniano@gmail.com)',)

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httputil
import json
from textana.textana import ProcessText


class BaseHandler(tornado.web.RequestHandler):
    """Base Handler to handle JSON as data format for API
    """

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.data_json = {}

    def prepare(self):
        """prepare data.json as converted python dict"""
        try:
            self.data_json = tornado.web.escape.json_decode(self.request.body)
        except:
            self.data_json = {}
            self.send_response({
                "success": "failure",
                "reason": "invalid JSON"
            })
            self.flush()

    def send_response(self, response):
        """output a response in JSON form
            Args: response: dictionary
        """
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response))


class RootHandler(tornado.web.RequestHandler):
    """Handle GET request to /"""
    def get(self):
        self.write("Post Analyzer ver. 1.0")


class FullScanAPIHandler(BaseHandler):
    """FullScanAPIHandler processing text sent via /api/fullscan
    """
    def post(self):
        """handles post request"""
        print self.data_json
        text = self.data_json["text"]

        pt = ProcessText()
        res = {
            "status": "success",
            "result": pt.process_text(text)
        }
        self.send_response(res)


application = tornado.web.Application([
    (r"/", RootHandler),
    (r"/api/fullscan", FullScanAPIHandler),
])

if __name__ == "__main__":
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
