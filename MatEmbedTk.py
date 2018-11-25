
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import fnmatch
import os
import time
start_time = time.time()
dirpath = "/home/dev/Documents/StlToVoxel/test/slice_output/1/"
count=len(fnmatch.filter(os.listdir(dirpath), '*.png'))
counter=0


def make_ax(grid=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.grid(grid)
    return ax
# print("If you want to give colors to voxel press follow the rules below \n\r To give single color to voxels press 0 \n \r To color by layes press 1\n\r To give different colors to voxels press 2.\n\r To give different colors to half of structure Press 3. ")
# dif = int(input(" Please give the input to proceed: "))
# print("Your decision: ", dif)

# read image into matrix.
#image =  cv2.imread("out_test/output001.png")
#m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# reading images into matrix.
print("No.of Slices:", count)
if count > 1000:
	image =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/1/output0001.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
elif count > 100:
	image =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/1/output001.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
elif count > 10:
	image =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/1/output01.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
else:
	image =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/1/output1.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print("No.of Slices:", count)
# if count > 1000:
# 	image1 =  cv2.imread("slice_output/2/output0001.png")
# 	m1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# elif count > 100:
# 	image1 =  cv2.imread("slice_output/2/output001.png")
# 	m1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# elif count > 10:
# 	image1 =  cv2.imread("slice_output/2/output01.png")
# 	m1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# else:
# 	image1 =  cv2.imread("slice_output/2/output1.png")
# 	m1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# get image properties.
#h,w,bpp = np.shape(m)
h,w = np.shape(m)
print(np.shape(m))
#k=[]
# print pixel value
#y = 2
#x = 0
#print(m[y][x])
# l = np.zeros(shape=(h,w))
# l1 = np.zeros(shape=(h,w))
#Iterate all image slides output00.png to output50.png
# for py in range(0,h):
#     for px in range(0,w):
#         l[py][px]=np.int(m[py][px])
#         #print(m[py][px])
# py=0
# px=0

# for py in range(0,h):
#     for px in range(0,w):
#         l1[py][px]=np.int(m1[py][px])
#         #print(m[py][px])
py=0
px=0
# n_images=count-1
#print(m[y])
g = np.zeros(shape=(h,w))
k = np.zeros(shape=(count,h,w))
colors = np.array([[['#ffffffff']*w]*h]*count)
k1=np.zeros(shape=(w))
k2=np.zeros(shape=(h,w))
for j in range(0,count):
	# iterate over the entire image.
	i=count-j-1
	if count >= 100:
		if i<10:
			image_name = "output00"+str(i)+".png"
		elif i<100:
			image_name = "output0"+str(i)+".png"
		else:
			image_name = "output"+str(i)+".png"
	elif count>=10:
		if i<10:
			image_name = "output0"+str(i)+".png"
		else:
			image_name = "output"+str(i)+".png"
	else:
		image_name = "output"+str(i)+".png"

	image1 =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/1/"+image_name)
	image2 =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/2/"+image_name)
	image3 =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/3/"+image_name)
	image4 =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/4/"+image_name)
	image5 =  cv2.imread("/home/dev/Documents/StlToVoxel/test/slice_output/5/"+image_name)

	print(image_name)
	print(i)
	m1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
	m2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
	m3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
	m4 = cv2.cvtColor(image4, cv2.COLOR_BGR2GRAY)
	m5 = cv2.cvtColor(image5, cv2.COLOR_BGR2GRAY)
	#k2=[]
	for py in range(0,h):
		#k1=[]
		#print(k1[0])
		for px in range(0,w):

			if ((m1[py][px]==255) and (m2[py][px]==255)):
				#x=1,y=1
				g[py][px]=g[py][px]+2
				colors[j][py][px]=str('#ffffffff')
				k[j][py][px]=int(0)
				counter=counter+1
			elif (m1[py][px]==255):
				#x=1,y=1
				g[py][px]=g[py][px]+2
				colors[j][py][px]=str('#ff0000ff')
				k[j][py][px]=int(2)
				counter=counter+1
			elif (m2[py][px]==255):
				#x=1,y=1
				g[py][px]=g[py][px]+2
				colors[j][py][px]=str('#00ff00ff')
				k[j][py][px]=int(2)
				counter=counter+1
			elif (m3[py][px]==255):
				#x=1,y=1
				g[py][px]=g[py][px]+2
				colors[j][py][px]=str('#0000ffff')
				k[j][py][px]=int(2)
				counter=counter+1
			elif (m4[py][px]==255):
				#x=1,y=1
				g[py][px]=g[py][px]+2
				colors[j][py][px]=str('#ffff00ff')
				k[j][py][px]=int(2)
				counter=counter+1
			elif (m5[py][px]==255):
				#x=1,y=1
				g[py][px]=g[py][px]+2
				colors[j][py][px]=str('#ff00ffff')
				k[j][py][px]=int(2)
				counter=counter+1
			else:
				k[j][py][px]=int(0)		
		print(k[j])
		#k2[py]=k1
	#k[j]=k2
	#filled = np.array(k)
	#ax = make_ax(True)
	#print(ax)
	#ax.voxels(filled,facecolors=colors, edgecolors='gray')
	#print("k:\n")
	#print(k)
	
#print(k)
print("Total no.of Voxels:")
print(count*h*w)
#print("Your decision:",dif)

#print(m[y][x])
#print(len(k))
#print(k)
#print(len(k[0]))
#print(len(k))
#print(g)
#print(k[1])
#print("Filled Voxel:")
#print(counter)
#colors=explode(colors)
#print(colors[j])
filled = np.array(k)
print("--- %s seconds ---" % (time.time() - start_time))
ax = make_ax(True)
print(ax)
ax.voxels(filled,facecolors=colors, edgecolors='gray')
plt.axis('scaled')
#plt.set_ylabel()
# plt.show()


import random
import matplotlib
import tkinter as Tk
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.25)

# y_values = [random.randrange(20, 40, 1) for _ in range(40)]
# x_values = [i for i in range(40)]

# l, = plt.plot(x_values, y_values)
# plt.axis([0, 9, 20, 40])

# ax_time = plt.axes([0.12, 0.1, 0.78, 0.03])
# s_time = Slider(ax_time, 'Time', 0, 30, valinit=0)


# def update(val):
    # pos = s_time.val
    # ax.axis([pos, pos+10, 20, 40])
    # fig.canvas.draw_idle()
# s_time.on_changed(update)

# plt.show()
matplotlib.use('TkAgg')

fig = Figure(figsize=(60,60))
a = fig.add_subplot(111, projection='3d')


a.set_title ("Estimation Grid", fontsize=16)
a.set_ylabel("Y", fontsize=14)
a.set_xlabel("X", fontsize=14)
a.set_zlabel("z", fontsize=14)
a.voxels(filled,facecolors=colors, edgecolors='gray')

root = Tk.Tk()
root.wm_title("Embedding in TK")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
# Axes3D.mouse_init()
canvas.draw()

# fig = plt.figure()
# matplotlib.use('TkAgg')

# root = Tk.Tk()
# root.wm_title("Embedding in TK")

# canvas = FigureCanvasTkAgg(fig, master=root)

# canvas.draw()
# canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
# canvas.draw()
Tk.mainloop()