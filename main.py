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


# calculate priority queues for each pin
# NOTE: will use a linked list in the future when I consider the line against previous lines, not just the previous image
priority_queues = []
current_a_pin = 0
for pin_from in pins:
    priority_queue = []
    current_b_pin = 0
    for pin_to in pins:
        if (current_a_pin == current_b_pin):
            current_b_pin += 1
            continue
        # black on white lines
        # line_image = np.full((radius, radius), 255, dtype=np.uint8)
        copy = np.copy(cropped_img)
        line_image = cv.line(copy, (pins[current_a_pin]), (pins[current_b_pin]), 0, 1)
        COMPUTED_COST = np.sum(cv.absdiff(line_image, cropped_img))/np.linalg.norm(np.array(pins[current_a_pin]) - np.array(pins[current_b_pin]))
        heapq.heappush(priority_queue, (COMPUTED_COST, pin_to)) 
        current_b_pin += 1
        del line_image
        del copy
    priority_queues.append(priority_queue)
    del priority_queue
    current_a_pin += 1
    sys.stdout.write('\r')
    sys.stdout.write(f'Computing line costs... {(int)(current_a_pin/len(pins)*100)}%')
    sys.stdout.flush()

final_image = np.full((radius, radius), 255, dtype=np.uint8)
num_lines = 1300
start_pin = 0
for i in range(num_lines):
    this_pins_pq = priority_queues[start_pin]
    # TODO: don't just pop. Pop and see if it's different enough from what we have already drawn
    destination = heapq.heappop(this_pins_pq)
    # uniqueness = np.sum(np.abs(np.subtract(final_image, cv.line(np.zeros((radius,radius), dtype=np.uint8), pins[start_pin], destination[1], 255, 1))))
    # if uniqueness < 1000:
    #     continue
    final_image = cv.line(final_image, pins[start_pin], destination[1], 0, 1)
    start_pin = pins.index(destination[1])

    sys.stdout.write('\r')
    sys.stdout.write(f'Printing image... {(int)(i/num_lines*100)}%')
    sys.stdout.flush()

cv.imwrite("image_pins.png", pinned_image)
cv.imwrite("final.png", final_image)

# wait until window is closed to stop GUI
cv.waitKey(0)

# clear memory and destroy GUI
cv.destroyAllWindows()
