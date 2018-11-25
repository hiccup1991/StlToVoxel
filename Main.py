
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


class MainWindow:
    inputdirname = '/home/dev/Documents/StlToVoxel/examples'
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
        top.configure(highlightcolor="black")

        self.cvsVoxelPlayer = Canvas(top)
        self.cvsVoxelPlayer.place(relx=0.26, rely=0.02, relheight=0.96, relwidth=0.72)   
        self.cvsVoxelPlayer.configure(background = 'white')
        self.cvsVoxelPlayer.configure(borderwidth = '4')
        self.cvsVoxelPlayer.configure(relief=RIDGE)

        self.btnOpen = Button(top)
        self.btnOpen.place(relx=0.02, rely=0.1, height=64, width=207)
        self.btnOpen.configure(text='''Open''')
        self.btnOpen.bind("<Button-1>", self.open_directory_dialog)

        self.lblResolution = Label(top)
        self.lblResolution.place(relx=0.02, rely=0.22, height=34, width=184)
        self.lblResolution.configure(text='''Resolution''')

        self.entResolution = Entry(top)
        self.entResolution.place(relx=0.02, rely=0.3, height=34, width=207)
        self.entResolution.insert(0, "50")
        self.entResolution.configure(width=304)

        self.btnStlToVoxel = Button(top)
        self.btnStlToVoxel.place(relx=0.02, rely=0.42, height=64, width=207)
        self.btnStlToVoxel.configure(text='''StlToVoxel''')
        self.btnStlToVoxel.bind("<Button-1>", self.stl_to_voxel_files)

        self.cboPartList = ttk.Combobox(top)
        self.cboPartList['values'] = ('KJ1.stl', 'KJ2.stl', 'KJ3.stl', 'KJ4.stl', 'KJ5.stl')
        self.cboPartList.current(0)
        self.cboPartList.place(relx=0.02, rely=0.6, height=34, width=207)

        self.cboPartColor = ttk.Combobox(top)
        self.cboPartColor.place(relx=0.02, rely=0.72, height=34, width=207)
        self.cboPartColor['values'] = ('red', 'green', 'blue', 'cyan', 'yellow', 'magenta')
        self.cboPartColor.configure(text='''Color''')
        self.cboPartColor.bind('<<ComboboxSelected>>', self.on_part_color)

        self.btnXml = Button(top)
        self.btnXml.place(relx=0.02, rely=0.82, height=64, width=207)
        self.btnXml.configure(text='''Xml''')
        self.btnXml.bind("<Button-1>", self.on_xml)

    def open_directory_dialog(self, event):
        inputdirname = filedialog.askdirectory(initialdir = "./",title = "Select directory")
        if inputdirname:
            self.inputdirname = inputdirname
            print("selected directory: " + inputdirname)
            filenames = []
            print("filelist: ")
            for file in os.listdir(inputdirname):
                if os.path.isfile(os.path.join(inputdirname, file)):
                    print(file)
                    filenames.append(file)
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
            convert.doExport(self.inputdirname + "/" + filename, outputfilename, int(self.entResolution.get()))
        self.show_model()

    def make_ax(self, grid=False):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.grid(grid)
        return ax

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
        colors = np.array([[['#ffffffff']*w]*h]*count)
        k1=np.zeros(shape=(w))
        k2=np.zeros(shape=(h,w))
        for j in range(0,count):

            images = []
            m = []
            for i in range(len(self.cboPartList['value'])):
                image = cv2.imread(filepaths[i][j])
                images.append(image)
                m.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
            #k2=[]
            for py in range(0,h):
                for px in range(0,w):
                    for t in range(0,len(m)):
                        if ((m[0][py][px]==255) and (m[1][py][px]==255)):
                            #x=1,y=1
                            g[py][px]=g[py][px]+2
                            colors[j][py][px]=str('#ffffffff')
                            k[j][py][px]=int(0)
                            counter=counter+1
                        elif (m[0][py][px]==255):
                            #x=1,y=1
                            g[py][px]=g[py][px]+2
                            colors[j][py][px]=str('#ff0000ff')
                            k[j][py][px]=int(2)
                            counter=counter+1
                        elif (m[1][py][px]==255):
                            #x=1,y=1
                            g[py][px]=g[py][px]+2
                            colors[j][py][px]=str('#00ff00ff')
                            k[j][py][px]=int(2)
                            counter=counter+1
                        elif (m[2][py][px]==255):
                            #x=1,y=1
                            g[py][px]=g[py][px]+2
                            colors[j][py][px]=str('#0000ffff')
                            k[j][py][px]=int(2)
                            counter=counter+1
                        elif (m[3][py][px]==255):
                            #x=1,y=1
                            g[py][px]=g[py][px]+2
                            colors[j][py][px]=str('#ffff00ff')
                            k[j][py][px]=int(2)
                            counter=counter+1
                        elif (m[4][py][px]==255):
                            #x=1,y=1
                            g[py][px]=g[py][px]+2
                            colors[j][py][px]=str('#ff00ffff')
                            k[j][py][px]=int(2)
                            counter=counter+1
                        else:
                            k[j][py][px]=int(0)		
                print(k[j])
        print("Total no.of Voxels:")
        print(count*h*w)
        filled = np.array(k)

        fig = Figure(figsize=(60, 60))
        canvas = FigureCanvasTkAgg(fig, master=self.cvsVoxelPlayer)
        canvas.get_tk_widget().pack()   
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title ("Estimation Grid", fontsize=16)
        ax.set_ylabel("Y", fontsize=14)
        ax.set_xlabel("X", fontsize=14)
        ax.set_zlabel("z", fontsize=14)
        ax.voxels(filled,facecolors=colors, edgecolors='gray')

        canvas.draw()

    def on_part_color(self, event):
        print(self.cboPartColor.get())

    def on_xml(self, event):
        print(self.vol)

if __name__ == '__main__':
    vp_start_gui()



