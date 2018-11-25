import cv2
import numpy as np
import time
start_time = time.time()
 
# read image into matrix.
image =  cv2.imread("output/output01.png")
m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# get image properties.
#h,w,bpp = np.shape(m)
h,w = np.shape(m)
print(np.shape(m))
#k=[]
# print pixel value
y = 250
x = 0
print(m[y][x])
k = np.zeros(shape=(h,w))
#Iterate all image slides output00.png to output50.png
for py in range(0,h):
    for px in range(0,w):
        k[py][px]=np.int(m[py][px])
        print(m[py][px])
py=0
px=0
g = np.zeros(shape=(h,w))
print(m[y])
n_images=352
for j in range(0,n_images):
	# iterate over the entire image.
	i=n_images-j
	if i<10:
		image_name = "output00"+str(i)+".png"
	elif i<100:
		image_name = "output0"+str(i)+".png"
	else:
		image_name = "output"+str(i)+".png"

	image =  cv2.imread("output/"+image_name)
	m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	for py in range(0,h):
	    for px in range(0,w):
	    	if m[py][px]==255 :
	        	g[py][px]=g[py][px]+1
print(m[y][x])
print(len(k))
print(k)
print(len(k[0]))
print(len(k))
print(g)
print(k[1])
print("250th column before")
print(m[y])
print("250th column after")
print(g[250])


