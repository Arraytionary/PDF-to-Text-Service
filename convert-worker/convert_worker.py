#!/usr/bin/env python3
import os
import logging
import json
import uuid
import redis
import requests
from pymongo import MongoClient

from minio import Minio
from minio.error import ResponseError
MINIO_HOST = os.getenv("MINIO_HOST", "localhost")

minioClient = Minio(f'{MINIO_HOST}:9000',
                  access_key='admin',
                  secret_key='password',
                  secure=False)

client = MongoClient('mongodb://mongo:27017/')
mongo = client.mango


LOG = logging
REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
QUEUE_NAME = 'convert_queue'

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
    pdf = task.get("file_name")
    download(uuid, pdf, "./")
    convert(pdf)
    upload(uuid, f"./{pdf[:-3]}txt")
    register_text__to_db(uuid, f"./{pdf[:-3]}txt")
    delete_all(pdf[:-3])

def download(uuid, file_name, path):
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

def upload(uuid, file_name):
    try:
        with open(file_name, 'rb') as file_data:
            file_stat = os.stat(file_name)
            print(minioClient.put_object(uuid, file_name[2:],
                                file_data, file_stat.st_size))
    except ResponseError as err:
        LOG.info(err)

def register_text__to_db(uuid, file):
    buckets = mongo.db.buckets
    bucket = buckets.find_one({"_id": uuid})
    bucket["txts"].append(file[2:])
    buckets.save(bucket)

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
