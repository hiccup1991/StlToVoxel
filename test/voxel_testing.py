import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import fnmatch
import os
import time
start_time = time.time()
dirpath1 = "/home/routray/Desktop/test/slice_output/6/"
dirpath = "/home/routray/Desktop/test/slice_output/7/"
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
print("If you want to give colors to voxel press follow the rules below \n\r To give single color to voxels press 0 \n \r To color by layes press 1\n\r To give different colors to voxels press 2.\n\r To give different colors to half of structure Press 3. ")
dif = int(input(" Please give the input to proceed: "))
print("Your decision: ", dif)

# read image into matrix.
#image =  cv2.imread("out_test/output001.png")
#m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# reading images into matrix.
print("No.of Slices:", count)
if count > 1000:
	image =  cv2.imread("slice_output/output0001.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
elif count > 100:
	image =  cv2.imread("slice_output/output001.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
elif count > 10:
	image =  cv2.imread("slice_output/output01.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
else:
	image =  cv2.imread("slice_output/output1.png")
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# get image properties.
#h,w,bpp = np.shape(m)
h,w = np.shape(m)
print(np.shape(m))
#k=[]
# print pixel value
#y = 2
#x = 0
#print(m[y][x])
l = np.zeros(shape=(h,w))
#Iterate all image slides output00.png to output50.png
for py in range(0,h):
    for px in range(0,w):
        l[py][px]=np.int(m[py][px])
        #print(m[py][px])
py=0
px=0
n_images=count-1
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

	image =  cv2.imread("slice_output/"+image_name)
	print(image_name)
	print(i)
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#k2=[]
	for py in range(0,h):
		#k1=[]
		#print(k1[0])
		for px in range(0,w):
			if (m[py][px]==255):
				#x=1,y=1
				g[py][px]=g[py][px]+1
				#(j*py*px)%2
				#counter%2 for voxel
				#colors[j][py][]=str('#ff00ffff')
				if dif==1:
					c=j%2
				elif dif==2:
					c=counter%2
				elif dif==3:
					if j < count/2:
						c=1
					else:
						c=0
				else:
					c=1

				if c==1:
					#if dif==1:
					colors[j][py][px]=str('#00ffffff')
					k[j][py][px]=int(1)
				else:
					#if dif==1:
					colors[j][py][px]=str('#ff00ffff')
					#colors[j][py][px]=str('#ff00ffff')
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

plt.show()


