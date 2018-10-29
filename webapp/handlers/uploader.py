import tornado
from tornado.httpclient import AsyncHTTPClient
from utils.uploadutil import UploadUtill

class UploaderHandler(tornado.web.RequestHandler):
    def initialize(self, minioClient):
        self.UploadUtill = UploadUtill(minioClient)

    def put(self,*args, **kwargs):
        data = self.request.body
        bucket_name = self.UploadUtill.addfile(data)
        self.set_header("Content-Type", 'application/json')
        if bucket_name:
            resjson = {"status":200, "message": "ok", "uuid": bucket_name}
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(200)

            api_endpoint = 'localhost:5000/createtxt'
            headers = {'Content-Type': 'application/json'}
            json_data = tornado.escape.json_encode(data)
            response = await tornado.http_client.fetch(api_endpoint,
                                            raise_error=False,
                                            method='POST',
                                            body=json_data,
                                            headers=headers)
        else:
            resjson = {"status": 504, "message": "upload failed"}
            self.write(tornado.escape.json_encode(resjson))
            self.set_status(504)

    
        self.finish()



