
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
    colorname = str

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

        top.geometry("1024x650+650+150")
        top.title("A CUBE VOXEL")
        top.configure(background=self.backgroundColor)

        self.lblLogo = Label(top)
        self.lblLogo.place(relx=0.06, rely=0.02, height=100, width = 100)  
        self.original = Image.open('./logo.png')
        resized = self.original.resize((100, 100),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized) # Keep a reference, prevent GC
        self.lblLogo.configure(image=self.image, background = self.backgroundColor)
        
        self.frmInputStl = LabelFrame(top)
        self.frmInputStl.place(relx=0.02, rely=0.18, relheight=0.1 , relwidth=0.25)
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
        self.frmLayerThickness.place(relx=0.02, rely=0.29, relheight=0.1 , relwidth=0.25)
        self.frmLayerThickness.configure(relief=RIDGE)
        self.frmLayerThickness.configure(text='''SPECIFY RESOLUTION VALUE''', font='bold')
        self.frmLayerThickness.configure(background=self.backgroundColor)

        self.entLayerThickness = Entry(self.frmLayerThickness)
        self.entLayerThickness.place(relx=0.05, rely=0.05, relheight=0.75, relwidth=0.9)
        self.entLayerThickness.insert(0, "")
        self.entLayerThickness.configure(background=self.backgroundColor)
        self.entLayerThickness.configure(justify=RIGHT)

        self.frmConvert = LabelFrame(top)
        self.frmConvert.place(relx=0.02, rely=0.39, relheight=0.08 , relwidth=0.25)
        self.frmConvert.configure(relief=RIDGE)
        self.frmConvert.configure(background=self.backgroundColor)

        self.btnStlToVoxel = Button(self.frmConvert)
        self.btnStlToVoxel.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)
        self.btnStlToVoxel.configure(text='''CONVERT TO VOXELS''', font='bold')
        self.btnStlToVoxel.bind("<Button-1>", self.stl_to_voxel_files)
        self.btnStlToVoxel.configure(background=self.backgroundColor)
        self.btnStlToVoxel.configure(disabledforeground=self.disabledforeground)

        self.frmModify = LabelFrame(top)
        self.frmModify.place(relx=0.02, rely=0.48, relheight=0.13 , relwidth=0.25)
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
        self.cboPartList.configure(state=DISABLED)

        self.lblPartColor = Label(self.frmModify)
        self.lblPartColor.place(relx=0.05, rely=0.5, relheight=0.3, relwidth=0.45)
        self.lblPartColor.configure(text=''' PART COLOR : ''' , font='bold')
        self.lblPartColor.configure(background=self.backgroundColor)

        self.cboPartColor = ttk.Combobox(self.frmModify)
        self.cboPartColor.place(relx=0.5, rely=0.5, relheight=0.3, relwidth=0.45)
        self.cboPartColor['values'] = ('RED', 'GREEN', 'BLUE', 'YELLOW', 'NAVY', 'GOLD', 'PURPLE', 'CYAN', 'ORANGE', 'AZURE', 'IVORY', 'SNOW', 'LINEN', 'CORNSILK', 'TOMATO', 'CORAL')
        self.cboPartColor.bind('<<ComboboxSelected>>', self.on_part_color)
        self.cboPartColor.configure(state=DISABLED)

        self.frmLayerColor = LabelFrame(top)
        self.frmLayerColor.place(relx=0.02, rely=0.62, relheight=0.17 , relwidth=0.25)
        self.frmLayerColor.configure(relief=RIDGE)
        self.frmLayerColor.configure(text='''MODIFY LAYER COLOR''', font='bold')
        self.frmLayerColor.configure(background=self.backgroundColor)
        
        self.lblColorMethod = Label(self.frmLayerColor)
        self.lblColorMethod.place(relx=0.05, rely=0.1, relheight=0.25, relwidth=0.45)
        self.lblColorMethod.configure(text='''METHOD : ''', font='bold')
        self.lblColorMethod.configure(background=self.backgroundColor)

        self.cboColorMethod = ttk.Combobox(self.frmLayerColor)
        self.cboColorMethod.place(relx=0.5, rely=0.1, relheight=0.25, relwidth=0.45)
        self.cboColorMethod['values'] = ('LAYER BY LAYER', 'HALF LAYER')
        self.cboColorMethod.bind('<<ComboboxSelected>>', self.on_color_method)
        self.cboColorMethod.current(0)
        self.cboColorMethod.configure(state=DISABLED)

        self.lblEvenColor = Label(self.frmLayerColor)
        self.lblEvenColor.place(relx=0.05, rely=0.38, relheight=0.25, relwidth=0.45)
        self.lblEvenColor.configure(text='''EVEN LAYER : ''', font='bold')
        self.lblEvenColor.configure(background=self.backgroundColor)

        self.cboEvenColor = ttk.Combobox(self.frmLayerColor)
        self.cboEvenColor.place(relx=0.5, rely=0.38, relheight=0.25, relwidth=0.45)
        self.cboEvenColor['values'] = ('RED', 'GREEN', 'BLUE', 'YELLOW', 'NAVY', 'GOLD', 'PURPLE', 'CYAN', 'ORANGE', 'AZURE', 'IVORY', 'SNOW', 'LINEN', 'CORNSILK', 'TOMATO', 'CORAL')
        self.cboEvenColor.bind('<<ComboboxSelected>>', self.on_even_color)
        self.cboEvenColor.current(0)
        self.cboEvenColor.configure(state=DISABLED)

        self.lblOddColor = Label(self.frmLayerColor)
        self.lblOddColor.place(relx=0.05, rely=0.66, relheight=0.25, relwidth=0.45)
        self.lblOddColor.configure(text='''ODD LAYER : ''' , font='bold')
        self.lblOddColor.configure(background=self.backgroundColor)

        self.cboOddColor = ttk.Combobox(self.frmLayerColor)
        self.cboOddColor.place(relx=0.5, rely=0.66, relheight=0.25, relwidth=0.45)
        self.cboOddColor['values'] = ('RED', 'GREEN', 'BLUE', 'YELLOW', 'NAVY', 'GOLD', 'PURPLE', 'CYAN', 'ORANGE', 'AZURE', 'IVORY', 'SNOW', 'LINEN', 'CORNSILK', 'TOMATO', 'CORAL')
        self.cboOddColor.bind('<<ComboboxSelected>>', self.on_odd_color)
        self.cboOddColor.current(0)
        self.cboOddColor.configure(state=DISABLED)

        self.frmMaterial = LabelFrame(top)
        self.frmMaterial.place(relx=0.02, rely=0.79, relheight=0.08 , relwidth=0.25)
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
        # self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax = self.fig.add_subplot((111), aspect='equal', projection='3d')
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.set_xlabel("Z", fontsize=12)
        self.ax.set_zlabel("X", fontsize=12)

    def open_directory_dialog(self, event):
        inputdirname = filedialog.askdirectory(initialdir = "./",title = "Select directory")
        if inputdirname:
            self.inputdirname = inputdirname
            print("selected directory: " + inputdirname)
            filenames=[]
            #filenames = fnmatch.filter(os.listdir(inputdirname), '*.stl')
            
            for filename in os.listdir(inputdirname):
                if filename.lower().endswith(('.stl')):
                    filenames.append(filename)
            filenames.sort()
            self.cboPartList['values'] = filenames
            self.cboPartList.current(0)
            if(len(filenames) == 1):
                self.cboEvenColor.configure(state=NORMAL)
                self.cboOddColor.configure(state=NORMAL)
                self.cboColorMethod.configure(state=NORMAL)
                self.cboPartList.configure(state=DISABLED)
                self.cboPartColor.configure(state=DISABLED)
            else:
                self.cboEvenColor.configure(state=DISABLED)
                self.cboOddColor.configure(state=DISABLED)
                self.cboColorMethod.configure(state=DISABLED)
                self.cboPartList.configure(state=NORMAL)
                self.cboPartColor.configure(state=NORMAL)

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
            resolution = int(layerthickness)
            convert.doExport(self.inputdirname + "/" + filename, outputfilename, resolution)
        self.show_model()

    def show_model(self):
        print('show model')
        # get filepaths
        dirpath = self.inputdirname + "/" + os.path.splitext(self.cboPartList.get())[0]
        count=len(fnmatch.filter(os.listdir(dirpath), '*.png'))
        counter=0
        boudingcounter=0
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
        # get height and width of one image.
        image =  cv2.imread(filepaths[0][0]) 
        print(filepaths[0][0])
        m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        h,w = np.shape(m)
        print(np.shape(m))

        py=0
        px=0

        #main processing part.
        g = np.zeros(shape=(h,w)) #2d array for one image
        k = np.zeros(shape=(count,h,w)) #3d array for images.This is used to show model.if the value=2, the voxel is showed.
        dimesions = Dimensions()
        dimesions.width = w # you can ignore this varaible .This is for xml.
        dimesions.height = h# you can ignore this varaible .This is for xml.
        dimesions.depth = count# you can ignore this varaible .This is for xml.
        self.content.dimensions = dimesions# you can ignore this varaible .This is for xml.
        self.content.voxel = list()# you can ignore this varaible .This is for xml.
        colors = np.array([[['#00000000']*w]*h]*count) #initiaize np with black color.
        for j in range(0,count):#count: images' count

            images = []#image list of one part
            m = []#color list of all part' images[part][y][x]
            for i in range(len(self.cboPartList['value'])):
                image = cv2.imread(filepaths[i][j])#this code is used only this part. To make m.
                images.append(image)#this code is used only this part. To make m.
                m.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
            for py in range(0,h):#h: image height
                for px in range(0,w):#w image width
                    k[j][py][px]=int(0)#initialize k with 0
                    for t in range(0,len(m)):#len(m): part's count such as 1, 3, 5 ...
                        if (m[t][py][px] == 255):#if m[t][py][px] is white, set color.
                            partCount = len(self.cboPartList['value'])
                            if (partCount == 1):
                                if (self.cboColorMethod.current() == 0):
                                    g[py][px]=g[py][px] + 2#this is not used.
                                    if(colors[j][py][px] == '#00000000'):#if colors is black color , set color.
                                        if (j % 2 == 0):
                                            colors[j][py][px] = self.cboEvenColor.get().lower()
                                        else:
                                            colors[j][py][px] = self.cboOddColor.get().lower()
                                        k[j][py][px]=int(2)#set k with 2.
                                    else:#if the color was already set, set white color.
                                        colors[j][py][px] = 'white'
                                        k[j][py][px]=int(0)      
                                else:
                                    g[py][px]=g[py][px] + 2#this is not used.
                                    if(colors[j][py][px] == '#00000000'):#if colors is black color , set color.
                                        if (j < count / 2):
                                            colors[j][py][px] = self.cboEvenColor.get().lower()
                                        else:
                                            colors[j][py][px] = self.cboOddColor.get().lower()
                                        k[j][py][px]=int(2)#set k with 2.
                                    else:#if the color was already set, set white color.
                                        colors[j][py][px] = 'white'
                                        k[j][py][px]=int(0)                                                             
                            else:
                                g[py][px]=g[py][px] + 2#this is not used.
                                if(colors[j][py][px] == '#00000000'):#if colors is black color , set part's color.
                                    colors[j][py][px] = self.partcolor[t]
                                    k[j][py][px]=int(2)#set k with 2.
                                else:#if the color was already set, set white color.
                                    colors[j][py][px] = 'white'
                                    k[j][py][px]=int(0)
                    #this part is for xml. you can ignore.
                    if(colors[j][py][px] != '#00000000' and colors[j][py][px] != 'white'):
                        voxel = Voxel()
                        hexcolor = matplotlib.colors.cnames[colors[j][py][px]].lstrip('#')
                        rgbcolor = str(tuple(int(hexcolor[i:i+2], 16) for i in (0, 2 ,4)))
                        voxel.colorname = colors[j][py][px]
                        voxel.color = rgbcolor
                        position = Position()
                        position.x = px
                        position.y = py
                        position.z = j
                        voxel.position = position 
                        self.content.voxel.append(voxel)
                        counter=counter+1 
                    if(colors[j][py][px] == 'white'):
                        boudingcounter=boudingcounter+1
        
        print("Total count of voxels: %d", count * w * h)
        print("Colored count of Voxels: %d", counter)
        filled = np.array(k)#initialize voxel with k. 
        self.ax.voxels(filled,facecolors=colors, edgecolors='gray')#initialize ax with voxel. this is library function.
        layerthickness = float(self.entLayerThickness.get())
        resolution = int(layerthickness)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.set_xlabel("Z", fontsize=12)
        self.ax.set_zlabel("X", fontsize=12)
        self.ax.set_xlim(0, resolution)
        self.canvas.draw()#draw model with ax.this is library function.

    def on_part_color(self, event):
        color = self.cboPartColor.get().lower()
        self.partcolor[self.cboPartList.current()] = color
        self.show_model()
    
    def on_even_color(self, event):
        color = self.cboPartColor.get().lower()
        self.partcolor[self.cboPartList.current()] = color
        self.show_model()

    def on_odd_color(self, event):
        color = self.cboPartColor.get().lower()
        self.partcolor[self.cboPartList.current()] = color
        self.show_model()

    def on_color_method(self, event):
        if(self.cboColorMethod.current() == 0):
            self.lblEvenColor['text'] = 'FIRST HALF';
            self.lblOddColor['text'] = 'SECOND HALF';
        else:
            self.lblEvenColor['text'] = 'EVEN LAYER';
            self.lblOddColor['text'] = 'ODD LAYER';           
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
        self.cboEvenColor.configure(state=DISABLED)
        self.cboOddColor.configure(state=DISABLED)
        self.cboPartList.configure(state=DISABLED)
        self.cboPartColor.configure(state=DISABLED)
        self.cboColorMethod.configure(state=DISABLED)

if __name__ == '__main__':
    vp_start_gui()
