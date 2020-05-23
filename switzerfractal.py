#
# switzerfractal.py - vexillological shitpost
# --------------------------------------------
# Switzerland, but in Switzerland, but in Switzerland, but in Switzerland but in Switzerland, but in Switzerland
# but in Switzerland, but in Switzerland, but in Switzerland, but in Switzerland, but in Switzerland... by nat
#
# Uses the Pillow library for image generation
# Inspired by https://www.reddit.com/r/vexillologycirclejerk/comments/gnm9q8/flag_of_switzestland/
#
# That was a stupid idea
#
# Usage:
#  $ python3 switzerfractal.py [output image path] [flag width] [depth]
#

import sys
from time import time
from PIL import Image

output_path = sys.argv[1]
flag_width = int(sys.argv[2], 10)
max_depth = int(sys.argv[3], 10)

img = Image.new("RGB", (flag_width, flag_width))

#
# See https://en.wikipedia.org/wiki/Flag_of_Switzerland#/media/File:Swiss_Flag_Specifications.svg
# for specs of the flag
#

background_color = (255, 0, 0)
foreground_color = (255, 255, 255)

normalized_square_size = 13/32

# Normalized coordinates of all the sub-squares, ie. targets of next flags

#sub_squares = [
#    (9.5/32 - normalized_square_size/2, 1/2 - normalized_square_size/2),  # left
#    (1/2 - normalized_square_size/2, 9.5/32 - normalized_square_size/2),  # top
#    (22.5/32 - normalized_square_size/2, 1/2 - normalized_square_size/2), # right
#    (1/2 - normalized_square_size/2, 22.5/32 - normalized_square_size/2), # bottom
#    (1/2 - normalized_square_size/2, 1/2 - normalized_square_size/2),     # center
#]

sub_squares = [
    (0, 0), (19/32, 0),
    (0, 19/32), (19/32, 19/32)
]

stripes = [
    [(6/32, 13/32), (26/32, 19/32)],
    [(13/32, 6/32), (19/32, 26/32)]
]

expected_passes = 0
for i in range(max_depth + 1):
    expected_passes += len(sub_squares) ** i

passes_done_count = 1

def rectangle(x1, y1, x2, y2, color):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if x >= flag_width or y >= flag_width:
                continue
            img.putpixel((x, y), color)

def switzerfractal(x, y, w, h, depth, invert_colors=False):
    
    invert_colors = False
    
    global passes_done_count
    
    if w == 0 or h == 0:
        return
    
    print("Pass %d/%d (%d,%d) (%d,%d) depth %d" % (passes_done_count, expected_passes, x, y, w, h, depth)) 
    passes_done_count += 1
    
    bg = background_color if not invert_colors else foreground_color
    fg = foreground_color if not invert_colors else background_color
    
    # Draw the background
    rectangle(x, y, w - 1, h - 1, bg)
    
    # Draw the stripes
    for stripe in stripes:
        x1, y1 = stripe[0]
        x2, y2 = stripe[1]
        
        x1 = x + x1 * w
        y1 = y + y1 * h
        x2 = x + x2 * w
        y2 = y + y2 * h
        
        rectangle(x1, y1, x2, y2, fg)
    
    if depth >= max_depth:
        return
    
    for subsquare in sub_squares:
        sx, sy = subsquare
        sx = x + sx * w
        sy = y + sy * h
        switzerfractal(
            sx, sy,
            normalized_square_size * w,
            normalized_square_size * h,
            depth + 1,
            not invert_colors
        )

print("Starting calculation for image (%d, %d) - expected passes - %d, depth %d" % (flag_width, flag_width, expected_passes, max_depth))
start = time()
switzerfractal(0, 0, flag_width, flag_width, 0, False)
end = time()
print("Finished calculation for image (%d, %d) - expected passes - %d, depth %d" % (flag_width, flag_width, expected_passes, max_depth))
print(" Work time: ", (end - start))
img.save(output_path)
