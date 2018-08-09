
root_path = r'C:/Data/glass/'
blended_path = root_path + r'blended_data/'
#in_path = blended_path + r'glass_removed_w_Poisson/'
#in_path2 = blended_path + r'face/'
in_path = blended_path + r'mask/'
in_path2 = blended_path + r'glass/'

#out_path2 = blended_path + r'face/'
out_path = blended_path + r'mask_crop640x320/'
out_path2 = blended_path + r'glass_crop640x320/'


from PIL import Image
import os 
import math
import time
import random
import numpy as np

os.makedirs(out_path, exist_ok=True)
os.makedirs(out_path2, exist_ok=True)


in_files = os.listdir(in_path)
for im_name in in_files:
    print(im_name)
    im = Image.open(in_path + im_name)
    cropped = im.crop((190,344,830,664))
    cropped.save(out_path + im_name)
    #im = Image.open(in_path2 + im_name[:-5]+'B.png')
    im = Image.open(in_path2 + im_name[:-5]+'A.png')
    cropped = im.crop((190,344,830,664))
    #cropped.save(out_path2 + im_name[:-5]+'B.png')
    cropped.save(out_path2 + im_name[:-5]+'A.png')
