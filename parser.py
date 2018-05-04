import os
import re
import win32api

rs=[]
steamfolder="steamapp"
gamefolder="Sid Meier's Civilization V"

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
    else:
        print("steamapp folder not found!")
    return path



