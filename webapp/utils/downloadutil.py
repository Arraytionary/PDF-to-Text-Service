from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists, NoSuchBucket)
class DownloadUtil:
    def __init__(self, minio):
        self.minio = minio
    def download(self, uuid):
        try:
            data = self.minio.get_object(uuid, f"{uuid}.tar.gz")
        except NoSuchBucket as err:
            return None
        return data