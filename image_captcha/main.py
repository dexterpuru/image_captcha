
import tkinter
from tkinter import *
root = Tk()
root.geometry("1000x700")
root.resizable(width=FALSE, height=FALSE)
import Captcha
captcha = Captcha.Captcha(root,1) # GROUP ID INITIALIZE WITH 1
root.mainloop()