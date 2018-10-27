import logging as LOG
import tornado.ioloop as ioloop
import tornado.httpserver as httpserver
import tornado.web
import os.path
from handlers.progress_socket import ProgressSocketHandler

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
chat_socket = ChatSocketHandler
def main():
    LOG.info("starting web controller server at port 5555 ... ")
    app = tornado.web.Application(
        [
            (r"/progress", chat_socket),
        ],
        xsrf_cookies=True,
        debug=True,
    )
    app.listen(5555)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
