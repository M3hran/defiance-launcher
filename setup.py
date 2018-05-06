from cx_Freeze import setup, Executable
import sys, os

appName="Defiance Launcher"
version="0.18.503"
base=None
description = "Defiance Launcher"
author = "M3hran"
author_email = "m3hran@gmail.com"

if sys.platform=='win32':
    base="WIN32GUI"

if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', "C:\\Defiance Launcher"]

#https://msdn.microsoft.com/en-us/library/aa370905(v=vs.85).aspx#System_Folder_Properties
shortcut_table = [
    ("DesktopShortcut",                         # Shortcut
     "DesktopFolder",                           # Directory_
     appName,                                   # Name
     "TARGETDIR",                               # Component_
     "[TARGETDIR]defiance_launcher.exe",        # Target
     None,                                      # Arguments
     None,                                      # Description
     None,                                      # Hotkey
     "",                            # Icon
     "",                                        # IconIndex
     None,                                      # ShowCmd
     'TARGETDIR'                                # WkDir
     )
    ]

msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}


exe = Executable("defiance_launcher.py",icon="launcher.ico",shortcutName="Defiance Launcher",shortcutDir="DesktopFolder", base=base)
os.environ['TCL_LIBRARY'] = r'C:\Users\M3hran\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\M3hran\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

includes=[]
include_files = [ r'C:\Users\M3hran\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll',
                  r'C:\Users\M3hran\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\launcher.ico',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\launcher_favicon.ico',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\launch3.png',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\baba.mp3',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\state.json',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\resources.json',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\mods',
                  r'C:\Users\M3hran\PycharmProjects\defiance-launcher\maps'
                  ]

setup(
    name = appName,
    version = version,
    description = description,
    author = author,
    author_email = author_email,
    options = {"build_exe": {
        'packages': ["os","subprocess","shutil", "idna","tkinter","requests","zipfile","io","tldextract","json","pygame","threading", "re"],
         "includes": includes, "include_files": include_files
    },
    "bdist_msi": bdist_msi_options
    },
    executables = [exe]
    )