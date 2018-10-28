import tarfile

def unzip(path, tar_name):
    if (tar_name.endswith("tar.gz")):
        tar = tarfile.open(tar_name, "r:gz")
        tar.extractall(path)
        tar.close()