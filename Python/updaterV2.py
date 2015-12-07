import requests, json, platform, os, argparse
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
    
def readData(datapath):
    userData = {}
    if os.path.isfile(datapath):
        with open(datapath, 'r') as file:
            userData = json.load(file)
    return userData
    
def updateUserData(datapath, out, current=None):
    current = out
    directory = os.path.dirname(datapath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(datapath, 'w+') as file:
        json.dump(out, file, indent="\t", sort_keys=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check scripts for updates and update them if requested")
    subparsers = parser.add_subparsers(title="commands")
    
    p_gui = subparsers.add_parser("gui", help="Open GUI version of program")
    p_gui.set_defaults(which="gui")
    
    p_update = subparsers.add_parser("update", help="Download and update any scripts that require it")
    p_update.set_defaults(which="update")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--no-prompt-deny", help="Don't prompt for and don't install updates which require acceptance", action="store_true")
    group.add_argument("-y", "--no-prompt-accept", help="Don't prompt for and install updates which require acceptance", action="store_true")
    p_update.add_argument("-f", "--force-update", help="Update or re-install scripts", action="store_true")
    p_update.add_argument("-s", "--scripts", help="Scripts to install", nargs="+")
    
    p_update = subparsers.add_parser("install", help="Install new modules")
    p_update.set_defaults(which="install")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--no-prompt-deny", help="Don't prompt for and don't install updates which require acceptance", action="store_true")
    group.add_argument("-y", "--no-prompt-accept", help="Don't prompt for and install updates which require acceptance", action="store_true")
    p_update.add_argument("-f", "--force-update", help="Update or re-install scripts", action="store_true")
    p_update.add_argument("-s", "--scripts", help="Scripts to install", nargs="+")
    
    #parser.add_argument("-g", "--gui", help="Open GUI version of program", action="store_true")
    #parser.add_argument("-u", "--update", help="Download and update any scripts that require it, as per settings", action="store_true")
    #parser.add_argument("-q", "--quiet", help="Don't prompt for updates which require acceptance", nargs='?', choices=["Y","N","Yes","No"], const=False)
    #parser.add_argument("-y", "--accept", help="Accept all upgrades without prompting", action="store_true")
    args = vars(parser.parse_args())
    print(args)
    if args["which"] == "gui":
        root = GuiWindow(lambda out: updateUserData(datapath, out, userData))
    #datapath = os.path.expanduser("~/.alpUpdater/scripts.conf")
    #userData = readData(datapath)
    #r = requests.get("https://raw.githubusercontent.com/Alpvax/PortableScriptUpdater/master/scripts.json")
    #osName = platform.system()
    #root = GuiWindow(lambda out: updateUserData(datapath, out, userData))
    #for key, scripts in json.loads(r.text).items():
    #    if osName in scripts: #Check script has a version for this OS
    #        script = scripts[osName]
    #        GuiUpdate(root, key, script, userData.get(key, None))
    #root.display()