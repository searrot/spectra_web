import os 
import numpy as np
import cv2

images = os.listdir('./static/user_images/')
new = cv2.imread(f'./static/user_images/{images[1]}')
last = cv2.imread(f'./static/user_images/{images[0]}')

image = np.array(new)
last = np.array(last)

if np.array_equal(image, last):
    print(1)
