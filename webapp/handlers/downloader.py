import tornado
import requests
import os
from utils.downloadutil import DownloadUtil

class DownloadHandler(tornado.web.RequestHandler):
    def initialize(self, minioClient):
        self.set_header("Content-Type", 'application/json')
        self.DownloadUtill = DownloadUtil(minioClient)

    def get(self, *args, **kwargs):
        try:
            uuid = tornado.escape.to_unicode(self.request.arguments['uuid'][0])
        except KeyError:
            self.write("uuid is not in the url")
            self.set_status(400)
            self.finish()
            return
        data = self.DownloadUtill.download(uuid)
        if data:
            self.set_header('Content-Type', 'application/x-tar')
            self.set_header(
                'Content-Disposition', f"attachment; filename={uuid}.tar.gz")
            with open(f"{uuid}.tar.gz", 'wb') as file:
                for d in data.stream(32*1024):
                    self.write(d)
                    self.flush()
            self.set_status(200)
        else:
            self.write(tornado.escape.json_encode({"status":"not found", "message": "data not found on minio"}))
            self.set_status(404)
        self.finish()

