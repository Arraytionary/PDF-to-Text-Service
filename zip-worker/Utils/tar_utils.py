
import os
import tarfile
def tardir(uuid, path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for file in os.listdir(path):
            tar_handle.add(os.path.join(f"./{uuid}/zip", file))
# tardir('./', 'sample.tar.gz') run this script to zip file
# tar.close()