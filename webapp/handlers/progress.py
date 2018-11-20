import tornado.web
import tornado.escape
import tornado.websocket

clients = dict()

class UpdateProgress(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, PUT')

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()
    def initialize(self):
        self.set_header("Content-Type", 'application/json')
        try:
            self.uuid = tornado.escape.to_unicode(self.request.arguments['uuid'][0])
            self.client = clients[self.uuid]
        except KeyError:
            self.set_status(404)
            self.write(tornado.escape.json_encode({"status": 404, "message": 'uuid does not exist'}))

    def post(self, *args, **kwargs): # expect uuid in url, and message in body.
        if 'complete' in self.request.arguments.keys():
            #Todo: implemnet 
            # 1. generate url for down loade file form minio
            pass
        else:
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
        if self.uuid not in clients.keys():
            clients[self.uuid] = self
            self.messages = []
            # self.write_message("uuid: " + self.uuid)
            self.write_message("Starting Converting ...")
        else:
            self.write_message(clients[self.uuid].messages[-1]) 

    def on_message(self, message):
        # client should not send anything to the server...
        pass
        
    def on_close(self):
        self.write_message("connnectopn close")


