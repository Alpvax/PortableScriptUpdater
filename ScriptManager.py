import requests, json, os
from custom_scripts import *
from custom_scripts import Script

DATA_PATH = os.path.expanduser(os.path.join("~", ".alpUpdater", "scripts.conf"))

def getScript(key):
    if key == None:
        raise TypeError("Cannot find or create a Script with no key")
    try:
        script = eval(key)
    except NameError as e:
        if str(e) == "name '" + key + "' is not defined":
            script = Script(key)
            exec("global {0}\n{0} = script".format(key))
    return script
        
        
def loadCurrentData(datapath=DATA_PATH):
    for key, currentData in readCurrentData().items():
        getScript(key).setCurrentVersion(currentData)
    
def readCurrentData(datapath=DATA_PATH):
    userData = {}
    if os.path.isfile(datapath):
        with open(datapath, 'r') as file:
            userData = json.load(file)
    return userData
    
def writeCurrentData(data, datapath=DATA_PATH):
    directory = os.path.dirname(datapath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(datapath, 'w') as file:
        json.dump(out, file, indent="\t", sort_keys=True)
    
def loadLatestData(url):
    data = json.loads(requests.get(url).text)
    updateLatest(data)
    
def updateLatest(data):
    for key, allVersions in data.items():
        script = getScript(key)
        s_vers = script.getVersion(allVersions)
        if s_vers:
            script.setLatest(s_vers)
            
def _allScripts():
    return [script for key, script in globals().items() if isinstance(script, Script)]
        
#def updateLatest(data, script=None, key=None):
#    if (not script) and key:
#        script = getScript(key)
#    if script and script.key in data:
#        _updateScriptVer(script, data[script.key])
#    else:
#        for key, allVersions in data.items():
#            _updateScriptVer(allVersions, scriptKey=key)
#def _updateScriptVer(script, allVersions):
#    s_vers = script.getVersion(allVersions)
#    if s_vers:
#        script.setLatest(s_vers)
    
def simpleMain():
    #updateLatest({"AHKAutorun": {"script": {"path": "AutoHotkey/autorun.ahk", "version": 1}, "binary": {"path": "AutoHotkey/binaries/autorun.exe", "version": 1}}})
    print(AHKAutorun.getCompatibleVersions())
    
if __name__ == "__main__":
    loadLatestData("https://raw.githubusercontent.com/Alpvax/PortableScriptUpdater/master/scripts.json")
    loadCurrentData()
    simpleMain()
    print([str(s) for s in _allScripts()])