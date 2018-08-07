##Copyright 2017 Adobe Systems Inc.
##
##Licensed under the Apache License, Version 2.0 (the "License");
##you may not use this file except in compliance with the License.
##You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
##Unless required by applicable law or agreed to in writing, software
##distributed under the License is distributed on an "AS IS" BASIS,
##WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##See the License for the specific language governing permissions and
##limitations under the License.


##############################################################
#path to GLASSES
fg_path = r'C:/Data/glass/source_data/foreground/'
#fg_path = r'C:/tmp/foreground/unseen_test/'

#path to provided alpha mattes
#a_path = r'C:/tmp/alpha/'
#a_path = r'C:/Data/glass/alpha/unseen_test/'
a_path = r'C:/Data/glass/source_data/alpha/'

#Path to FACES
#bg_path = r'F:/celebA/celebA-HQ/'
#bg_path = r'F:/celebA/testing/'
#bg_path = r'c:/tmp/faces_checked/'
bg_path = r'c:/Data/glass/source_data/faces_checked_v2/'

#Path to folder where you want the composited images to go
#out_path = 'C:/tmp/composite/'
#out_path2 = 'C:/tmp/faces/'
out_path = 'C:/Data/glass/generated_data/composite_Poisson/'
out_path2 = 'C:/Data/glass/generated_data/faces_Poisson/'

#parameters
NUM_BGS = 40         ## TRAINING: for each FG image (eyeglass), use how many BG (face) images. This number cannot be larger than existing BG images. Must CHECK!
#NUM_BGS = 6           ## TESTING UNSEEN DATA

## images already with glasses (and other artifacts), these are bad!!!: 52, 132, 138, 164, 167, 168, 175, 179, 193, 210, 252, 259, 286, 292, 295

##############################################################

from PIL import Image
import os 
import math
import time
import random
import numpy as np
import Poisson_v2
import copy ## for deep copy

def composite4(fg, bg, a, shift_hori, shift_vert):
    
    bbox = fg.size
    w = bbox[0]
    h = bbox[1]

    fg_list = fg.load()
    bg_list = bg.load()
    a_list = a.load()

    for y in range(h):
        for x in range (w):
            alpha = a_list[x,y] / 255

            if alpha >= 1:
                r = int(fg_list[x,y][0])
                g = int(fg_list[x,y][1])
                b = int(fg_list[x,y][2])
                bg_list[x+shift_hori, y+shift_vert] = (r, g, b, 255)
            elif alpha > 0:
                r = int(alpha * fg_list[x,y][0] + (1-alpha) * bg_list[x + shift_hori, y + shift_vert][0])
                g = int(alpha * fg_list[x,y][1] + (1-alpha) * bg_list[x + shift_hori, y + shift_vert][1])
                b = int(alpha * fg_list[x,y][2] + (1-alpha) * bg_list[x + shift_hori, y + shift_vert][2])
                bg_list[x + shift_hori, y + shift_vert] = (r, g, b, 255)

    return bg


fg_files = os.listdir(fg_path)
a_files = os.listdir(a_path)
bg_files = os.listdir(bg_path)
bg_iter = iter(bg_files)
fcount = 0

#from skimage import data, io
#img_Poisson_src = io.imread(r'C:/Data/glass/Poisson_template/white.png').astype(np.float64)

for im_name in fg_files:

    try:
        im = Image.open(fg_path + im_name)
    except:
        continue

    a = Image.open(a_path + im_name).convert('L') ## convert alpha image to grayscale

    bbox = im.size
    w = bbox[0]
    h = bbox[1]
    
    if im.mode != 'RGB' and im.mode != 'RGBA':
        im = im.convert('RGB')



    bcount = 0 
    for i in range(NUM_BGS):
    #for bg_name in bg_files:

        out_ffname = out_path + str(fcount) + '_A.png'
        if os.path.isfile(out_ffname):
            bcount += 1
            fcount += 1
            continue

        try:
            bg_name = next(bg_iter)
        except StopIteration:
            bg_iter = iter(bg_files)
            bg_name = next(bg_iter)

        ## convert npy to RGB image
        print(bg_name)
        try:
            bg = Image.open(bg_path + bg_name)
        except:
            continue

        #bg = bg.resize((312,312), Image.BICUBIC)


        #bg = Image.open(bg_path1 + bg_name)
        #if bg.mode != 'RGB':
        #    bg = bg.convert('RGB')

        ## update w and h
        bbox = im.size
        w = bbox[0]
        h = bbox[1]
        bg_bbox = bg.size
        bw = bg_bbox[0]
        bh = bg_bbox[1]

        factor = 2.0 * random.randint(95,101) / 100
        a = a.resize((math.ceil(w*factor), math.ceil(h*factor)), Image.BICUBIC)
        a = np.array(a)
        a[:, -1] = 0
        a[:, 0] = 0
        a[-1, :] = 0
        a[0, :] = 0
        a = Image.fromarray(a)
        im_resized = im.resize((math.ceil(w*factor), math.ceil(h*factor)), Image.BICUBIC)

        shift_hori = math.ceil(512 - w*factor/2)
        shift_vert = math.ceil(519 - h*factor/2)
        bg.save(out_path2 + str(fcount) + '_B.png', "PNG")

        out = composite4(im_resized, bg, a, shift_hori, shift_vert)

        img_Poisson_src = 0 * np.array(a)
        #img_mask, img_src, offset_adj = Poisson_v2.create_mask(np.array(a).astype(np.float64), np.array(out), img_Poisson_src, offset=offset)
        offset_adj = (shift_vert, shift_hori)
        poisson_mask = copy.deepcopy(np.array(a).astype(np.float64))
        poisson_mask[poisson_mask > 0] = 1
        poisson_mask[poisson_mask == 0] = 0
        # Necessary code from Internet: "remove edge from the mask so that we don't have to check the edge condition"
        poisson_mask[:, -1] = 0
        poisson_mask[:, 0] = 0
        poisson_mask[-1, :] = 0
        poisson_mask[0, :] = 0

        img_pro = Poisson_v2.poisson_blend(poisson_mask, img_Poisson_src, np.array(out), method='normal', offset_adj=offset_adj)
        img_pro = Image.fromarray(img_pro)

    #out.save(out_path + im_name[:len(im_name)-4] + '_' + bg_name[:len(bg_name)-4] + '_R.png', "PNG")
        img_pro.save(out_ffname, "PNG")
        bcount += 1
        fcount += 1
