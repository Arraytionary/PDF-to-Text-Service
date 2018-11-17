import tornado
import requests
import os
from utils.uploadutil import UploadUtill
HOST = os.getenv("QUEUE_HOST", "localhost")

class UploaderHandler(tornado.web.RequestHandler):
    def initialize(self, minioClient):
        self.UploadUtill = UploadUtill(minioClient)
        self.args = self.request.arguments.keys()

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT')
    
    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def post(self, *args, **kwargs):# start the process
        if 'uuid' in self.args:
            uuid = tornado.escape.to_unicode(self.request.arguments['uuid'][0])
            json = {
                    'uuid': uuid,
                    'file': f"{uuid}.tar.gz"
                    }
            url = f"http://{HOST}:5000/createtxt"
            print(url)
            r = requests.post(url, json=json)
            self.set_status(r.status_code)
            self.write(f"{url}")
        else:
            self.set_status(400)
            self.write("no uuid in the url")

    def put(self,*args, **kwargs):
        data = self.request.body
        bucket_name = self.UploadUtill.addfile(data)
        self.set_header("Content-Type", 'application/json')
        # print("bucket_name(uuid):", bucket_name)
        if bucket_name:
            resjson = tornado.escape.json_encode(
                {'status': 200, 
                'message': 'ok', 
                'uuid': bucket_name,
                'file': f"{bucket_name}.tar.gz"
                }
                )
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(200)
            
        else:
            resjson = {"status": 400, "message": "upload failed"}
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(400)
        self.finish()



