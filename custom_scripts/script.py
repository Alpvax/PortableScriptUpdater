class Script():
    def __init__(self, key):
        self.key = key
        self.getVersion = platformVersion
        
    def setVersionFunc(self, getVersion):
        if callable(getVersion):
            self.getVersion = getVersion
        return self
        
    def setLatest(self, versions):
        self.latestVersions = versions
        
    def getCompatibleVersions(self):
        return self.latestVersions
        
    def getCurrentVersion(self):
        data = getCurrentData()
        
    def __str__(self):
        return self.__class__.__name__ + ": " + self.key

def platformVersion(allVersions):
    if not system_platform:
        from platform import system as system_platform
    osName = platform.system()
    if osName in allVersions: #Check script has a version for this OS
        return allVersions[osName]
    else:
        return None
        
def namedVersions(allVersions, names):
    return getJSONChildren(allVersions, *names(allVersions))
        
def getJSONChildren(json, *children):
    out = {}
    for child in children:
        if child in json:
            out[child] = json[child]
    return out if len(out) > 0 else None