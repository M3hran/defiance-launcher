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
    #f3=False
    url = simpledialog.askstring("Input", "Note: You may only download zip files\nEnter URL: ")
    #print(url)
    if url != None:
        a=valid_url(url)
        if  a != True:
            tkinter.messagebox.showwarning("Invalid", "Not a valid URL. Please try again.")
        else:
            f2=True


        if url != None and f2==True:
            ext = tldextract.extract(url)
            #ext.domain == "dropbox"
                #url = url + "?raw=1"

            b = url[-4:]
            if b != '.zip' and ext.domain != "dropbox":
                tkinter.messagebox.showwarning("Invalid","URL must end with \".zip\"")
                #print(b)
            if ext.domain == "dropbox":
                if re.search(r'preview=', url, re.IGNORECASE):
                    raise ValueError("You are using dropbox's preivew link, use actual zipfile link!\n\nHint: Right click on zipfile, select \"Copy link address\"")
                if re.search(r'\?dl=0', url, re.IGNORECASE):
                    r = re.compile(r'\?dl=0',re.IGNORECASE)
                    url = r.sub(r'', url)
                b = url[-4:]
                if b == '.zip':
                    url=url+"?dl=1"
                else:
                    raise ValueError("Bad Download URL")

            f1 = True
        if(f1 and f2 == True):
            return url


