import tarfile
import os

def make_tarfile(output_filename, source_dir):
    os.chdir(source_dir)
    for file in os.listdir():
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add("./" + file, arcname=os.path.basename(file))
    os.chdir("../../")