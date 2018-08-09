##############################################################
#path to downloaded images
#download_path = r'C:/tmp/download_glasses/'
download_path = r'C:/tmp/download_glasses/unseen_test/'

#output path to alpha mattes
#a_path = r'C:/tmp/alpha/'
a_path = r'C:/tmp/alpha/unseen_test/'

#output Path to fg images
#fg_path = r'C:/tmp/foreground/'
fg_path = r'C:/tmp/foreground/unseen_test/'

##############################################################

from PIL import Image
import os 
import math
import time
import random


ori_files = os.listdir(download_path)
fcount = 0
for im_name in ori_files:
    
    im = Image.open(download_path + im_name)
    if im.mode != 'RGBA':
        raise ValueError("does not have alpha channel!!!")
    red, green, blue, alpha = im.split()
    alpha.save(a_path + str(fcount).zfill(4) + '.png', "PNG")
    out = im.convert('RGB')
    out.save(fg_path + str(fcount).zfill(4) + '.png', "PNG")
    fcount +=1
