import tarfile
import os
import logging

LOG = logging
LOG.basicConfig(
    level=LOG.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def make_tarfile(output_filename, source_dir):
    os.chdir(source_dir)
    with tarfile.open(output_filename, "w:gz") as tar:
        for file in os.listdir():
                LOG.info(file)
                tar.add("./" + file, arcname=os.path.basename(file))
    os.chdir("../../")
