#importing the tkinter library
from tkinter import *

#Defining all Sub-Routines:
def speak():
    pass

#Make GUI
main=Tk()
main.title("A CUBE VOXEL")
main.geometry("800x800")

#adding a frame
GUIFrame=Frame(main)
GUIFrame.grid(row=1, column=0, sticky=W)

#ADD A LABEL
Label(main, text="SARTHAK ROUTRAY",font=40).grid(row=0, column=0, sticky=W)

#Add Button
Button(GUIFrame, text="RESOLUTION" , width=12, command=speak).grid(row=5, column=0, sticky=W, )
Button(GUIFrame, text="VOXELIZE" , width=12, command=speak).grid(row=10, column=0, sticky=W)












main.mainloop()




