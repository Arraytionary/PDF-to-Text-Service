import tornado.web
import tornado.escape
import tornado.websocket

clients = dict()


class UpdateProgress(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header("Content-Type", 'application/json')
        try:
            self.uuid = tornado.escape.to_unicode(self.request.arguments['uuid'][0])
            self.client = clients[self.uuid]
        except KeyError:
            self.set_status(404)
            self.write(tornado.escape.json_encode({"status": 404, "message": 'uuid does not exist'}))

    def post(self, *args, **kwargs): # expect uuid in url, and message in body.
        body = tornado.escape.json_decode(self.request.body)
        msg = body['message']
        # print(body['message'])
        self.client.messages.append(msg)
        self.client.write_message(msg)
        self.set_status(200)
        self.write(tornado.escape.json_encode({"status": 200, "message": "ok"}))


class ProgressSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.uuid = tornado.escape.to_unicode(self.request.arguments['uuid'][0])
        clients[self.uuid] = self
        self.messages = []
        print("uuid: ", self.uuid)
        self.write_message("Starting Converting ...")

    def on_message(self, message):
        # client should not send anything to the server...
        pass
    def on_close(self):
        self.write_message("DONE ...")


