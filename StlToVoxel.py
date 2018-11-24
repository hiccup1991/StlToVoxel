
import sys

from tkinter import *
from tkinter import filedialog
import StlToVoxel_support
import os
import convert

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = MainWindow(root)
    StlToVoxel_support.init(root, top)
    root.mainloop()

w = None
def create_MainWindow(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, rt
    rt = root
    w = Toplevel (root)
    top = MainWindow (w)
    StlToVoxel_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_MainWindow():
    global w
    w.destroy()
    w = None


class MainWindow:
    inputname = ''
    outputname = ''
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 

        top.geometry("937x579+650+150")
        top.title("StlToVoxel")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.cvsVoxelPlayer = Canvas(top)
        self.cvsVoxelPlayer.place(relx=0.23, rely=0.02, relheight=0.96, relwidth=0.75)
        self.cvsVoxelPlayer.configure(background="#d9d9d9")
        self.cvsVoxelPlayer.configure(borderwidth="2")
        self.cvsVoxelPlayer.configure(highlightbackground="#d9d9d9")
        self.cvsVoxelPlayer.configure(highlightcolor="black")
        self.cvsVoxelPlayer.configure(insertbackground="black")
        self.cvsVoxelPlayer.configure(relief=RIDGE)
        self.cvsVoxelPlayer.configure(selectbackground="#c4c4c4")
        self.cvsVoxelPlayer.configure(selectforeground="black")
        self.cvsVoxelPlayer.pack(expand=YES, fill=BOTH)
        png = tkinter.PhotoImage(file='/home/dev/Pictures/wallpaper.png')
        self.cvsVoxelPlayer.create_image(100, 100, image=png)

        self.btnOpen = Button(top)
        self.btnOpen.place(relx=0.01, rely=0.22, height=64, width=207)
        self.btnOpen.configure(activebackground="#d9d9d9")
        self.btnOpen.configure(activeforeground="#000000")
        self.btnOpen.configure(background="#d9d9d9")
        self.btnOpen.configure(disabledforeground="#a3a3a3")
        self.btnOpen.configure(foreground="#000000")
        self.btnOpen.configure(highlightbackground="#d9d9d9")
        self.btnOpen.configure(highlightcolor="black")
        self.btnOpen.configure(pady="0")
        self.btnOpen.configure(text='''Open''')
        self.btnOpen.bind("<Button-1>", self.open_file_dialog)

        self.btnStlToVoxel = Button(top)
        self.btnStlToVoxel.place(relx=0.01, rely=0.38, height=64, width=207)
        self.btnStlToVoxel.configure(activebackground="#d9d9d9")
        self.btnStlToVoxel.configure(activeforeground="#000000")
        self.btnStlToVoxel.configure(background="#d9d9d9")
        self.btnStlToVoxel.configure(disabledforeground="#a3a3a3")
        self.btnStlToVoxel.configure(foreground="#000000")
        self.btnStlToVoxel.configure(highlightbackground="#d9d9d9")
        self.btnStlToVoxel.configure(highlightcolor="black")
        self.btnStlToVoxel.configure(pady="0")
        self.btnStlToVoxel.configure(text='''StlToVoxel''')
        self.btnStlToVoxel.bind("<Button-1>", self.stl_to_voxel)

        self.entResolution = Entry(top)
        self.entResolution.place(relx=0.01, rely=0.54, height=64, width=207)
        self.entResolution.configure(background="white")
        self.entResolution.configure(disabledforeground="#a3a3a3")
        self.entResolution.configure(font="TkFixedFont")
        self.entResolution.configure(foreground="#000000")
        self.entResolution.configure(insertbackground="black")
        self.entResolution.insert(0, "100")
        self.entResolution.configure(width=304)

        self.btnModelColor = Button(top)
        self.btnModelColor.place(relx=0.01, rely=0.69, height=64, width=207)
        self.btnModelColor.configure(activebackground="#d9d9d9")
        self.btnModelColor.configure(activeforeground="#000000")
        self.btnModelColor.configure(background="#d9d9d9")
        self.btnModelColor.configure(disabledforeground="#a3a3a3")
        self.btnModelColor.configure(foreground="#000000")
        self.btnModelColor.configure(highlightbackground="#d9d9d9")
        self.btnModelColor.configure(highlightcolor="black")
        self.btnModelColor.configure(pady="0")
        self.btnModelColor.configure(text='''Color''')

        self.btnModelColor = Button(top)
        self.btnModelColor.place(relx=0.01, rely=0.84, height=64, width=207)
        self.btnModelColor.configure(activebackground="#d9d9d9")
        self.btnModelColor.configure(activeforeground="#000000")
        self.btnModelColor.configure(background="#d9d9d9")
        self.btnModelColor.configure(disabledforeground="#a3a3a3")
        self.btnModelColor.configure(foreground="#000000")
        self.btnModelColor.configure(highlightbackground="#d9d9d9")
        self.btnModelColor.configure(highlightcolor="black")
        self.btnModelColor.configure(pady="0")
        self.btnModelColor.configure(text='''Xml''')

        self.Label1 = Label(top)
        self.Label1.place(relx=0.02, rely=0.03, height=91, width=184)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Label''')

    def open_file_dialog(self, event):
        filename = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("stl files","*.stl"),))
        if filename:
            self.inputname = filename
            print(filename)
            directoryname = os.path.dirname(filename)
            filename_w_ext = os.path.basename(filename)
            only_name = os.path.splitext(filename_w_ext)[0]
            newdirectoryname = os.path.join(directoryname, only_name)
            print(newdirectoryname)
            print(directoryname)
            if not os.path.exists(newdirectoryname):
                os.mkdir(newdirectoryname)
                print("Directory " , newdirectoryname ,  " Created ")
            else:    
                print("Directory " , newdirectoryname ,  " already exists")
            self.outputname = newdirectoryname + "/" + only_name + ".png"
            print(self.outputname)
    def stl_to_voxel(self, event):
        convert.doExport(self.inputname, self.outputname, int(self.entResolution.get()))
        self.cvsVoxelPlayer.pack(expand=YES, fill=BOTH)
        png = PhotoImage(file='./examples/KJ1/KJ1011.png')
        self.cvsVoxelPlayer.create_image(0, 0, image=png)

if __name__ == '__main__':
    vp_start_gui()



