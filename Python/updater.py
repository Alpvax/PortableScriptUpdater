import requests

if __Name__ == "__main__":
    r = requests.get("https://raw.github.com/Alpvax/PortableScriptUpdater/scripts.json")
    print(r.text)#XXX