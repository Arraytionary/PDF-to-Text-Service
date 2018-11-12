from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
class DownloadUtil:
    def __int__(self, minio):
        self.mino = minio
    def download(uuid):
        try:
            data = minio.get_object(uuid, f"{uuid}.tar.gz")
        except ResponseError as err:
            return None
        return data