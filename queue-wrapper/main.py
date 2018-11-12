import os
import json
import redis
import requests
from flask import Flask, jsonify, request
from pymongo import MongoClient
import pymongo
from flask_cors import CORS, cross_origin
HOST = os.getenv("WEB_HOST", "localhost")
# PORT = os.getenv("SOS_PORT", 8000)    
BASE_URL = f"http://{HOST}:5555/progress/update"

app = Flask(__name__)
CORS(app, support_credentials=True)

client = MongoClient('mongodb://mongo:27017/')
mongo = client.mango

class RedisResource:
    REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
    QUEUE_NAME = 'zip_queue'

    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    conn = redis.Redis(host=host, *port)

@app.route('/createtxt', methods = ['POST'])
def send_job():
    body = request.json
    # print(body)s
    #zip file name
    file_name = body["file"]

    # user that request the task
    uuid = body["uuid"]

    # add information to database
    if not assign_db(uuid, file_name):
        return jsonify({'status': 'UUID already exist'}),400
    
    #issue socket that job has been accepted
    requests.post(f"{BASE_URL}?uuid={uuid}", json={"message":"Job accepted"})

    # push json to extract queue
    json_packed = json.dumps({"uuid": uuid, "zip_name": file_name})
    RedisResource.conn.rpush(
        RedisResource.QUEUE_NAME,
        json_packed)

    return jsonify({'status': 'OK'})

def assign_db(uuid, file_name):
    buckets = mongo.db.buckets
    try:
        buckets.insert_one({'_id': uuid, 'zip_name': file_name, 'pdfs':[], 'txts':[]})
        return True
    except pymongo.errors.DuplicateKeyError:
        return False
