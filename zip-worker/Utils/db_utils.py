import os

def get_pdfs_num(uuid, mongo):
    buckets = mongo.db.buckets
    bucket = buckets.find_one({"_id": uuid})
    return len(bucket["pdfs"])

def get_txts_num(uuid, mongo):
    buckets = mongo.db.buckets
    bucket = buckets.find_one({"_id": uuid})
    return len(bucket["txts"])

def get_txts_list(uuid, mongo):
    buckets = mongo.db.buckets
    bucket = buckets.find_one({"_id": uuid})
    return bucket["txts"]

def get_zip_name(uuid, mongo):
    buckets = buckets = mongo.db.buckets
    bucket = buckets.find_one({"_id": uuid})
    return bucket["zip_name"]

