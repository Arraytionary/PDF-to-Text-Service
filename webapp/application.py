import os
import logging as LOG
import tornado.ioloop as ioloop
import tornado.web
from minio import Minio
from handlers.progress import ProgressSocketHandler
from handlers.uploader import UploaderHandler
from handlers.progress import UpdateProgress
from handlers.downloader import DownloadHandler

HOST = os.getenv("MINIO_HOST", "localhost")

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    LOG.info("starting web controller server at port 5555 ... ")
    LOG.info("connecting to minio at port 9000...")

    minioClient = Minio(f'{HOST}:9000',
                        access_key='admin',
                        secret_key='password',
                        secure=False
                        )
    app = tornado.web.Application(
        [
            (r"/progress/socket", ProgressSocketHandler),
            (r"/progress/update", UpdateProgress),
            (r"/upload", UploaderHandler, dict(minioClient=minioClient)),
            (r"/download", DownloadHandler, dict(minioClient=minioClient)),
        ],
        debug=True,
    )
    app.listen(5555)
    tornado.ioloop.IOLoop.current().start()
