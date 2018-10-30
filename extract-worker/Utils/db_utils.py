import os
"""
assign list of pdf(s) files extracted from zip to mongodb
"""
def register_pdf__to_db(uuid, path, mongo):
    buckets = mongo.db.buckets
    bucket = buckets.find_one({"_id": uuid})
    for file in os.listdir(path):
        bucket["pdfs"].append(file)
    buckets.save(bucket)

def get_pdfs_list(uuid, mongo):
    buckets = mongo.db.buckets
    bucket = buckets.find_one({"_id": uuid})
    print(bucket)
    return bucket["pdfs"]
