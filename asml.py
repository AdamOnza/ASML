# Anti-social micro-log
# Todo:
# state copyright
# Done:
#   01:
# change name to micro-log
# changed directory finding code to just switch the current directory
# -- to where the script file is.
# switched to grid geometry manager.

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import time
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

ARCHIVE_FILE = "asml00.txt"
MAX_POST_SIZE = 500


# file format:
# each post is on it's own line.
#   (with any \ns escaped with "string_escape" encoding)

class logWindow:
    def __init__(this,savefile):
        this.savefile = savefile
        this.win = Tk()
        this.win.title("ASML")
        this.tx = ScrolledText(this.win,height=8,width=40)
        this.tx.grid(row=0,column=0,columnspan=2)
        this.tx.bind("<KeyRelease>",this.checklen)
        this.txle = Label(this.win, text="%i/%i"%(MAX_POST_SIZE,MAX_POST_SIZE))
        this.txle.grid(row=1,column=0)
        this.postbu = Button(this.win,text="post",command=this.post)
        this.postbu.grid(row=1,column=1)

    def mainloop(this):
        this.win.mainloop()
        #this.save()

    def checklen(this,e=None):
        x = this.tx.get(1.0, END)
        x = x.strip("\n")
        le = len(x)
        this.txle.config(text="%i/%i"%(MAX_POST_SIZE-le,MAX_POST_SIZE))

    def post(this):
        "Save a post."
        x = this.tx.get(1.0, END)
        x = x.strip("\n")
        print ("%i %r"%(len(x),x))
        if x != "":
            x = str(x).encode("unicode_escape")
            x = x.decode('utf-8')
            x = "\n" + time.strftime("%I:%M %p %m/%d/%Y\t") +x
            f = open(this.savefile,"a")
            f.write(x)
            f.close()
        this.tx.delete(1.0, END)
        this.checklen()

if __name__ == '__main__':
    print()
    
    # Open file. Create it if it doesn't exist.
    
    try:
        f = open(ARCHIVE_FILE,"rb")
        f.close()
    except FileNotFoundError:
        try:
            f = open(ARCHIVE_FILE,"wb")
            f.close()
        except:
            raise Exception("Unable to open or create savefile in current location.")
    mb = logWindow(ARCHIVE_FILE)
    mb.mainloop()
