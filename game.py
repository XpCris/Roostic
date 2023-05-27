import win10toast
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import json
from random import randrange as rand
from threading import Thread

notification = win10toast.ToastNotifier()

def notify(title,body,icon="assets/toast.ico"):
    thread = Thread(target=lambda:notification.show_toast(title,body,icon_path=icon))
    thread.start()

window = Tk()
window.state("zoomed")
window.title("Roostic (Roosters will not be collected in the background)")
window.iconbitmap("assets/toast.ico")
bgimg = ImageTk.PhotoImage(file="assets/rooster_a.png")
Label(window,image=bgimg).place(anchor="center",relx=0.5,rely=0.5)
Label(window,text="All illustrations from https://emojidex.com").place(relx=0.815,y=670)

def readgamedata():
    f = open("assets/data.json","r")
    gamedata = json.loads(f.read())
    f.close()
    return gamedata

def writegamedata(datadict):
    f = open("assets/data.json","w")
    f.write(json.dumps(datadict))
    f.close()
    return readgamedata()

def addrooster(name,level):
    jsondata = readgamedata()
    jsondata["roosters"].append({"name":name,"level":level})
    print(jsondata)
    writegamedata(jsondata)
    global roosters
    for rooster in roosters:
        rooster.destroy()
    updateroosters()
    
roosters = []
roosternames = []
renameentries = []
images = []

def collectrooster():
    if iscollecting.get() == 1:
        print("Rooster collected!")
        notify("Roostic","A Rooster is here!","assets/toast.ico")
        addrooster("Rooster "+str(rand(0,9))+str(rand(0,9))+str(rand(0,9)),rand(0,999))
        startcollection()

def startcollection():
    if iscollecting.get() == 1:
        window.title("Roostic (Roosters will be collected in the background)")
    else:
        window.title("Roostic (Roosters will not be collected in the background)")
    print(iscollecting.get())
    time = rand(120,900)*1000
    print("Next rooster in "+str(time/1000)+" seconds.")
    window.after(time,collectrooster)

iscollecting = IntVar()
collectingcheckbox = ttk.Checkbutton(window,text="Collect roosters",variable=iscollecting,command=startcollection)
collectingcheckbox.place(x=20,y=670)

i = 0

def deleterooster(roosternum):
    gamedata = readgamedata()
    i = 0
    for rooster in gamedata["roosters"]:
        if rooster["name"] == roosternames[roosternum]:
            gamedata["roosters"].pop(i)
        i+=1
    writegamedata(gamedata)
    for rooster in roosters:
        rooster.destroy()
    updateroosters(False)

def renamerooster(roosternum):
    gamedata = readgamedata()
    i = 0
    for rooster in gamedata["roosters"]:
        if rooster["name"] == roosternames[roosternum]:
            gamedata["roosters"][i]["name"] = renameentries[roosternum].get()
        i+=1
    writegamedata(gamedata)
    for rooster in roosters:
        rooster.destroy()
    updateroosters(False)

def updateroosters(forcefocus=True):
    i = 0
    global roosters
    global renameentries
    roosters = []
    for rooster in readgamedata()["roosters"]:
        images.append(ImageTk.PhotoImage(file="assets/rooster_b.png"))
        roosterwindow = Toplevel(window)
        roosterwindow.protocol("WM_DELETE_WINDOW",lambda:deleterooster(i-1))
        roosterwindow.title(rooster["name"])
        roosterwindow.resizable(False,False)
        roosterwindow.geometry("250x100+0+"+str(30+i*60))
        roosterwindow.wm_attributes("-toolwindow","True")
        roosterwindow.transient(window)
        if forcefocus:
            roosterwindow.focus_force()
        
        ttk.Button(roosterwindow,text="Rename",command=lambda:renamerooster(i-1)).place(x=100,y=40,width=145)
        renameentry = ttk.Entry(roosterwindow)
        renameentry.place(x=100, y=70,width=145)
        renameentries.append(renameentry)
        ttk.Button(roosterwindow,text="Free this Rooster",command=lambda:deleterooster(i-1)).place(x=100,y=10,width=145)
        Label(roosterwindow,image=images[i]).place(x=0,y=-5,width=100,height=100)
        Label(roosterwindow,text="Level "+str(rooster["level"])).place(x=28,y=75)
        roosternames.append(rooster["name"])
        roosters.append(roosterwindow)
        i+=1

updateroosters()



if readgamedata()["intro"]:
    guide = Toplevel(window)
    guide.wm_attributes("-toolwindow","True","-topmost","True")
    guide.title("Welcome to the game!")
    Label(guide,text="This is a very simple game.\nTo start collecting roosters now, just check \"Collect Roosters\"\nand let the program sit in the background!\nYou will be notified when a rooster was catched.\n(this message won't appear again after closing it)").pack()
    newgamedata = readgamedata()
    newgamedata["intro"] = False
    writegamedata(newgamedata)

window.mainloop()