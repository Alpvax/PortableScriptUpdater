import requests, json, platform, os, regex
from tkinter import *
from tkinter.ttk import *

root = Tk()
frameCount = 0

class GuiUpdate(Labelframe):
    def __init__(self, scriptName, script, current=None):
        global root, frameCount
        Labelframe.__init__(self, root, text=scriptName)
        self.key = scriptName
        self.versions = script
        self.setupVars()
        self.grid(sticky="nwe")
        root.rowconfigure(frameCount, weight=1)
        root.columnconfigure(0, weight=1)
        frameCount += 1
        self.createWidgets()
        
    def setupVars(self):
        self.versionVar = IntVar()
        self.typeVar = StringVar()
        self.updateVar = IntVar()
        if self.versions:
            self.versionVar.set(self.versions.get("version", 1))
        
    def createWidgets(self):
        i = 0
        for version in self.versions:
            Radiobutton(self, text=version, variable=self.typeVar, value=version).grid(column=0, row = i, sticky="w")
            self.columnconfigure(i, weight=1)
            i += 1
        #Label(self, text=self.key).pack(side=LEFT)

if __name__ == "__main__":
    datapath = os.path.expanduser("~/.alpUpdater/scripts.conf")
    userData = {}
    if os.path.isfile(datapath):
        with open(datapath, 'r') as file:
            userData = json.load(file)
    r = requests.get("https://raw.githubusercontent.com/Alpvax/PortableScriptUpdater/master/scripts.json")
    osName = platform.system()
    for key, scripts in json.loads(r.text).items():
        if osName in scripts: #Check script has a version for this OS
            script = scripts[osName]
            print(script)
            if key in userData:
                print(userData[key])
            else:
                f = GuiUpdate(key, script)
                print(root)
    if frameCount > 0:
        Button(root, text="done").grid(sticky="s")
        root.mainloop()