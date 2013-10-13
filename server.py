"""server.py: entry point for post analyzer server
"""

__author__ = ('Carlos Justiniano (carlos.justiniano@gmail.com)',)

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httputil
import json
import string
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
