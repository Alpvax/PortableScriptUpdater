import requests, json, platform, os, regex
from tkinter import *
from tkinter.ttk import *

class GuiWindow(Tk):
    def __init__(self, submitCallback=None):
        Tk.__init__(self)
        self.resizable(True, False)
        self.frames = {}
        self.callback = submitCallback
    
    def add(self, frame):
        self.frames[frame.key] = frame
        frame.grid()#sticky="nwe")
        self.rowconfigure(len(self.frames), weight=1, pad=0)
        self.columnconfigure(0, weight=1, pad=10)
        
    def display(self):
        if len(self.frames) > 0:
            Button(self, text="done", command=self.submit).grid(sticky="ns")
            self.mainloop()
    
    def submit(self):
        out = {}
        for key, frame in self.frames.items():
            out[key] = frame.submit()
        if self.callback:
            self.callback(out)
        self.destroy()

class GuiUpdate(Labelframe):
    def __init__(self, master, scriptName, script, current=None):
        Labelframe.__init__(self, master, text=scriptName)
        self.key = scriptName
        self.versions = script
        self.current = current or {}
        master.add(self)
        self.createWidgets()
        
    def createWidgets(self):
        self.versionVars = {}
        i = 0
        for version in self.versions:
            Label(self, text=version).grid(column=0, row = i, sticky="w")
            self.versionVars[version] = StringVar()
            self.versionVars[version].set("Auto-update")
            Combobox(self, textvariable=self.versionVars[version], values=["Auto-update", "Ask First", "Single installation", "Do not install"], state="readonly").grid(column=1, row = i, sticky="w")
            currentVer = self.current.get(version, None)
            Label(self, text=("Currently version: " + str(currentVer.get("current version", "Error!"))) if currentVer else "Not currently installed").grid(column=2, row = i, sticky="w")
            Label(self, text="Latest version: " + str(self.versions[version].get("version", "ERROR!"))).grid(column=3, row = i, sticky="w")
            self.rowconfigure(i, weight=1)
            i += 1
        for j in range(3):
            self.columnconfigure(j, weight=1, pad=5)
            
    def submit(self):
        out = {}
        for version in self.versions:
            print("{key}.{ver}: {process}.".format(key=self.key, ver=version, process=self.versionVars[version].get()))
            out[version] = {"current version": self.versions[version].get("version", -1), "update mode": self.versionVars[version].get()}
        return out
    
def updateUserData(datapath, out):
    print(out)
    directory = os.path.dirname(datapath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(datapath, 'w+') as file:
        json.dump(out, file, indent="\t", sort_keys=True)

if __name__ == "__main__":
    datapath = os.path.expanduser("~/.alpUpdater/scripts.conf")
    userData = {}
    if os.path.isfile(datapath):
        with open(datapath, 'r') as file:
            userData = json.load(file)
    r = requests.get("https://raw.githubusercontent.com/Alpvax/PortableScriptUpdater/master/scripts.json")
    osName = platform.system()
    root = GuiWindow(lambda out: updateUserData(datapath, out))
    for key, scripts in json.loads(r.text).items():
        if osName in scripts: #Check script has a version for this OS
            script = scripts[osName]
            GuiUpdate(root, key, script, userData.get(key, None))
    root.display()