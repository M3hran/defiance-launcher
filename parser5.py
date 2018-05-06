import os
import re
import win32api, json

rs=[]
steamfolder="steamapp"
gamefolder="Sid Meier's Civilization V"
default="C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization V"

def find_existing(type):
    data = json.load(open("resources.json"))
    statedata = json.load(open("state.json"))
    obj=type+"s"
    if type == "mod":
        folder="\\Assets\\DLC"
    if type == "map":
        folder="\\Assets\\Maps"
        print("here")
        for a in data[obj]:
            rex = re.compile(a["name"])
            for root,dirs,files in os.walk(statedata["path"]+folder):
                for d in dirs:
                    result = rex.search(d)
                    if result:
                        return a["name"]

def search_drives(path):
    rex = re.compile(path)
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        for root,dirs,files in os.walk(drive):
            for d in dirs:
                result = rex.search(d)
                if result:
                    if root.endswith('\\'):
                        path = root+d
                    else:
                        path = "\\".join((root,d))
                    rs.append(path)
    return rs

def find_path(possible_path,path):
    rex = re.compile(path)
    for root,dirs,files in os.walk(possible_path):
        for d in dirs:
              result = rex.search(d)
              if result:
                if root.endswith('\\'):
                    path = root+d
                else:
                    path = "\\".join((root,d))
    return path

def find_installation():
    print("Searching for game path...")

    if os.path.exists(default+"\\CivilizationV.exe"):
        return default

    steamapp=search_drives(steamfolder)

    if steamapp:
        for i in steamapp:
            civpath=find_path(i,gamefolder)
            if civpath:
                if os.listdir(civpath)==[]:
                    print("found empty folder at: "+civpath)
                    continue
                else:
                    #print(civpath)
                    path=civpath
                    break
            else:
                print("Civ installation folder not found!")
                return -1
    else:
        print("steamapp folder not found!")
        return -1
    return path



