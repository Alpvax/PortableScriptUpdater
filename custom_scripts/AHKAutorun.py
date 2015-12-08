from platform import system

def getCompatibleVersionNames(allVersions):
    "Return a list of keys to return the versions for. Never used if 'getCompatibleVersions' is defined"
    return None if system() != "Windows" else ["script", "binary"]