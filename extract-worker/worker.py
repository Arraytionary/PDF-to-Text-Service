#!/usr/bin/env python3
import os
import logging
import json
import uuid
import redis
import requests
from pymongo import MongoClient
from Utils.tar_utils import unzip
from Utils.db_utils import register_pdf__to_db
from Utils.task_utils import send_job




#TODO link it to docker compose instead
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
QUEUE_NAME = 'zip_queue'

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
    # get file info
    uuid = task.get("uuid")
    zip_name = task.get("zip_name")

    # assign path
    path = f"./f{uuid}/"

    # extract file
    extract(uuid, zip_name, path)

    # upload extracted file to minio
    upload(uuid, f"{path}pdfs")

    # assign file to mogodb
    register_pdf__to_db(uuid, f"{path}pdfs", mongo)

    # send job to queue
    send_job(uuid)

def extract(uuid, file_name, path):
    # retrieve file from minio
    try:
    data = minioClient.get_object(uuid, file_name)
    with open(path + file_name, 'wb') as file_data:
        for d in data.stream(32*1024):
            file_data.write(d)
    except ResponseError as err:
        log.info(err)
    
    
    # extract
    unzip(f"p{path}pdfs", f"{path}{file_name}")


# upload file to minio
def upload(uuid, path):
    for file in os.listdir(path):
        try:
            with open(file, 'rb') as file_data:
                file_stat = os.stat(file)
                print(minioClient.put_object(uuid, file,
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
