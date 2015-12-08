# PortableScriptUpdater
Repository used for version control of various scripts (ahk, python etc)

The current latest versions are stored/retrieved from scripts.json, the latest versions will be read from there.

#Setting up script versions
Settings are taken from /custom_scripts/<script_key>.py
Define the method "getScript(scriptKey)" to use your own implementation of the custom_scripts.script.Script class.

Define the method "getCompatibleVersions(allVersions)" and return a json object composing all of the versions applicable to the current system.
Alternatively, define the method "getCompatibleVersionNames(allVersions)" and return a list of the json version keys applicable to the current system.

If neither of the getCompatibleVersion methods are defined, it will default to using platform.system() as the singular version key.