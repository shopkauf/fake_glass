
in_path = 'C:/Data/glass/composite_Poisson_cropped640x320/'
in_path2 = 'C:/Data/glass/faces_Poisson_cropped640x320/'
out_path = 'C:/Data/glass/composite_Poisson_cropped320x160/'
out_path2 = 'C:/Data/glass/faces_Poisson_cropped320x160/'

#in_path = 'C:/Data/glass/composite_Poisson_cropped640x320/unseen_test/'
#in_path2 = 'C:/Data/glass/faces_Poisson_cropped640x320/unseen_test/'
#out_path = 'C:/Data/glass/composite_Poisson_cropped320x160/unseen_test/'
#out_path2 = 'C:/Data/glass/faces_Poisson_cropped320x160/unseen_test/'


from PIL import Image
import os 
import math
import time
import random
import numpy as np


in_files = os.listdir(in_path)
for im_name in in_files:
    print(im_name)
    im = Image.open(in_path + im_name)
    cropped = im.resize((320, 160), Image.LANCZOS)
    cropped.save(out_path + im_name)
    im = Image.open(in_path2 + im_name[:-5]+'B.png')
    cropped = im.resize((320, 160), Image.LANCZOS)
    cropped.save(out_path2 + im_name[:-5]+'B.png')
