import fnmatch
import os
dirpath="/home/routray/Desktop/test/slice_output/"
print len(fnmatch.filter(os.listdir(dirpath), '*.png'))