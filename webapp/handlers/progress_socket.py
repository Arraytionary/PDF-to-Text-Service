import tornado.web
import tornado.escape
import tornado.websocket

clients = dict()
class UpdateProgress(tornado.web.RequestHandler):
    def initialize(self):
        self.uuid = tornado.escape.to_unicode(self.request.arguments['uuid'][0])
    def post(self, *args, **kwargs):
         pass
class ProgressSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.uuid = tornado.escape.to_unicode(self.request.arguments['uuid'][0])
        self.client = clients[self.uuid]
        print("uuid: ", self.uuid)
        self.write_message("Starting Converting ...")

    def on_message(self, message):
        #client should not send anything to the server...
        self.write_message("fuck")

    def on_close(self):
        self.write_message("DONE ...")


