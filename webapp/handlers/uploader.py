import tornado
from utils.uploadutil import UploadUtill
class UploaderHandler(tornado.web.RequestHandler):
    def initialize(self, minioClient):
        self.UploadUtill = UploadUtill(minioClient)

    def post(self, *args, **kwargs):
        self.set_header("Content-Type", 'application/json')
        pass

    def put(self,*args, **kwargs):
        data = self.request.body
        bucket_name = self.UploadUtill.addfile(data)
        self.set_header("Content-Type", 'application/json')
        if bucket_name:
            resjson = {"status":200, "message": "ok", "uuid": bucket_name}
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(200)
        else:
            resjson = {"status": 504, "message": "upload failed"}
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(504)
        self.finish()

            
