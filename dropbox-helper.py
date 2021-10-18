from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import ctypes, sys
import os

window = Tk()
window.title('Dropbox Helper')
innerFrame = Frame(window)
innerFrame.grid(padx = 10, pady = 30)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

def selectPath():
    path_ = askdirectory().replace("/","\\")
    path_chosen.set(path_)

def selectDir():
    path2_ = askdirectory().replace("/","\\")
    if("Dropbox" in path2_):
        file_path_chosen.set(path2_)
        b.config(state = NORMAL)
    else:
        file_path_chosen.set("Please choose a directory in Dropbox folder")
        b.config(state = DISABLED)

def selectFile():
    path2_ = askopenfilename().replace("/","\\")
    if("Dropbox" in path2_):
        file_path_chosen.set(path2_)
        b.config(state = NORMAL)
    else:
        file_path_chosen.set("Please choose a directory in Dropbox folder")
        b.config(state = DISABLED)

def create():
    dir_ = os.path.dirname(file_path_chosen.get())
    relative_path = os.path.relpath(file_path_chosen.get(), dir_)
    if is_admin():
        if os.path.isdir(file_path_chosen.get()):
            print("mklink /d " + path_chosen.get() + "\\" + relative_path + " " + file_path_chosen.get())
            os.system("mklink /d " + path_chosen.get() + "\\" + relative_path + " " + file_path_chosen.get())
        elif os.path.isfile(file_path_chosen.get()):
            print("mklink " + path_chosen.get() + " " + relative_path)
            os.system("mklink " + path_chosen.get() + "\\" + relative_path + " " + file_path_chosen.get())
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

path_chosen = StringVar()
file_path_chosen = StringVar()
path_chosen.set(os.path.join(os.path.expanduser("~"),'Desktop'))
Label(innerFrame, text = "Target path").grid(row = 0, column = 0, padx = 5)
Entry(innerFrame, exportselection=0, width = 40, textvariable = path_chosen).grid(row = 0, column = 1)
Button(innerFrame, text = "Select Path", command = selectPath).grid(row = 0,column = 2, padx = 5)

b = Button(innerFrame, text='Create', width=10, command=create, state= DISABLED)
b.grid(row=2,columnspan = 4)
Label(innerFrame, text = "File from Dropbox").grid(row = 1, column = 0, padx = 5)
Entry(innerFrame, exportselection=0, width = 40, textvariable = file_path_chosen).grid(row = 1, column = 1)
Button(innerFrame, text = "Select Path", command = selectDir).grid(row = 1,column = 2, padx = 5)
Button(innerFrame, text = "Select File", command = selectFile).grid(row = 1,column = 3, padx = 5)

window.mainloop()
