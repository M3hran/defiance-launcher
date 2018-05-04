import os
import parser
from tkinter import *
import tkinter.messagebox
from urllib import request
from tkinter import simpledialog
import requests, zipfile, io, tldextract, json
import pygame


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

    print("dlc added!")

def remove_dlc(event):
    print("dlc removed!")

def add_map(event):
    print("map added!")

def remove_map(event):
    print("map removed!")

def ask_url():

    url = simpledialog.askstring("Input", "Note: You may only download zip files\nEnter URL: ")
    while( valid_url(url) != True ):
        tkinter.messagebox.showwarning("Invalid", "Not a valid URL. Please try again.")
        ask_url()
    return url

def dl_mod():

    if setup==False:
        url=ask_url()


    if not os.path.exists("mods"):
        os.makedirs("mods")

    ext = tldextract.extract(url)
    if ext.domain=="dropbox":
        url=url+"?raw=1"

    #download and unpack zip file in mod folder
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("mods/")

    print("mod downloaded!")

def dl_map():
    print("map pack downloaded!")

def aboutpage():
    tkinter.messagebox.showinfo("About Defiance-Launcher", "Visit us at https://www.github.com/m3hran/defiance-launcher")

#music
pygame.init()
pygame.mixer.music.load("baba.mp3")
pygame.mixer.music.play(-1)

ver="0.18.0503"
#install_path=parser.find_installation()
#print(install_path)
setup=False
root = Tk()
root.geometry("%dx%d+%d+%d" % (430, 200, 250, 350))
root.resizable(width=False, height=False)
window = myWindow(root)
window.pack(side=LEFT)
#SecondFrame = myWindow(root)
#SecondFrame.pack(side=LEFT)

# ********** Main Menu **********
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Add Mod...", command=dl_mod)
subMenu.add_command(label="Add Map pack...", command=doesnothing)
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
#RemoveButt = Button(toolbar, text="Remove all mods", command=dl_mod)
#RemoveButt.pack(side=LEFT, padx=2, pady=2)
AddModButt = Button(toolbar, text=" + Mod ", command=dl_mod)
AddModButt.pack(side=LEFT, padx=2, pady=2)
AddMapButt = Button(toolbar, text=" + Map ", command=doesnothing)
AddMapButt.pack(side=LEFT, padx=2, pady=2)
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
status = Label(root, text="Preparing to do nothing..", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)



# ********* Main **********
#title = Label(root, text="Defiance Launcher  "+ver, bg="blue", fg="white")
#title.pack(side=LEFT)
f1= Frame(root)
f1.pack(side=TOP)
f2= Frame(root)
f2.pack(side=TOP)

#load resources
data = json.load(open("resources.json"))

#generating MOD list
modselect = Label(f1, text="Select Mod:  ")
modselect.pack(side=LEFT)
mod_dropdown=[]
for mod in data["mods"]:
    print(mod["name"])
    mod_dropdown.append(mod["name"])
variable = StringVar(f1)
variable.set("MODs")
md= OptionMenu(f1,variable,*mod_dropdown)
md.pack(side=LEFT)

#generating MAP list
mapselect = Label(f2, text="Select Map:  ")
mapselect.pack(side=LEFT)
map_dropdown=[]
for map in data["maps"]:
    print(map["name"])
    map_dropdown.append(map["name"])
variable = StringVar(f2)
variable.set("MAPs")
mp= OptionMenu(f2,variable,*map_dropdown)
mp.pack(side=LEFT)


button1 = Button(f1, text="Mod", command=doesnothing)
#button1.bind("<Button-1>", doesnothing)
button2 = Button(f1, text="Un-Mod", command=doesnothing)
#button2.bind("<Button-1>", doesnothing)
button3 = Button(f2, text="Mod", command=doesnothing)
#button3.bind("<Button-1>", doesnothing)
button4 = Button(f2, text="Un-Mod", command=doesnothing)
#button4.bind("<Button-1>", doesnothing)

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=LEFT)

root.mainloop()


