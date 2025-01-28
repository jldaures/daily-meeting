#!/usr/bin/env python
# -*- coding: utf8 -*-


help_msg = """
Tool for Daily Meetings
@author: daures
@version: 1.3
"""

import tkinter
import tkinter.ttk
import tkinter.messagebox
import random
import time
import threading


members = [ ["teammate 1",     0, None],
            ["teammate 2",     0, None],
            ["teammate 3",     0, None],
            ["teammate 4",     0, None],
            ["teammate 5",     0, None]
          ]

STEP_SEC = 1
MAX_STEPS = 10
GREEN_RED_RATION = 3/4
total_steps = 0
timer = None

def main():
    root = tkinter.Tk()
    root.title("Daily Meeting")
    root.geometry("+200+200")
    createWidgets(root)
    createMenu(root)
    root.lift()
    root.attributes('-topmost', True)
    root.mainloop()

def createWidgets(root):
    global name_var
    global name_label, colour
    global progress_var
    global progress_bar
    frame = tkinter.Frame(root)
    but   = tkinter.Button(frame, text="  Next  ", command=select_member,
                           font=('courier', 12, 'bold'), bg='forest green', fg='white', height=2, width=10)
    but.grid(row=1, column=1)
    name_var   = tkinter.StringVar()
    name_var.set("None")
    colour = tkinter.StringVar()
    colour.set('grey')
    name_label = tkinter.Label(frame,  textvariable=name_var , width=15, font=('courier', 12, 'bold'), bg=colour.get()).grid(row=1, column=2)
    style = tkinter.ttk.Style()
    style.theme_use('alt')
    style.configure('red.Horizontal.TProgressbar', background='red')
    style.configure('green.Horizontal.TProgressbar', background='green')
    progress_var = tkinter.DoubleVar()
    progress_bar = tkinter.ttk.Progressbar(frame, variable=progress_var, maximum=MAX_STEPS, mode ="determinate", style='green.Horizontal.TProgressbar')
    progress_bar.grid(row=2, column=2)
    for i, m in enumerate(members) :
        tkinter.Label(frame,  text=m[0] , width=15).grid(row=(i+3), column=1)
        m[2] = tkinter.IntVar()
        m[2].set(m[1])
        check = tkinter.Checkbutton(frame, variable=m[2]).grid(row=(i+3), column=2)
    frame.grid(row=3, column=2)

def createMenu(root):
    menubar = tkinter.Menu(root)
    menubar.add_command(label="Exit", command=root.destroy)
    menubar.add_command(label="Help", command=helpfunc)
    root.config(menu=menubar)

def helpfunc() :
    tkinter.messagebox.showinfo('help', help_msg)

def progress_bar_management(reset):
    global progress_var
    global total_steps
    global timer
    if reset :
        if timer is not None:
            timer.cancel()
        total_steps = 0
    progress_var.set(total_steps)
    if (total_steps < MAX_STEPS):
        if (total_steps < (MAX_STEPS*GREEN_RED_RATION)):
            progress_bar.config(style='green.Horizontal.TProgressbar')
        else:
            progress_bar.config(style='red.Horizontal.TProgressbar')
        timer = threading.Timer(STEP_SEC, progress_bar_management, (False,))
        timer.start()
        total_steps += STEP_SEC
    else:
        timer = None
        total_steps = 0

def select_member():
    for m in members:
        m[1] = m[2].get()
    not_reported = [m[0] for m in members if m[1] == 0]
    if not not_reported:
        tkinter.messagebox.showinfo("Next", "Everyone has reported")
    else:
        random.seed(time.time())
        rnd = random.SystemRandom()
        sel = rnd.choice(not_reported)
        name_var.set(sel)
        for m in members:
            if m[0] == sel:
                m[1] = 1
                m[2].set(1)
                progress_bar_management(True)


if __name__ == '__main__':
    main()
