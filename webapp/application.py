import logging as LOG
import tornado.ioloop as ioloop
import tornado.httpserver as httpserver
import tornado.web
import os.path
from minio import Minio
from minio.error import ResponseError
from handlers.progress_socket import ProgressSocketHandler
from handlers.uploader import UploaderHandler

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    LOG.info("starting web controller server at port 5555 ... ")
    LOG.info("connecting to minio at port 9000...")

    minioClient = Minio('127.0.0.1:9000',
                        access_key='admin',
                        secret_key='password',
                        secure=False
                        )
    app = tornado.web.Application(
        [
            (r"/progress", ProgressSocketHandler),
            (r"/uploader", UploaderHandler, dict(minioClient=minioClient)),
        ],
        # cookie_secret="Supanut_BOATTTTTTTTTTTT",
        # xsrf_cookies=True,
        debug=True,
    )
    app.listen(5555)
    tornado.ioloop.IOLoop.current().start()
