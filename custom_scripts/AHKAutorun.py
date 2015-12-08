from platform import system

def getCompatibleVersionNames(allVersions):
    return None if system() != "Windows" else ["script", "binary"]