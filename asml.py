# Anti-social micro-log
# Done:
#   01:
# change name to micro-log
# changed directory finding code to just switch the current directory
# -- to where the script file is.
# switched to grid geometry manager.
# 01b:
#   added context menu code from leif04c.

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
        this.tx = ScrolledText(this.win,height=8,width=40,
                               undo=True, maxundo=-1, autoseparators=True)
        this.tx.grid(row=0,column=0,columnspan=2)
        this.tx.bind("<KeyRelease>",this.checklen)

        menustruct = [
                ['Undo', this.doUndo],
                ['Redo', this.doRedo],
                ['---','---'],
                ['Select All', this.doSelAll],
                ['Cut', this.doCut],
                ['Copy', this.doCopy],
                ['Paste', this.doPaste]
                ]

        m = Menu(this.win,tearoff=0)
        for lab,com in menustruct:
            if lab == '---':
                m.add_separator()
            else:
                m.add_command(label=lab,command=com)
        this.context = m
        this.tx.bind("<Button-3>",this.doContext)
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
    def doContext(this,e):
        try:
            this.context.tk_popup(e.x_root,e.y_root,0)
        finally:
            this.context.grab_release()

    def doUndo(this):
        try:
            this.tx.edit_undo()
        except TclError:
            pass

    def doRedo(this):
        try:
            this.tx.edit_redo()
        except TclError:
            pass
    def doSelAll(this):
        this.tx.tag_add("sel", '1.0', END)
        this.tx.focus_force()

    def doCut(this):
        if len(this.tx.tag_ranges("sel")) == 0:
            return
        this.win.clipboard_clear()
        this.win.clipboard_append(this.tx.selection_get())
        this.tx.delete(SEL_FIRST,SEL_LAST)
        this.win.update()

    def doCopy(this):
        this.win.clipboard_clear()
        this.win.clipboard_append(this.tx.selection_get())
        this.win.update()

    def doPaste(this):
        if len(this.tx.tag_ranges("sel")) != 0:
            this.tx.delete(SEL_FIRST,SEL_LAST)
        try:
            x = this.win.clipboard_get()
            this.tx.insert(INSERT, x)
        except TclError:
            pass

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
