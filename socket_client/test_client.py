import tornado
import time
import functools

from tornado import escape
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket
from web_socket_interface import WebSocketClient

class TestWebSocketClient(WebSocketClient):

    def _on_message(self, msg):
        print("msg:", msg)
        deadline = time.time() + 1
        ioloop.IOLoop().instance().add_timeout(
            deadline, functools.partial(self.send, str(input())))

    def _on_connection_success(self):
        print('Connected!')
        self.send(str(int(time.time())))

    def _on_connection_close(self):
        print('Connection closed!')

    def _on_connection_error(self, exception):
        print('Connection error: %s', exception)


if __name__ == '__main__':
    client = TestWebSocketClient()
    client.connect('ws://localhost:5555/progress/socket?uuid=ba51f59f-ff29-427e-bf7f-6b1aa2aebb0d')
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        client.close()
