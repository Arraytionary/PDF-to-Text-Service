import os
import json
import redis
import requests
from flask import Flask, jsonify, request
from .db_utils import *
from pymongo import MongoClient


client = MongoClient('mongodb://mongo:27017/')
mongo = client.mango

class RedisResource:
    REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
    QUEUE_C = 'convert_queue'
    QUEUE_Z = 'compress_queue'

    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    conn = redis.Redis(host=host, *port)

def send_job(uuid):
    
    pdfs = get_pdfs_list(uuid, mongo)
    for file in pdfs:
        # push json to convert queue
        if file.split(".")[-1] == "pdf" and file[0] != ".":
            json_packed = json.dumps({"uuid": uuid, "file_name": file})
            RedisResource.conn.rpush(
                RedisResource.QUEUE_C,
                json_packed)
    
    json_packed = json.dumps({"uuid": uuid})
    RedisResource.conn.rpush(
        RedisResource.QUEUE_Z,
        json_packed)
