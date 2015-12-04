import requests, json, platform, os, regex
from tkinter import *
from tkinter.ttk import *

class GuiWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.resizable(True, False)
        self.frames = 0
    
    def add(self, frame):
        self.frames += 1
        frame.grid(sticky="nwe")
        self.rowconfigure(self.frames, weight=1)
        self.columnconfigure(0, weight=1)
        
    def display(self):
        if self.frames > 0:
            Button(self, text="done").grid(sticky="s")
            self.mainloop()

class GuiUpdate(Labelframe):
    def __init__(self, master, scriptName, script, current=None):
        Labelframe.__init__(self, master, text=scriptName)
        self.key = scriptName
        self.versions = script
        self.setupVars()
        master.add(self)
        self.createWidgets()
        
    def setupVars(self):
        self.versionVar = IntVar()
        self.typeVar = StringVar()
        self.updateVar = IntVar()
        if self.versions:
            self.versionVar.set(self.versions.get("versions", 1))
        
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
    root = GuiWindow()
    for key, scripts in json.loads(r.text).items():
        if osName in scripts: #Check script has a version for this OS
            script = scripts[osName]
            print(script)
            if key in userData:
                print(userData[key])
            else:
                f = GuiUpdate(root, key, script)
    root.display()