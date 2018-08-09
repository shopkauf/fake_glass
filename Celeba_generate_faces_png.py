
##############################################################
#Path to FACES
bg_path = r'F:/celebA/celebA-HQ/'
#bg_path = r'F:/celebA/testing/'

#Path to folder where you want the composited images to go
out_path2 = 'C:/tmp/faces_unseen_test/'


##############################################################

from PIL import Image
import os 
import math
import time
import random
import numpy as np

bg_files = os.listdir(bg_path)
bcount = 0
for bg_name in bg_files:

    bcount += 1

    # TRAINING DATA:
    #if bcount > 2000:
    #    break

    # TEST DATA:
    #if bcount < 29000:
    if bcount < 29900:
        continue

    ## convert npy to RGB image
    print(bg_name)
    tmp = np.load(bg_path + bg_name)
    tmp = tmp.reshape(3, 1024, 1024)
    tmp = np.transpose(tmp, (1, 2, 0))
    bg = Image.fromarray(np.uint8(tmp))

    bg.save(out_path2 + bg_name + '.png', "PNG")

