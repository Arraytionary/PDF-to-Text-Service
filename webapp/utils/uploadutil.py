import logging as LOG
import io
import uuid
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
class UploadUtill:
    def __init__(self, minio):
        self.minio = minio
    def _create_bucket(self):
        """ create bucket on minio"""
        bucket_name = str(uuid.uuid4())
        LOG.info(bucket_name)
        try:
            self.minio.make_bucket(bucket_name, location="us-east-1")
        except BucketAlreadyOwnedByYou as err:
            pass
        except BucketAlreadyExists as err:
            pass
            # return self.create_bucket()
        except ResponseError as err:
            raise
        return bucket_name #uuid

    def addfile(self, data):
        bucket_name = self._create_bucket()
        """ add tgs file to minio """
        obj_name = f"{bucket_name}.tgz"
        file = io.BytesIO(data)
        try:
            print(self.minio.put_object(
                bucket_name,
                obj_name,
                file,
                len(data)
            ))
            return bucket_name
        except ResponseError as err:
            print(err)
            return None
