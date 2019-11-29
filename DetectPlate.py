
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import cv2
import imutils
from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
plate_like_objects = []
filename = './container1.jpg'
img = cv2.imread(filename, 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
# img = cv2.bilateralFilter(img,9,75,75)
area = img.shape[0]*img.shape[1]
ret, labels = cv2.connectedComponents(img)
fig, (ax1) = plt.subplots(1,figsize=(18, 16), dpi= 80)
ax1.imshow(img)
regions=[]
centroids=[]
for region in regionprops(labels):
    min_row, min_col, max_row, max_col = region.bbox
#     print(min_row)
    region_height = max_row - min_row
    region_width = max_col - min_col
    if region.area < 30 or region.area>0.01*area:
        #if the region is so small then it's likely not a license plate
        continue
    if(region_height>0.7*region_width and region_height<5*region_width):
        
        rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
        ax1.add_patch(rectBorder)
        regions.append(region)
        centroids.append((min_col+region_width/2,min_row+region_height/2))
img_len=img.shape[0]
for i in range(len(regions)):
    cen1_x=centroids[i][0]
    num_vertical=0
    req_reqions=[]
    for j in range(len(regions)):
        cen2_x=centroids[j][0]
        if(abs(cen2_x-cen1_x)<0.01*img_len):
            num_vertical=num_vertical+1
            req_reqions.append(regions[j])
    if(num_vertical>5):
        break
fig, (ax1) = plt.subplots(1,figsize=(18, 16), dpi= 80)
ax1.imshow(img)

bbs=[]
for region in req_reqions:
    min_row, min_col, max_row, max_col = region.bbox
    rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
    ax1.add_patch(rectBorder)
    bbs.append(region.bbox)
# min_col=min(bbs[:][1])
import numpy as np
bbs=np.array(bbs)
min_row = min(bbs[:,0])
max_row = max(bbs[:,2])
min_col = min(bbs[:,1])
max_col = max(bbs[:,3])
rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="blue",
                                       linewidth=2, fill=False)
ax1.add_patch(rectBorder)
plate_like_objects.append(img[min_row:max_row,min_col:max_col])