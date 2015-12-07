from os import listdir
from os.path import join as joinPath
from os.path import splitext
from os.path import isdir
from os.path import isfile
from os.path import basename
from os.path import dirname

__all__ = [splitext(f)[0] for f in listdir(dirname(__file__)) if f not in ("__init__.py", "__pycache__") and (splitext(f)[1] == ".py" or (isdir(f) and isfile(joinPath(f, "__init__.py"))))]

def numScripts():
    return len(__all__)
