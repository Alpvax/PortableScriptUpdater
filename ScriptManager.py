import requests, json, os

DATA_PATH = os.path.expanduser(os.path.join("~", ".alpUpdater", "scripts.conf"))


def getScriptVersion(key, currentData=None):
    print(eval(key).getVersion(currentData))
    #try:
        #print(eval(key).getScript())
    #except 
    
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
        script = eval(key)
        s_vers = script.getVersion(allVersions)
        if s_vers:
            script.setLatest(s_vers)
    
    
def simpleMain():
    updateLatest({"AHKAutorun": {"script": {"path": "AutoHotkey/autorun.ahk", "version": 1}, "binary": {"path": "AutoHotkey/binaries/autorun.exe", "version": 1}}})
    print(AHKAutorun.getCompatibleVersions())
    #getScriptVersion("mod1", {"Windows": {"script": {"path": "AutoHotkey/autorun.ahk", "version": 1}, "binary": {"path": "AutoHotkey/binaries/autorun.exe", "version": 1}}})
    
if __name__ == "__main__":
    thisDir = None #Declare so it isn't listed as a difference
    thisDir = dir()
    from custom_scripts import *
    print([f for f in dir() if f not in thisDir])
    simpleMain()