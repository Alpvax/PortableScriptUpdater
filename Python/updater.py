import requests, json, os
from platform import system

if __name__ == "__main__":
    platform = system()
    datapath = os.path.expanduser("~/.alpUpdater")
    userData = {}
    if os.path.isfile(datapath):
        with open(datapath, 'r') as file:
            userData = json.load(file)
    print(userData)
    r = requests.get("https://raw.githubusercontent.com/Alpvax/PortableScriptUpdater/master/scripts.json")
    for key, script in json.loads(r.text).items():
        if script[platform]: #Check script has a version for this OS
            print(script[platform])