import heapq
import sys
import cv2 as cv
import numpy as np

img = cv.imread("eye.jpg", cv.IMREAD_GRAYSCALE)

# the smaller side of the image fed to the program will be the radius of the circle
radius = min(img.shape)

# crop the image to a square with side length equal to the radius.
cropped_img = img[(int)(img.shape[0]/2 - radius/2):(int)(img.shape[0]/2 + radius/2), (int)(img.shape[1]/2 - radius/2):(int)(img.shape[1]/2 + radius/2)]

# the amount of 'nails' to be used in the image
num_pins = 100
pins = []

# create a circle of pins around the image represented as dots
for i in range(num_pins):
    angle = (2*np.pi/num_pins)*i
    x = (int)((radius-3)/2 * np.cos(angle) + radius/2)
    y = (int)((radius-3)/2 * np.sin(angle) + radius/2)
    pins.append((x,y))
    pinned_image = cv.circle(cropped_img, (x-1,y-1), 3, 255, -1)

NUM_LINES = 4000

line_image = np.full((radius, radius), 255, dtype=np.uint8)

for i in range(NUM_LINES):
    sys.stdout.write('\r')
    sys.stdout.write(f'Printing image... {(int)(i/NUM_LINES*100)}%')
    sys.stdout.flush()
    # choose a random pin to start the line
    start = np.random.choice(num_pins)
    for i in range(num_pins):
        if i is not start:
            line_image_copy = np.copy(line_image)
            line_image_copy = cv.line(line_image_copy, pins[start], pins[i], 0, 1)
            cost = np.abs
 


# sys.stdout.write('\r')
# sys.stdout.write(f'Printing image... {(int)(i/num_lines*100)}%')
# sys.stdout.flush()

cv.imwrite("image_pins.png", pinned_image)
cv.imwrite("final.png", final_image)

# wait until window is closed to stop GUI
cv.waitKey(0)

# clear memory and destroy GUI
cv.destroyAllWindows()
