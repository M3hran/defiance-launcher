import os, subprocess
import parser5
from tkinter import *
import tkinter.messagebox
from tkinter import simpledialog
import requests, zipfile, io, tldextract, json
import pygame, threading


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

def add_dlc(event):
    event.widget.pack_forget()
    button2.pack(side=LEFT)
    print("dlc added!")

def remove_dlc(event):
    event.widget.pack_forget()
    button1.pack(side=LEFT)
    print("dlc removed!")

def add_map(event):
    event.widget.pack_forget()
    button4.pack(side=LEFT)
    print("map added!")

def remove_map(event):
    event.widget.pack_forget()
    button3.pack(side=LEFT)
    print("map removed!")

def ask_url():

    url = simpledialog.askstring("Input", "Note: You may only download zip files\nEnter URL: ")
    while( valid_url(url) != True ):
        tkinter.messagebox.showwarning("Invalid", "Not a valid URL. Please try again.")
        ask_url()
    return url

def dl_resources(url, asset):
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
    tkinter.messagebox.showinfo("About Defiance-Launcher", "Visit us at https://www.github.com/m3hran/defiance-launcher")

def init_resources():
    #init in a different thread
    def callback1():
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
                statusText.set("Downloading " + mod["name"] + " ...")
                dl_resources(mod["url"],"mod")
                print("downloading "+mod["name"])


        # Download Maps if necessary
        for map in data["maps"]:
            if not os.path.exists("maps/"+ map["name"]):
                statusText.set("Downloading " + map["name"] + "...")
                dl_resources(map["url"],"map")
                print("downloading "+map["name"])
        statusText.set("Ready..")


    def callback2():
        statusText.set("Locating Steamapps...Please wait..")
        install_path=parser5.find_installation()

        data = { "path": install_path }
        with open('state.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        statusText.set("Ready..")

    t1 = threading.Thread(target=callback1)
    t1.start()
    if not os.path.isfile("state.json"):
        t2 = threading.Thread(target=callback2)
        t2.start()

def dl_map():
    a = ask_url()
    dl_resources(a,"map")

def dl_mod():
    a = ask_url()
    dl_resources(a,"mod")

def LaunchCiv():
    data = json.load(open("state.json"))
    print(data["path"])

    steampath=data["path"]
    steampath= re.sub('(steamapps).*', '', steampath)
    steampath=steampath+"Steam.exe"
    subprocess.Popen([steampath,"steam://rungameid/8930//%5Cdx11"])
    root.destroy()


# ********* Main **********
#music
pygame.init()
pygame.mixer.music.load("baba.mp3")
pygame.mixer.music.play(-1)
ver="0.18.0503"
install_path = ""




setup=False
root = Tk()
#background_image=PhotoImage(file="defiance_logo.png")
#background_label = Label(root, image=background_image)
#background_label.place(x=0, y=40, relwidth=1, relheight=1)
root.geometry("%dx%d+%d+%d" % (430, 300, 250, 350))
root.attributes("-alpha", 0.9)
root.configure(bg="#10397c")
root.resizable(width=False, height=False)

window = myWindow(root)
window.pack(side=LEFT)
statusText = StringVar()
statusText.set("Ready..")


# ********** Main Menu **********
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Add Mod...", command=dl_mod)
subMenu.add_command(label="Add Map pack...", command=dl_map)
subMenu.add_separator()
subMenu.add_command(label="Exit",command=root.destroy)

viewMenu = Menu(menu)
menu.add_cascade(label="View", menu=viewMenu)
viewMenu.add_command(label="View Mods", command=doesnothing)
viewMenu.add_command(label="View Maps", command=doesnothing)
viewMenu.add_command(label="View Logs", command=doesnothing)
viewMenu.add_command(label="About...", command=aboutpage)

# ****** Toolbar ********

toolbar = Frame(root, bg="blue")
RemoveButt = Button(toolbar, text="Remove Mods", command=doesnothing)
RemoveButt.pack(side=LEFT, padx=2, pady=2)
#AddModButt = Button(toolbar, text=" + Mod ", command=dl_mod)
#AddModButt.pack(side=LEFT, padx=2, pady=2)
#AddMapButt = Button(toolbar, text=" + Map ", command=dl_map)
#AddMapButt.pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)
checkCmd = IntVar()
checkCmd.set(1)

def muteselection():
    if checkCmd.get() == 1:
        pygame.mixer.music.pause()
    if checkCmd.get() == 0:
        pygame.mixer.music.unpause()
muteselection()
mute= Checkbutton(toolbar, text="Mute", variable=checkCmd, command=muteselection)
mute.pack(side=RIGHT)





# ***** Statusbar *******
status = Label(root, textvariable=statusText, bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)


#title = Label(root, text="Defiance Launcher  "+ver, bg="blue", fg="white")
#title.pack(side=LEFT)
f1= Frame(root, bg="#10397c")
f1.pack(side=TOP, pady=20)
f2= Frame(root, bg="#10397c")
f2.pack(side=TOP, pady=10)
f3= Frame(root, bg="#10397c")
f3.pack(side=BOTTOM)

#load resources
data = json.load(open("resources.json"))

#generating MOD list
#modselect = Label(f1, text="Select Mod:  ")
#modselect.pack(side=LEFT)
mod_dropdown=[]
for mod in data["mods"]:
    mod_dropdown.append(mod["name"])
variable = StringVar(f1)
variable.set("MODs")
md= OptionMenu(f1,variable,*mod_dropdown)
md.pack(side=LEFT, padx=25)

#generating MAP list
#mapselect = Label(f2, text="Select Map:  ")
#mapselect.pack(side=LEFT)
map_dropdown=[]
for map in data["maps"]:
    map_dropdown.append(map["name"])
variable = StringVar(f2)
variable.set("MAPs")
mp= OptionMenu(f2,variable,*map_dropdown)
mp.pack(side=LEFT, padx=25)


button1 = Button(f1, text="Mod")
button1.bind("<Button-1>", add_dlc)
button2 = Button(f1, text="Un-Mod")
button2.bind("<Button-1>", remove_dlc)
button3 = Button(f2, text="Mod")
button3.bind("<Button-1>", add_map)
button4 = Button(f2, text="Un-Mod")
button4.bind("<Button-1>", remove_map)

LaunchButt = Button(f3, text="Launch", command=LaunchCiv)

button1.pack(side=LEFT)
#button2.pack(side=LEFT)
button3.pack(side=LEFT)
#button4.pack(side=LEFT)

LaunchIcon= PhotoImage(file="defiance_logo.png")
LaunchButt.config(image=LaunchIcon,height=95,width=95)
LaunchButt.pack(side=LEFT,pady=8)


init_resources()

root.mainloop()


