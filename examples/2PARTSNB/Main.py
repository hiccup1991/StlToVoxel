
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

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import fnmatch
import shutil

matplotlib.use('TkAgg')


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

class Position(object):
    x = int
    y = int
    z = int

class Voxel(object):
    position = Position
    color = str

class Dimensions(object):
    width = int
    height = int
    depth = int

class Content(object):
    dimensions = Dimensions
    voxel = [Voxel]


class MainWindow:
    inputdirname = '/home/dev/Documents/StlToVoxel/examples'
    partcolor = ['red', 'green', 'blue', 'yellow', 'navy', 'gold', 'purple', 'cyan', 'orange', 'azure', 'ivory', 'snow', 'linen', 'cornsilk', 'tomato', 'coral']
    content = Content()
    backgroundColor = 'light blue'
    disabledforeground = '#a3a3a3'
    highlightbackground = '#5eff45'

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 

        top.geometry("937x579+650+150")
        top.title("A CUBE VOXEL")
        top.configure(background=self.backgroundColor)

        self.lblLogo = Label(top)
        self.lblLogo.place(relx=0.06, rely=0.02, height=100, width = 100)  
        self.original = Image.open('./logo.png')
        resized = self.original.resize((100, 100),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized) # Keep a reference, prevent GC
        self.lblLogo.configure(image=self.image, background = self.backgroundColor)
        
        self.frmInputStl = LabelFrame(top)
        self.frmInputStl.place(relx=0.02, rely=0.2, relheight=0.1 , relwidth=0.25)
        self.frmInputStl.configure(relief=RIDGE)
        self.frmInputStl.configure(text='''INPUT STL FILE''', font='bold')
        self.frmInputStl.configure(background=self.backgroundColor)
        
        self.btnOpen = Button(self.frmInputStl)
        self.btnOpen.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
        self.btnOpen.configure(text='''OPEN''', font='bold')
        self.btnOpen.bind("<Button-1>", self.open_directory_dialog)
        self.btnOpen.configure(background=self.backgroundColor)
        self.btnOpen.configure(disabledforeground=self.disabledforeground)

        self.frmLayerThickness = LabelFrame(top)
        self.frmLayerThickness.place(relx=0.02, rely=0.32, relheight=0.1 , relwidth=0.25)
        self.frmLayerThickness.configure(relief=RIDGE)
        self.frmLayerThickness.configure(text='''SPECIFY LAYER THICKNESS (in inch)''', font='bold')
        self.frmLayerThickness.configure(background=self.backgroundColor)

        self.entLayerThickness = Entry(self.frmLayerThickness)
        self.entLayerThickness.place(relx=0.05, rely=0.05, relheight=0.75, relwidth=0.9)
        self.entLayerThickness.insert(0, "0.02")
        self.entLayerThickness.configure(background=self.backgroundColor)
        self.entLayerThickness.configure(justify=RIGHT)

        self.frmConvert = LabelFrame(top)
        self.frmConvert.place(relx=0.02, rely=0.44, relheight=0.1 , relwidth=0.25)
        self.frmConvert.configure(relief=RIDGE)
        self.frmConvert.configure(background=self.backgroundColor)

        self.btnStlToVoxel = Button(self.frmConvert)
        self.btnStlToVoxel.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
        self.btnStlToVoxel.configure(text='''CONVERT TO VOXELS''', font='bold')
        self.btnStlToVoxel.bind("<Button-1>", self.stl_to_voxel_files)
        self.btnStlToVoxel.configure(background=self.backgroundColor)
        self.btnStlToVoxel.configure(disabledforeground=self.disabledforeground)

        self.frmModify = LabelFrame(top)
        self.frmModify.place(relx=0.02, rely=0.56, relheight=0.15 , relwidth=0.25)
        self.frmModify.configure(relief=RIDGE)
        self.frmModify.configure(text='''MODIFY CHANGES''', font='bold')
        self.frmModify.configure(background=self.backgroundColor)

        self.lblPart = Label(self.frmModify)
        self.lblPart.place(relx=0.05, rely=0.05, relheight=0.3, relwidth=0.45)
        self.lblPart.configure(text='''PART : ''', font='bold')
        self.lblPart.configure(background=self.backgroundColor)

        self.cboPartList = ttk.Combobox(self.frmModify)
        # self.cboPartList['values'] = ('KJ1.stl', 'KJ2.stl', 'KJ3.stl', 'KJ4.stl', 'KJ5.stl')
        # self.cboPartList.current(0)
        self.cboPartList.place(relx=0.5, rely=0.05, relheight=0.3, relwidth=0.45)
        self.cboPartList.configure(background=self.backgroundColor)

        self.lblPartColor = Label(self.frmModify)
        self.lblPartColor.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.45)
        self.lblPartColor.configure(text=''' PART COLOR : ''' , font='bold')
        self.lblPartColor.configure(background=self.backgroundColor)

        self.cboPartColor = ttk.Combobox(self.frmModify)
        self.cboPartColor.place(relx=0.5, rely=0.5, relheight=0.3, relwidth=0.45)
        self.cboPartColor['values'] = ('RED', 'GREEN', 'BLUE', 'YELLOW', 'NAVY', 'GOLD', 'PURPLE', 'CYAN', 'ORANGE', 'AZURE', 'IVORY', 'SNOW', 'LINEN', 'CORNSILK', 'TOMATO', 'CORAL')
        self.cboPartColor.bind('<<ComboboxSelected>>', self.on_part_color)

        self.frmMaterial = LabelFrame(top)
        self.frmMaterial.place(relx=0.02, rely=0.74, relheight=0.08 , relwidth=0.25)
        self.frmMaterial.configure(relief=RIDGE)
        self.frmMaterial.configure(text='''SPECIFY MATERIAL''', font='bold')
        self.frmMaterial.configure(background=self.backgroundColor)

        self.cboMaterial = ttk.Combobox(self.frmMaterial)
        self.cboMaterial.place(relx=0.05, rely=0.05, relheight=0.75, relwidth=0.9)
        self.cboMaterial['values'] = ('PLA', 'ABS')
        self.cboMaterial.current(0)

        self.frmSaveCancel = LabelFrame(top)
        self.frmSaveCancel.place(relx=0.02, rely=0.88, relheight=0.08 , relwidth=0.25)
        self.frmSaveCancel.configure(relief=RIDGE)
        self.frmSaveCancel.configure(background=self.backgroundColor)
        
        self.btnXml = Button(self.frmSaveCancel)
        self.btnXml.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.4)
        self.btnXml.configure(text='''SAVE''', font='bold')
        self.btnXml.bind("<Button-1>", self.on_xml)
        self.btnXml.configure(background=self.backgroundColor)
        self.btnXml.configure(disabledforeground=self.disabledforeground)

        self.btnCancel = Button(self.frmSaveCancel)
        self.btnCancel.place(relx=0.55, rely=0.05, relheight=0.9, relwidth=0.4)
        self.btnCancel.configure(text='''CANCEL''', font='bold')
        self.btnCancel.bind("<Button-1>", self.on_cancel)
        self.btnCancel.configure(background=self.backgroundColor)
        self.btnCancel.configure(disabledforeground=self.disabledforeground)

        self.cvsVoxelPlayer = Canvas(top)
        self.cvsVoxelPlayer.place(relx=0.28, rely=0.05, relheight=0.91, relwidth=0.70)   
        self.cvsVoxelPlayer.configure(background = self.backgroundColor)
        self.cvsVoxelPlayer.configure(borderwidth = '4')
        self.cvsVoxelPlayer.configure(relief=RIDGE)

        self.fig = Figure(figsize=(60, 60))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.cvsVoxelPlayer)
        self.canvas.get_tk_widget().pack(padx='5', pady='5')   
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_zlabel("z", fontsize=12)

    def open_directory_dialog(self, event):
        inputdirname = filedialog.askdirectory(initialdir = "./",title = "Select directory")
        if inputdirname:
            self.inputdirname = inputdirname
            print("selected directory: " + inputdirname)
            filenames = fnmatch.filter(os.listdir(inputdirname), '*.stl')
            filenames.sort()
            self.cboPartList['values'] = filenames
            self.cboPartList.current(0)

    def stl_to_voxel_files(self, event):
        for filename in self.cboPartList["values"]:
            only_name = os.path.splitext(filename)[0]
            outputdirectoryname = self.inputdirname + "/" + only_name
            print("outputdirectoryname: " + outputdirectoryname)
            if not os.path.exists(outputdirectoryname):
                os.mkdir(outputdirectoryname)
                print("Directory " , outputdirectoryname ,  " Created ")
            else:    
                shutil.rmtree(outputdirectoryname)
                os.mkdir(outputdirectoryname)
                print("Directory " , outputdirectoryname ,  " already exists")
            outputfilename = outputdirectoryname + "/" + only_name + ".png"
            print("outputfilename: " + outputfilename)
            layerthickness = float(self.entLayerThickness.get())
            resolution = int(1.0/layerthickness)
            convert.doExport(self.inputdirname + "/" + filename, outputfilename, resolution)
        self.show_model()

    def show_model(self):
        print('show model')
        dirpath = self.inputdirname + "/" + os.path.splitext(self.cboPartList.get())[0]
        count=len(fnmatch.filter(os.listdir(dirpath), '*.png'))
        counter=0
        filepaths = []
        for part in self.cboPartList['value']:
            dirpath = self.inputdirname + "/" + os.path.splitext(part)[0]
            temp = fnmatch.filter(os.listdir(dirpath), '*.png')
            temp.sort(reverse = True)
            for i in range(len(temp)):
                temp[i] = dirpath + "/" + temp[i] 
            filepaths.append(temp)
        print("FileList: ", filepaths)
        # reading images into matrix.
        print("No.of Slices:", count)
        image =  cv2.imread(filepaths[0][0])
        print(filepaths[0][0])
        m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        h,w = np.shape(m)
        print(np.shape(m))

        py=0
        px=0

        g = np.zeros(shape=(h,w))
        k = np.zeros(shape=(count,h,w))
        dimesions = Dimensions()
        dimesions.width = w
        dimesions.height = h
        dimesions.depth = count
        self.content.dimensions = dimesions
        self.content.voxel = list()
        colors = np.array([[['#00000000']*w]*h]*count)
        for j in range(0,count):

            images = []
            m = []
            for i in range(len(self.cboPartList['value'])):
                image = cv2.imread(filepaths[i][j])
                images.append(image)
                m.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
            for py in range(0,h):
                for px in range(0,w):
                    k[j][py][px]=int(0)
                    for t in range(0,len(m)):
                        if (m[t][py][px] == 255):
                            g[py][px]=g[py][px] + 2
                            if(colors[j][py][px] == '#00000000'):
                                colors[j][py][px] = self.partcolor[t]
                                k[j][py][px]=int(2)
                            else:
                                colors[j][py][px] = 'white'
                                k[j][py][px]=int(0)
                            counter=counter+1
                    if(colors[j][py][px] != '#00000000'):
                        voxel = Voxel()
                        hexcolor = matplotlib.colors.cnames[colors[j][py][px]].lstrip('#')
                        rgbcolor = str(tuple(int(hexcolor[i:i+2], 16) for i in (0, 2 ,4)))
                        voxel.color = rgbcolor
                        position = Position()
                        position.x = px
                        position.y = py
                        position.z = j
                        voxel.position = position 
                        self.content.voxel.append(voxel)

        print("Total count of Voxels: %d", count * w * h)
        print("Colored count of Voxels: %d", counter)
        filled = np.array(k)
        self.ax.voxels(filled,facecolors=colors, edgecolors='gray')
        self.canvas.draw()

    def on_part_color(self, event):
        color = self.cboPartColor.get().lower()
        self.partcolor[self.cboPartList.current()] = color
        self.show_model()

    def on_xml(self, event):
        xml_doc = pyconvert.pyconv.convert2XML(self.content)
        # print(xml_doc.toprettyxml())
        print('xml generating...')
        outputdirectoryname = self.inputdirname + "/result"
        if not os.path.exists(outputdirectoryname):
            os.mkdir(outputdirectoryname)
            print("Directory " , outputdirectoryname ,  " Created ")
        file = open(outputdirectoryname + "/" + "voxeldata.xml", 'w')
        file.write(xml_doc.toprettyxml())
        file.close()
        print('xml generated')

    def on_cancel(self, event):
        self.inputdirname = ''
        self.cboPartList['value']=''
        self.ax.cla()
        self.canvas.draw()

if __name__ == '__main__':
    vp_start_gui()



