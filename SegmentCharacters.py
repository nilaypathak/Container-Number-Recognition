import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import DetectPlate

# The invert was done so as to convert the black pixel to white pixel and vice versa
license_plate = DetectPlate.plate_like_objects[0]

labelled_plate = measure.label(license_plate)

fig, ax1 = plt.subplots(1,figsize=(18, 10))
ax1.imshow(license_plate, cmap="gray")
# the next two lines is based on the assumptions that the width of
# a license plate should be between 5% and 15% of the license plate,
# and height should be between 35% and 60%
# this will eliminate some
character_dimensions = (0.001*license_plate.shape[0], 0.90*license_plate.shape[0], 0.5*license_plate.shape[1], 1.1*license_plate.shape[1])
print(license_plate.shape)
min_height, max_height, min_width, max_width = character_dimensions

characters = []
counter=0
column_list = []
for regions in regionprops(labelled_plate):
    y0, x0, y1, x1 = regions.bbox
    region_height = y1 - y0
    region_width = x1 - x0

    if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
        roi = license_plate[max(0,y0-3):min(y1+6,license_plate.shape[0]), 0:license_plate.shape[1]]

        # draw a red bordered rectangle over the character.
        rect_border = patches.Rectangle((0, max(0,y0-3)), license_plate.shape[1] - 0, y1 - y0+5, edgecolor="red",
                                       linewidth=2, fill=False)
        ax1.add_patch(rect_border)

        # resize the characters to 20X20 and then append each character into the characters list
        resized_char = resize(roi, (20, 20))
        characters.append(resized_char)

    # this is just to keep track of the arrangement of the characters
    column_list.append(x0)
# print(characters)
plt.show()