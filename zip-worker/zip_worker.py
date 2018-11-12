#!/usr/bin/env python3
import os
import logging
import json
import uuid
import redis
import requests
from pymongo import MongoClient
from Utils.db_utils import *
from Utils.tar_utils import make_tarfile

from minio import Minio
from minio.error import ResponseError

HOST = os.getenv("WEB_HOST", "localhost")
BASE_URL = f"http://{HOST}:5555/progress/update"
MINIO_HOST = os.getenv("MINIO_HOST", "localhost")

minioClient = Minio(f'{MINIO_HOST}:9000',
                  access_key='admin',
                  secret_key='password',
                  secure=False)

client = MongoClient('mongodb://mongo:27017/')
mongo = client.mango


LOG = logging
REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
QUEUE_NAME = 'compress_queue'

INSTANCE_NAME = uuid.uuid4().hex

LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def watch_queue(redis_conn, queue_name, callback_func, timeout=30):
    active = True

    while active:
        # Fetch a json-encoded task using a blocking (left) pop
        packed = redis_conn.blpop([queue_name], timeout=timeout)

        if not packed:
            # if nothing is returned, poll a again
            continue

        _, packed_task = packed

        # If it's treated to a poison pill, quit the loop
        if packed_task == b'DIE':
            active = False
        else:
            task = None
            try:
                task = json.loads(packed_task)
            except Exception:
                LOG.exception('json.loads failed')
            if task:
                callback_func(task)

def execute(log, task):
    log.info(str(task))
    # number = task.get('number')
    uuid = task.get("uuid")
    n_pdfs = get_pdfs_num(uuid, mongo)
    n_txts = get_txts_num(uuid, mongo)
    # Do spin wait until all file being converted
    while n_pdfs != n_txts:
        # TODO tell backend that the progress on converting
        convert_progress = n_txts*100./n_pdfs
        requests.post(f"{BASE_URL}?uuid={uuid}", json={
                      "message": f"converting: {convert_progress}\%"})
        n_txts = get_txts_num(uuid, mongo)
    # done all converted
    # TODO tell backend that the conversion is complete
    requests.post(f"{BASE_URL}?uuid={uuid}", json={
                  "message": "convert complete"})


    path = f"./{uuid}/txt/"
    if not os.path.exists(path):
        os.makedirs(path)
    zip_name = get_zip_name(uuid, mongo)
    download_all_txt(uuid, path)
    # zip all txt file
    requests.post(f"{BASE_URL}?uuid={uuid}", json={"message": "zipping file"})
    if not os.path.exists(f"./{uuid}/zip"):
        os.makedirs(f"./{uuid}/zip")

    make_tarfile(f"../zip/{zip_name}", path[:-1])

    
    upload(uuid, f"./{uuid}/zip/", zip_name)
    # tell backend that file is ready for download
    requests.post(f"{BASE_URL}?uuid={uuid}", json={
                  "message": "file is ready to download"})

def download_all_txt(uuid, path):
    for file_name in get_txts_list(uuid, mongo):
        try:
            data = minioClient.get_object(uuid, file_name)
            with open(path + file_name, 'wb') as file_data:
                for d in data.stream(32*1024):
                    file_data.write(d)
        except ResponseError as err:
            LOG.info(err)

def delete_all(file_name):
    #delete file downloaded from sos
    os.remove(f"./{file_name}pdf")
    # delete file txt after uploaded
    os.remove(f"./{file_name}txt")

def convert(file_name):
     # convert
    os.system(f"pdftotext -layout {file_name}")

def upload(uuid, path, file_name):
    try:
        minioClient.remove_object(uuid, file_name)
    except ResponseError as err:
        log.info(err)
    try:
        with open(path + file_name, 'rb') as file_data:
            file_stat = os.stat(path + file_name)
            print(minioClient.put_object(uuid, file_name,
                                file_data, file_stat.st_size))
    except ResponseError as err:
        log.info(err)

def main():
    LOG.info('Starting a worker...')
    LOG.info('Unique name: %s', INSTANCE_NAME)
    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    named_logging = LOG.getLogger(name=INSTANCE_NAME)
    named_logging.info('Trying to connect to %s [%s]', host, REDIS_QUEUE_LOCATION)
    redis_conn = redis.Redis(host=host, *port)
    watch_queue(
        redis_conn, 
        QUEUE_NAME, 
        lambda task_descr: execute(named_logging, task_descr))

if __name__ == '__main__':
    main()
