
import sys

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import StlToVoxel_support
import os
import convert
from PIL import Image, ImageTk
from tkinter import colorchooser
import numpy
import pyconvert.pyconv

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
    outputdirname = ''
    vol = None
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

        self.lblVoxelPlayer = Label(top)
        self.lblVoxelPlayer.place(relx=0.26, rely=0.02, relheight=0.96, relwidth=0.72)
        self.lblVoxelPlayer.configure(background="#d9d9d9")
        self.lblVoxelPlayer.configure(borderwidth="2")
        self.lblVoxelPlayer.configure(highlightbackground="#d9d9d9")
        self.lblVoxelPlayer.configure(highlightcolor="black")
        self.lblVoxelPlayer.configure(relief=RIDGE)

        self.btnOpen = Button(top)
        self.btnOpen.place(relx=0.02, rely=0.1, height=64, width=207)
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

        self.lblResolution = Label(top)
        self.lblResolution.place(relx=0.02, rely=0.22, height=34, width=184)
        self.lblResolution.configure(activebackground="#f9f9f9")
        self.lblResolution.configure(activeforeground="black")
        self.lblResolution.configure(background="#d9d9d9")
        self.lblResolution.configure(disabledforeground="#a3a3a3")
        self.lblResolution.configure(foreground="#000000")
        self.lblResolution.configure(highlightbackground="#d9d9d9")
        self.lblResolution.configure(highlightcolor="black")
        self.lblResolution.configure(text='''Resolution''')

        self.entResolution = Entry(top)
        self.entResolution.place(relx=0.02, rely=0.3, height=34, width=207)
        self.entResolution.configure(background="white")
        self.entResolution.configure(disabledforeground="#a3a3a3")
        self.entResolution.configure(font="TkFixedFont")
        self.entResolution.configure(foreground="#000000")
        self.entResolution.configure(insertbackground="black")
        self.entResolution.insert(0, "100")
        self.entResolution.configure(width=304)

        self.btnStlToVoxel = Button(top)
        self.btnStlToVoxel.place(relx=0.02, rely=0.42, height=64, width=207)
        # self.btnStlToVoxel.configure(activebackground="#d9d9d9")
        # self.btnStlToVoxel.configure(activeforeground="#000000")
        # self.btnStlToVoxel.configure(background="#d9d9d9")
        # self.btnStlToVoxel.configure(disabledforeground="#a3a3a3")
        # self.btnStlToVoxel.configure(foreground="#000000")
        # self.btnStlToVoxel.configure(highlightbackground="#d9d9d9")
        # self.btnStlToVoxel.configure(highlightcolor="black")
        # self.btnStlToVoxel.configure(pady="0")
        self.btnStlToVoxel.configure(text='''StlToVoxel''')
        self.btnStlToVoxel.bind("<Button-1>", self.stl_to_voxel)

        self.cboImageList = ttk.Combobox(top)
        self.cboImageList.place(relx=0.02, rely=0.54, height=34, width=207)
        # self.cboImageList.configure(activebackground="#d9d9d9")
        # self.cboImageList.configure(activeforeground="#000000")
        # self.cboImageList.configure(background="#d9d9d9")
        # self.cboImageList.configure(disabledforeground="#a3a3a3")
        # self.cboImageList.configure(foreground="#000000")
        # self.cboImageList.configure(highlightbackground="#d9d9d9")
        # self.cboImageList.configure(highlightcolor="black")
        self.cboImageList.bind('<<ComboboxSelected>>', self.on_image_select)

        self.btnModelColor = Button(top)
        self.btnModelColor.place(relx=0.02, rely=0.66, height=64, width=207)
        # self.btnModelColor.configure(activebackground="#d9d9d9")
        # self.btnModelColor.configure(activeforeground="#000000")
        # self.btnModelColor.configure(background="#d9d9d9")
        # self.btnModelColor.configure(disabledforeground="#a3a3a3")
        # self.btnModelColor.configure(foreground="#000000")
        # self.btnModelColor.configure(highlightbackground="#d9d9d9")
        # self.btnModelColor.configure(highlightcolor="black")
        # self.btnModelColor.configure(pady="0")
        self.btnModelColor.configure(text='''Color''')
        self.btnModelColor.bind("<Button-1>", self.on_model_color)

        self.btnXml = Button(top)
        self.btnXml.place(relx=0.02, rely=0.82, height=64, width=207)
        # self.btnModelColor.configure(activebackground="#d9d9d9")
        # self.btnModelColor.configure(activeforeground="#000000")
        # self.btnModelColor.configure(background="#d9d9d9")
        # self.btnModelColor.configure(disabledforeground="#a3a3a3")
        # self.btnModelColor.configure(foreground="#000000")
        # self.btnModelColor.configure(highlightbackground="#d9d9d9")
        # self.btnModelColor.configure(highlightcolor="black")
        # self.btnModelColor.configure(pady="0")
        self.btnXml.configure(text='''Xml''')
        self.btnXml.bind("<Button-1>", self.on_xml)

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
            self.outputdirname = newdirectoryname
            print(self.outputname)

    def stl_to_voxel(self, event):
        self.vol = convert.doExport(self.inputname, self.outputname, int(self.entResolution.get()))
        self.lblVoxelPlayer.pack(side=TOP, fill=BOTH, expand=YES)
        # self.outputdirname = os.path.dirname("./examples/KJ1/KJ1.png")
        filenames = os.listdir(self.outputdirname)
        filenames.sort()
        self.cboImageList['values'] = filenames
        self.cboImageList.current(0)
        image = Image.open(os.path.join(self.outputdirname, self.cboImageList.get()))
        png = ImageTk.PhotoImage(image)
        self.lblVoxelPlayer.configure(image=png)
        self.lblVoxelPlayer.image = png
        
    def on_image_select(self, event):
        # self.outputdirname = os.path.dirname("./examples/KJ1/KJ1.png")
        image = Image.open(os.path.join(self.outputdirname, self.cboImageList.get()))
        png = ImageTk.PhotoImage(image)
        self.lblVoxelPlayer.configure(image=png)
        self.lblVoxelPlayer.image = png

    def on_model_color(self, event):
        color = colorchooser.askcolor() 
        # self.outputdirname = os.path.dirname("./examples/KJ1/KJ1.png")
        filename = os.path.join(self.outputdirname, self.cboImageList.get())
        image = Image.open(filename)
        pixels = image.load()
        height, width = image.size[0], image.size[1]
        color_image = Image.new('RGB', (height, width), color = 'black')
        color_pixels = color_image.load()
        for i in range(height):
            for j in range(width):
                    if pixels[i, j] == 0 or pixels[i, j] == (0, 0, 0):
                        continue
                    color_pixels[i, j] = (int(color[0][0]), int(color[0][1]), int(color[0][2]))
        color_image.save(filename)
        png = ImageTk.PhotoImage(color_image)
        self.lblVoxelPlayer.configure(image=png)
        self.lblVoxelPlayer.image = png

    def on_xml(self, event):
        print(self.vol)
        # xml = pyconvert.pyconv.convert2XML(self.vol)
        # print(xml.toprettyxml())

if __name__ == '__main__':
    vp_start_gui()