def dl_resources(url, asset):
    #download and unpack zip file in mod folder
    try:

        statusText.set("Downloading...Please wait..")
        disableLaunch()
        # download from url
        r = requests.get(url)
        # extract filename from url header
        d = r.headers['content-disposition']
        modName = re.findall("filename=(.+)", d)
        modName = ''.join(modName)
        modName = re.findall(r'"([^"]*)"', modName)
        modName = ''.join(modName)
        modName = modName[:-4]
        print("starting unzip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        fname=z.namelist()[0].split("/")[0]
        if asset == "map":
            z.extractall("maps/")
        elif asset == "mod":
            z.extractall("mods/")
        else:
            print("dl asset err")

        # update resources with new asset

        with open("resources.json", "r") as jsonFile:
            data = json.load(jsonFile)
        a = asset + "s"
        match = False
        for i in data[a]:
            if i["name"] == modName:
                match = True

        if match == False:
            data[a].append({'name': modName, 'folderName': fname, 'url': url})
            with open("resources.json", "w") as jsonFile:
                json.dump(data, jsonFile)
    except:
        e = sys.exc_info()[0]
        tkinter.messagebox.showwarning("Error", "Error: %s" % e)
        return "error"


    statusText.set("Ready.")
    enableLaunch()

def dl_map():
    try:
        a = ask_url()
        if a:
            v = dl_resources(a,"map")
            if v != "error":
                map_dropdown = []
                mp.children["menu"].delete(0, "end")
                data = json.load(open("resources.json"))
                for map in data["maps"]:
                    map_dropdown.append(map["name"])
                    mp.children["menu"].add_command(label=map["name"], command=lambda m=map["name"]: map_select(m))

                #setMenu('map')
                with open("state.json", "r") as jsonFile:
                    statedata = json.load(jsonFile)

                if statedata["map"] == "":
                    variable2.set("MAPs")
                else:
                    variable2.set(statedata["map"])
    except ValueError as err:
        tkinter.messagebox.showwarning("Error", err.args)

def dl_mod():
    try:
        a = ask_url()
        if a:
            v = dl_resources(a,"mod")
            if v != "error":

                mod_dropdown = []
                md.children["menu"].delete(0, "end")
                data = json.load(open("resources.json"))
                for mod in data["mods"]:
                    mod_dropdown.append(mod["name"])
                    md.children["menu"].add_command(label=mod["name"], command=lambda m=mod["name"]: mod_select(m))
                #setMenu('mod')

                #with open("state.json", "r") as jsonFile:
                #    statedata = json.load(jsonFile)

                #if statedata["map"] == "":
                #    variable1.set("MAPs")
                #else:
                #    variable1.set(statedata["map"])

    except ValueError as err:
        tkinter.messagebox.showwarning("Error", err.args)

def aboutpage():
    tkinter.messagebox.showinfo("About Defiance-Launcher", "Contribute at https://www.github.com/m3hran/defiance-launcher")

def setMenu(type):
    statedata = json.load(open("state.json"))

    if type == "mod":
        if statedata["mod"] == "":
            a = parser5.find_existing("mod")
            if a:
                variable1.set(a)
                with open("state.json", "r") as jsonFile:
                    data = json.load(jsonFile)

                data[type] = a
                with open("state.json", "w") as jsonFile:
                    json.dump(data, jsonFile)
            else:
                variable1.set("MODs")
        if statedata["mod"] != "":
            variable1.set(statedata["mod"])

    if type == "map":
        if statedata["map"] == "":
            a = parser5.find_existing("map")
            if a:
                variable2.set(a)
                with open("state.json", "r") as jsonFile:
                    data = json.load(jsonFile)

                data[type] = a
                print("setting asset " + data[type])
                with open("state.json", "w") as jsonFile:
                    json.dump(data, jsonFile)

            else:
                variable2.set("MAPs")
        if statedata["map"] != "":
            variable2.set(statedata["map"])

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
            if not os.path.exists("mods/"+mod["folderName"]):
                lock.set("true")
                statusText.set("Downloading " + mod["name"] + " ...")
                dl_resources(mod["url"],"mod")
                #print("downloading "+mod["name"])
            lock.set("false")

        # Download Maps if necessary
        for map in data["maps"]:
            if not os.path.exists("maps/"+ map["folderName"]):
                lock.set("true")
                statusText.set("Downloading " + map["name"] + "...")
                dl_resources(map["url"],"map")
                #print("downloading "+map["name"])
            lock.set("false")
        statusText.set("Locating Steamapps...Please wait..")

        if (sema.acquire(blocking=False)):
            statusText.set("Ready.")
        sema.release()

    def callback2():
        sema.acquire()
        with open("state.json", "r") as jsonFile:
            data = json.load(jsonFile)

        if data["path"] == "" or data["path"] == None:
            statusText.set("Locating Steamapps...Please wait..")
            lock.set("true")
            install_path=parser5.find_installation()
            print("game path found!")
            statusText.set("Steamapps Located...")
            data["path"]=install_path
            with open('state.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False)
            if (sema.acquire(blocking=False)):
                statusText.set("Ready.")
            lock.set("false")
        sema.release()


    t1 = threading.Thread(target=callback1)
    t1.start()

    t2 = threading.Thread(target=callback2)
    t2.start()

def LaunchCiv():
    if sema.acquire(blocking=False):
        data = json.load(open("state.json"))
        print(data["path"])
        steampath=data["path"]
        steampath= re.sub('(steamapps).*', '', steampath)
        steampath=steampath+"Steam.exe"
        subprocess.Popen([steampath,"steam://rungameid/8930//%5Cdx11"])
        sema.release()
        root.destroy()

def SetAsset(name,type):

    with open("state.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data[type] = name

    if type == 'mod':
        p = "\\Assets\\DLC\\"
        q = "mods\\"
    if type == 'map':
        p = "\\Assets\\Maps\\"
        q = "maps\\"

    with open("resources.json", "r") as jsonFile:
        d = json.load(jsonFile)
    for mod in d[type+"s"]:
        if name == mod["name"]:
            name = mod["folderName"]

    dpath= data["path"] + p + name
    if not os.path.exists(dpath):
        def callback3():
            if type == 'mod':
                md.configure(state="disabled")
            if type == 'map':
                mp.config(state="disabled")
            sema.acquire()
            statusText.set("Modding...Please wait..")
            disableLaunch()


            shutil.copytree(q+name, dpath)
            with open("state.json", "w") as jsonFile:
                json.dump(data, jsonFile)
            sema.release()
            if (sema.acquire(blocking=False)):
                enableLaunch()
                if type == 'mod':
                    md.configure(state="active")
                if type == 'map':
                    mp.configure(state="active")
                statusText.set("Ready.")
                sema.release()

        t3 = threading.Thread(target=callback3)
        t3.start()

def rmAsset(type):
    with open("state.json", "r") as jsonFile:
        data = json.load(jsonFile)

    if data[type] != "":


        with open("resources.json", "r") as jsonFile:
            d = json.load(jsonFile)
        for mod in d[type + "s"]:
            if data[type] == mod["name"]:
                name = mod["folderName"]

        modp=data["path"] + "\\Assets\\DLC\\" + name + "\\"
        mapp=data["path"] + "\\Assets\\Maps\\" + name + "\\"
        def callback4():
            sema.acquire()
            disableLaunch()
            statusText.set("Removing...Please wait..")
            if type == 'mod':
                if os.path.exists(modp):
                        shutil.rmtree(modp)
            if type == 'map':
                if os.path.exists(mapp):
                        shutil.rmtree(mapp)

            data[type] = ""
            with open("state.json", "w") as jsonFile:
                json.dump(data, jsonFile)
            sema.release()
            if (sema.acquire(blocking=False)):
                enableLaunch()
                statusText.set("Ready.")
                sema.release()

        t4 = threading.Thread(target=callback4)
        t4.start()

#refact mod_select
def mod_select(name):
    data = json.load(open("state.json"))

    if name != None:
        if data["mod"] == "":
            print(name)
            SetAsset(name,"mod")
            variable1.set(name)
        else:
            if data["mod"] != name and sema.acquire(blocking=False):
                    rmAsset("mod")
                    SetAsset(name,"mod")
                    variable1.set(name)
                    sema.release()
    else:
        variable1.set("MODs")

def map_select(name):
    data = json.load(open("state.json"))

    if name != None:
        if data["map"] == "":
            SetAsset(name,"map")
            variable2.set(name)
        else:
            if data["map"] != name and sema.acquire(blocking=False):
                rmAsset("map")
                SetAsset(name,"map")
                variable2.set(name)
                sema.release()
    else:
        variable2.set("MAPs")

def removeAll():
    rmAsset("mod")
    variable1.set("MODs")
    rmAsset("map")
    variable2.set("MAPs")

def enableLaunch():
    LaunchButt.configure(state="active", image=LaunchIcon_en )

def disableLaunch():
    LaunchButt.configure(state="disabled")


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
    if sema.acquire(blocking=False):
        statusText.set("Launch..")
        sema.release()

def on_leave(event):
    if sema.acquire(blocking=False):
        statusText.set("Ready.")
        sema.release()

# ********* Main **********
#music
pygame.init()
pygame.mixer.music.load("baba.mp3")
pygame.mixer.music.play(-1)
ver="0.18.0503"
install_path = ""
fname=""
sema = threading.BoundedSemaphore(value=2)
sema2 = threading.BoundedSemaphore(value=1)


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

setMenu("mod")

if mod_dropdown != []:
    md = OptionMenu(f1, variable1, *mod_dropdown, command=mod_select)
else:
    md = OptionMenu(f1, variable1, None, command=mod_select)
md.pack(side=LEFT, padx=25)

map_dropdown=[]
data = json.load(open("resources.json"))

for map in data["maps"]:
    map_dropdown.append(map["name"])

setMenu("map")
if map_dropdown != []:
    mp = OptionMenu(f2, variable2, *map_dropdown, command=map_select)
else:
    mp = OptionMenu(f2, variable2, None, command=map_select)
mp.pack(side=LEFT, padx=25)


LaunchButt = Button(f3, text="Launch", command=LaunchCiv)

#LaunchIcon= PhotoImage(file="defiance_logo.png")
LaunchIcon_en= PhotoImage(file="launch3.png")
LaunchButt.config(image=LaunchIcon_en,height=82,width=82)
LaunchButt["bg"] = "white"
LaunchButt[ "border" ] = "3"
LaunchButt.pack(side=LEFT,pady=10)
LaunchButt.bind("<Enter>", on_enter)
LaunchButt.bind("<Leave>", on_leave)

init_resources()

root.mainloop()


