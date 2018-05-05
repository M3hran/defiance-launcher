import os, subprocess, shutil
import parser5
from tkinter import *
import tkinter.messagebox
from tkinter import simpledialog
import requests, zipfile, io, tldextract, json
import pygame, threading, re


class myWindow(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        # don't assume that self.parent is a root window.
        # instead, call `winfo_toplevel to get the root window
        self.winfo_toplevel().title("Defiance Launcher  "+ver)

        # this adds something to the frame, otherwise the default
        # size of the window will be very small
        #label = Entry(self)
        #label.pack(side="top", fill="x")

def valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    a = re.match(regex, url)

    if a:
        return True
    else:
        return False

def doesnothing():
    tkinter.messagebox.showwarning("In Development", "Oops, this does nothing at the moment :(")

def ask_url():

    f1=False
    f2=False
    url = simpledialog.askstring("Input", "Note: You may only download zip files\nEnter URL: ")
    #print(url)
    if url != None:
        a=valid_url(url)
        if  a != True:
            tkinter.messagebox.showwarning("Invalid", "Not a valid URL. Please try again.")
            #ask_url()
        else:
            f2=True


        if url != None and f2==True:
            b = url[-4:]
            if b != '.zip':
                tkinter.messagebox.showwarning("Invalid","URL must end with \".zip\"")
                #print(b)
                #ask_url()
            else:
                f1 = True

        if(f1 and f2 == True):
            #print(url)
            return url


def dl_resources(url, asset):

    modName = url.split('/')[-1]
    modName = modName[:-4]
    #print(modName)

    with open("resources.json", "r") as jsonFile:
        data = json.load(jsonFile)

    #print(data)
    a= asset+"s"
    match=False
    for i in data[a]:
        if i["name"] == modName:
            match = True

    if match == False:
        data[a].append({'name':modName,'url':url})
        with open("resources.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    ext = tldextract.extract(url)
    if ext.domain=="dropbox":
        url=url+"?raw=1"

    #download and unpack zip file in mod folder
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    if asset == "map":
        z.extractall("maps/")
    if asset == "mod":
        z.extractall("mods/")

def aboutpage():
    tkinter.messagebox.showinfo("About Defiance-Launcher", "Contribute at https://www.github.com/m3hran/defiance-launcher")

def init_resources():

    #init in a different thread
    def callback1():
        sema.acquire()
        # Ensure resources.json exists otherwise fail.
        if not os.path.isfile("resources.json"):
            tkinter.messagebox.showwarning("Error", "Could not find resources.json file.")
            root.destory()
        # Create folders
        if not os.path.exists("mods"):
            os.makedirs("mods")
        if not os.path.exists("maps"):
            os.makedirs("maps")

        # load resources
        data = json.load(open("resources.json"))

        # Download MODs if necessary
        for mod in data["mods"]:
            if not os.path.exists("mods/"+mod["name"]):
                lock.set("true")
                statusText.set("Downloading " + mod["name"] + " ...")
                dl_resources(mod["url"],"mod")
                print("downloading "+mod["name"])
            lock.set("false")

        # Download Maps if necessary
        for map in data["maps"]:
            if not os.path.exists("maps/"+ map["name"]):
                lock.set("true")
                statusText.set("Downloading " + map["name"] + "...")
                dl_resources(map["url"],"map")
                print("downloading "+map["name"])
            lock.set("false")
        statusText.set("Locating Steamapps...Please wait..")
        if (sema.acquire(blocking=False)):
            statusText.set("Ready.")
        sema.release()

    def callback2():
        sema.acquire()
        statusText.set("Locating Steamapps...Please wait..")
        lock.set("true")
        install_path=parser5.find_installation()
        print("game path found!")
        statusText.set("Steamapps Located...")
        data = { "path": install_path, "mod": "none", "map": "none", "music":"on" }
        with open('state.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        if (sema.acquire(blocking=False)):
            statusText.set("Ready.")
        lock.set("false")
        sema.release()

    sema = threading.BoundedSemaphore(value=2)

    t1 = threading.Thread(target=callback1)
    t1.start()
    if not os.path.isfile("state.json"):
        t2 = threading.Thread(target=callback2)
        t2.start()

def dl_map():
    a = ask_url()
    if a:
        dl_resources(a,"map")
        map_dropdown = []
        mp.children["menu"].delete(0, "end")
        data = json.load(open("resources.json"))
        for map in data["mapss"]:
            map_dropdown.append(map["name"])
            mp.children["menu"].add_command(label=map["name"], command=lambda m=map["name"]: variable2.set(m))
        with open("state.json", "r") as jsonFile:
            statedata = json.load(jsonFile)

        if statedata["map"] == "":
            variable1.set("MAPs")
        else:
            variable1.set(statedata["map"])

def dl_mod():
    a = ask_url()
    if a:
        dl_resources(a,"mod")
        mod_dropdown = []
        md.children["menu"].delete(0, "end")
        data = json.load(open("resources.json"))
        for mod in data["mods"]:
            mod_dropdown.append(mod["name"])
            md.children["menu"].add_command(label=mod["name"], command=lambda m=mod["name"]: variable1.set(m))
        with open("state.json", "r") as jsonFile:
            statedata = json.load(jsonFile)

        if statedata["mod"] == "":
            variable1.set("MODs")
        else:
            variable1.set(statedata["mod"])

def LaunchCiv():
    data = json.load(open("state.json"))
    print(data["path"])
    steampath=data["path"]
    steampath= re.sub('(steamapps).*', '', steampath)
    steampath=steampath+"Steam.exe"
    subprocess.Popen([steampath,"steam://rungameid/8930//%5Cdx11"])
    root.destroy()

def SetAsset(name,type):

    with open("state.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data[type] = name
    print("setting asset "+data[type])
    with open("state.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    if type == 'mod':
        dpath= data["path"] + "\\Assets\\DLC\\" + name
        shutil.copytree("mods\\"+name, dpath)

    if type == 'map':
        dpath= data["path"] + "\\Assets\\Maps\\" + name
        shutil.copytree("maps\\"+name, dpath)


def rmAsset(type):
    with open("state.json", "r") as jsonFile:
        data = json.load(jsonFile)

    if data[type] != "":
        print("removing asset "+data[type])

        modp=data["path"] + "\\Assets\\DLC\\" + data[type] + "\\"
        mapp=data["path"] + "\\Assets\\Maps\\" + data[type] + "\\"

        if type == 'mod':
            if os.path.exists(modp):
                    shutil.rmtree(modp)
        if type == 'map':
            if os.path.exists(mapp):
                    shutil.rmtree(mapp)

        data[type] = ""
        with open("state.json", "w") as jsonFile:
            json.dump(data, jsonFile)

def mod_select(name):
    statusText.set("Modding...Please Wait..")
    data = json.load(open("state.json"))
    if data["mod"] == "":
        SetAsset(name,"mod")
    else:
        rmAsset("mod")
        SetAsset(name,"mod")
    statusText.set("Ready.")

def map_select(name):
    data = json.load(open("state.json"))
    statusText.set("Modding...Please Wait..")
    if data["map"] == "":
        SetAsset(name,"map")
    else:
        rmAsset("map")
        SetAsset(name,"map")
    statusText.set("Ready.")

def removeAll():
    rmAsset("mod")
    variable1.set("MODs")
    rmAsset("map")
    variable2.set("MAPs")

def muteselection():
    with open("state.json", "r") as jsonFile:
        data = json.load(jsonFile)
    if checkCmd.get() == 1:
        pygame.mixer.music.pause()
        print("music off.")
        data["music"] = "off"
    if checkCmd.get() == 0:
        pygame.mixer.music.unpause()
        print("music on.")
        data["music"] = "on"
    with open("state.json", "w") as jsonFile:
        json.dump(data, jsonFile)

def on_enter(event):
    if lock.get() == "false":
        statusText.set("Launch..")

def on_leave(event):
    if lock.get() == "false":
        statusText.set("Ready.")

# ********* Main **********
#music
pygame.init()
pygame.mixer.music.load("baba.mp3")
pygame.mixer.music.play(-1)
ver="0.18.0503"
install_path = ""

root = Tk()
root.iconbitmap(r'launcher_favicon.ico')
root.geometry("%dx%d+%d+%d" % (300, 300, 250, 350))
root.attributes("-alpha", 0.9)
root.configure(bg="#10397c")
root.resizable(width=False, height=False)

window = myWindow(root)
window.pack(side=LEFT)
statusText = StringVar()
statusText.set("Ready.")
lock = StringVar()
lock.set("false")


# ********** Main Menu **********
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Add Mod pack...", command=dl_mod)
subMenu.add_command(label="Add Map pack...", command=dl_map)
subMenu.add_separator()
subMenu.add_command(label="Exit",command=root.destroy)

viewMenu = Menu(menu)
menu.add_cascade(label="View", menu=viewMenu)
viewMenu.add_command(label="View Logs", command=doesnothing)
viewMenu.add_command(label="About...", command=aboutpage)

# ****** Toolbar ********

toolbar = Frame(root, bg="#10397c")
RemoveButt = Button(toolbar, text="Remove All", command=removeAll)
RemoveButt.pack(side=LEFT, padx=2, pady=2)
#AddModButt = Button(toolbar, text=" + Mod ", command=dl_mod)
#AddModButt.pack(side=LEFT, padx=2, pady=2)
#AddMapButt = Button(toolbar, text=" + Map ", command=dl_map)
#AddMapButt.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)
checkCmd = IntVar()

with open("state.json", "r") as jsonFile:
    statedata = json.load(jsonFile)

if statedata["music"] == "on":
    checkCmd.set(0)

if statedata["music"] == "off":
    checkCmd.set(1)

muteselection()
mute= Checkbutton(toolbar, text="Mute", variable=checkCmd, command=muteselection)
mute.pack(side=RIGHT)


# ***** Statusbar *******
status = Label(root, textvariable=statusText, bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

f1= Frame(root, bg="#10397c")
f1.pack(side=TOP, pady=20)
f2= Frame(root, bg="#10397c")
f2.pack(side=TOP, pady=10)
f3= Frame(root, bg="#10397c")
f3.pack(side=BOTTOM)

#load resources


variable1 = StringVar(f1)
variable2 = StringVar(f2)

mod_dropdown=[]
data = json.load(open("resources.json"))

for mod in data["mods"]:
    mod_dropdown.append(mod["name"])

with open("state.json", "r") as jsonFile:
    statedata = json.load(jsonFile)

if statedata["mod"] == "":
    variable1.set("MODs")
else:
    variable1.set(statedata["mod"])
md = OptionMenu(f1, variable1, *mod_dropdown, command=mod_select)
md.pack(side=LEFT, padx=25)

map_dropdown=[]

data = json.load(open("resources.json"))

for map in data["maps"]:
    map_dropdown.append(map["name"])

if statedata["map"] == "":
    variable2.set("MAPs")
else:
    variable2.set(statedata["map"])

mp = OptionMenu(f2, variable2, *map_dropdown, command=map_select)
mp.pack(side=LEFT, padx=25)


LaunchButt = Button(f3, text="Launch", command=LaunchCiv)

#LaunchIcon= PhotoImage(file="defiance_logo.png")
LaunchIcon= PhotoImage(file="launch3.png")
LaunchButt.config(image=LaunchIcon,height=70,width=70)
LaunchButt["bg"] = "white"
LaunchButt[ "border" ] = "3"
LaunchButt.pack(side=LEFT,pady=20)
LaunchButt.bind("<Enter>", on_enter)
LaunchButt.bind("<Leave>", on_leave)

init_resources()
root.mainloop()


