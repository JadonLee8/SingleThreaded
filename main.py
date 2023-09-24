import heapq
import cv2 as cv
import numpy as np
import sys

img = cv.imread("img.png", cv.IMREAD_GRAYSCALE)

# the smaller side of the image fed to the program will be the radius of the circle
radius = min(img.shape)
print(radius)

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

cv.imshow("pinned image", pinned_image)

# calculate priority queues for each pin

# NOTE: will use a linked list in the future when I consider the line against previous lines, not just the previous image
priority_queues = []
current_a_pin = 0
for pin_from in pins:
    priority_queue = []
    # TODO: compute cost of line
    # compute the difference between an image of dimensions radius x radius with a line between pins drawn on it and the cropped image
    current_b_pin = 0
    for pin_to in pins:
        line_image = np.zeros((radius, radius), dtype=np.uint8)
        line_image = cv.line(line_image, (pins[current_a_pin]), (pins[current_b_pin]), 255, 1)
        COMPUTED_COST = np.sum(np.abs(np.subtract(line_image, cropped_img)))
        heapq.heappush(priority_queue, (COMPUTED_COST, pin_to)) # TODO: replace computeed cost with actual cost (how far off the line is from the pixels in the base image)
        current_b_pin += 1
        del line_image
    priority_queues.append(priority_queue)
    del priority_queue
    current_a_pin += 1
    print(current_a_pin/num_pins*100, "% \done of priority queues")

final_image = np.zeros((radius, radius), dtype=np.uint8)
num_lines = 4000
start_pin = 0
for i in range(num_lines):
    this_pins_pq = priority_queues[start_pin]
    destination = heapq.heappop(this_pins_pq)
    final_image = cv.line(final_image, pins[start_pin], destination[1], 255, 1)
    start_pin = pins.index(destination[1])
    print(i/num_lines*100, "% \done of final image")

cv.imshow("final image", final_image)

# wait until window is closed to stop GUI
cv.waitKey(0)

# clear memory and destroy GUI
cv.destroyAllWindows()
