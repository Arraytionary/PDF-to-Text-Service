import tornado
import requests
from utils.uploadutil import UploadUtill
HOST = os.getenv("MINIO_HOST", "localhost")

class UploaderHandler(tornado.web.RequestHandler):
    def initialize(self, minioClient):
        self.UploadUtill = UploadUtill(minioClient)

    def put(self,*args, **kwargs):
        data = self.request.body
        bucket_name = self.UploadUtill.addfile(data)
        self.set_header("Content-Type", 'application/json')
        print("bucket_name(uuid):", bucket_name)
        if bucket_name:
            resjson = tornado.escape.json_encode({"status": 200, "message": "ok", "uuid": bucket_name})
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(200)

            requests.post(f"{HOST}:5000/createtext", data=resjson)
            
        else:
            resjson = {"status": 504, "message": "upload failed"}
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(504)
        self.finish()



