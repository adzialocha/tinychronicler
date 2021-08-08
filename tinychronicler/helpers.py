import os
import shutil
import tempfile
from contextlib import contextmanager


@contextmanager
def temporary_file(file_ext: str):
    tmp_dir = tempfile.mkdtemp()
    yield os.path.join(tmp_dir, "out{}".format(file_ext))
    shutil.rmtree(tmp_dir)
