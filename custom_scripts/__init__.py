from os import listdir
from os.path import join as joinPath
from os.path import splitext
from os.path import isdir
from os.path import isfile
from os.path import basename
from os.path import dirname

from .script import Script, namedVersions
    
def getExclusions():
    excluded = ["__init__.py", "script.py", "__pycache__"]
    if isfile("excluded_modules.conf"):
        with open("excluded_modules.conf", "r") as file:
            excluded += [line for line in file if len(line) > 0]
    return excluded
    
all_mod_list = [splitext(f)[0] for f in listdir(dirname(__file__)) if f not in getExclusions() and (splitext(f)[1] == ".py" or (isdir(f) and isfile(joinPath(f, "__init__.py"))))]
__all__ = []
for modName in all_mod_list:
    exec("from . import {0} as module_{0}".format(modName))
    module = eval("module_" + modName)
    
    try:    #Create Script
        exec("{0} = module.getScript(\"{0}\")".format(modName))
    except AttributeError:
        exec("{0} = Script(\"{0}\")".format(modName))
    __all__.append(modName)
    script = eval(modName)
    
    #Set script.getVersion if available, else default (platform.system())
    if callable(getattr(module, 'getCompatibleVersions', None)):
        script.setVersionFunc(module.getCompatibleVersions)
    elif callable(getattr(module, 'getCompatibleVersionNames', None)):
        script.setVersionFunc(lambda allVersions, names=module.getCompatibleVersionNames: namedVersions(allVersions, names))

def numScripts():
    return len(__all__)