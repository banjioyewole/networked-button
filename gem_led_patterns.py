from sense_hat import SenseHat
import threading
import time
import sys

# sense = SenseHat()
# sense = None

o = [255,127,0]
y = [125,125,0]
a = y #amarillo if you catch my drift; this is so we can change the home color when we do a long press
#y = [255, 255, 0]
g = [0,255,0]
# b = [0,0,255]
# r = [255,0,0]
r = y
b = y
i = [75,0,130]
v = [159,0,255]
e = [0,0,0]
p = [236, 64, 121]
u = [64, 64, 64]
w = [255, 255, 255]

image = [
e,e,e,e,e,e,e,e,
e,e,e,r,r,e,e,e,
e,r,r,o,o,r,r,e,
r,o,o,y,y,o,o,r,
o,y,y,g,g,y,y,o,
y,g,g,b,b,g,g,y,
b,b,b,i,i,b,b,b,
b,i,i,v,v,i,i,b
]

home_1 = [
e,e,e,a,a,e,e,e,
e,e,a,a,a,e,a,e,
e,a,a,a,a,a,a,e,
a,a,a,a,a,a,a,a,
a,a,a,a,a,a,a,a,
e,a,a,a,a,a,a,e,
e,a,a,a,a,a,a,e,
e,a,a,a,a,a,a,e,
]

home_white = [
e,e,e,w,w,e,e,e,
e,e,w,w,w,e,w,e,
e,w,w,w,w,w,w,e,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
e,w,w,w,w,w,w,e,
e,w,w,w,w,w,w,e,
e,w,w,w,w,w,w,e,
]

heat = [
e,e,e,e,e,e,e,e,
e,e,e,r,r,e,e,e,
e,e,r,r,r,r,e,e,
e,r,r,r,r,r,r,e,
r,r,r,e,e,r,r,r,
r,r,e,e,e,e,r,r,
r,r,e,e,e,e,r,r,
e,e,e,e,e,e,e,e,
]

heat_white = [
e,e,e,e,e,e,e,e,
e,e,e,w,w,e,e,e,
e,e,w,w,w,w,e,e,
e,w,w,w,w,w,w,e,
w,w,w,e,e,w,w,w,
w,w,e,e,e,e,w,w,
w,w,e,e,e,e,w,w,
e,e,e,e,e,e,e,e,
]

cool_white = [
e,e,e,e,e,e,e,e,
w,w,e,e,e,e,w,w,
w,w,e,e,e,e,w,w,
w,w,w,e,e,w,w,w,
e,w,w,w,w,w,w,e,
e,e,w,w,w,w,e,e,
e,e,e,w,w,e,e,e,
e,e,e,e,e,e,e,e,
]

cool = [
e,e,e,e,e,e,e,e,
b,b,e,e,e,e,b,b,
b,b,e,e,e,e,b,b,
b,b,b,e,e,b,b,b,
e,b,b,b,b,b,b,e,
e,e,b,b,b,b,e,e,
e,e,e,b,b,e,e,e,
e,e,e,e,e,e,e,e,
]

gong_1 = [
u,u,u,u,u,u,u,u,
u,e,u,e,e,e,u,e,
u,e,e,p,p,p,e,e,
u,e,p,p,p,p,p,e,
u,e,p,p,p,p,p,e,
u,e,p,p,p,p,p,e,
u,e,e,p,p,p,e,e,
u,e,e,e,e,e,e,e,
]

gong_2 = [
e,e,p,p,p,p,e,e,
e,p,p,p,p,p,p,e,
p,p,p,p,p,p,p,p,
p,p,p,p,p,p,p,p,
p,p,p,p,p,p,p,p,
p,p,p,p,p,p,p,p,
e,p,p,p,p,p,p,e,
e,e,p,p,p,p,e,e,
]

gong_white = [
e,e,w,w,w,w,e,e,
e,w,w,w,w,w,w,e,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
e,w,w,w,w,w,w,e,
e,e,w,w,w,w,e,e,
]

dark = [
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
]

error = [
y,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
e,e,e,e,e,e,e,e,
]



def display_image(image, scroll_up, fades_out, apply_gradient):
    if(scroll_up is not None):
        scroll(image, scroll_up)
    else:
        # time.sleep(0.25)
        sense.set_pixels(image)
        time.sleep(0.5)
    if(apply_gradient):
        homekit_gradient()
    if(fades_out):
        fade_out()


def homekit_gradient():

    base_decr = 5
    decr = 0
    pixel = 0

    for row in range(0,8):
        decr += base_decr
        for col in range(0,8):
            pixel = sense.get_pixel(col, row)
            if(pixel[1] >=decr):
                pixel[1] -= decr
            sense.set_pixel(col, row, pixel[0], pixel[1], pixel[2])
            #print(pixel)


def scroll(image, is_scroll_up):
    base_inc = .015
    fade_base_inc = .015
    was_0 = False
    row_offset_0_index = 6 if is_scroll_up else -6
    while(was_0 == False):
        was_0 = row_offset_0_index == 0
        for row in range(0,8):
            if(row + row_offset_0_index > 7 or row + row_offset_0_index < 0):
                continue;
            for col in range(0,8):
                    pixel = image[8*row + col]
                    #if(pixel[1] >=decr):
                        #    pixel[1] -= decr

                    sense.set_pixel(col, row_offset_0_index+row, pixel[0], pixel[1], pixel[2])
                #print(pixel)
        row_offset_0_index = row_offset_0_index + ((-1) if is_scroll_up else 1)
        time.sleep(base_inc)
        base_inc+=fade_base_inc

def fade_out():
    base_inc = .025
    fade_base_inc = .0125
    time.sleep(.05)
    max_subpixel = 255
    while(max_subpixel > 1):
        max_subpixel = 0
        for row in range(0,8):
            for col in range(0,8):
                pixel = sense.get_pixel(col, row)
                for int in range(0, len(pixel)):
                    pixel[int] /=6
                    pixel[int] *=5
                    max_subpixel = max(max_subpixel, pixel[int])
                sense.set_pixel(col, row, pixel[0], pixel[1], pixel[2])
        time.sleep(base_inc)
        base_inc+=fade_base_inc


class LuminousClass:

    def __init__(self):
        self.sense = SenseHat()
        global sense
        sense = self.sense

    def quick_homekit(self):
        display = home_1 if not self.is_white else home_white
        display_image(display, True, True, True)

    def quick_up(self):
        display = heat if not self.is_white else heat_white
        display_image(display, True, True, True)

    def quick_down(self):
        display = cool if not self.is_white else cool_white
        display_image(display, False, True, True)

    def quick_gong(self):
        display = gong_2 if not self.is_white else gong_white
        display_image(display, None, True, True)

    def illumination_handler(self, direction, type):
        self.sense.low_light = False
        self.is_white = type == 2
        if direction == "up":
          self.quick_up()
        elif direction == "down":
          self.quick_down()
        elif direction == "left":
          self.quick_homekit()
        elif direction == "right":
          self.quick_homekit()
        elif direction == "core":
          self.quick_gong()




# myLumen = LuminousClass()
# myLumen.quick_up()

#RUNNABLE
#
# display_image(dark, None, False, False)
#
#
# if(len(sys.argv) > 1):
#     arg = sys.argv[1].lower()
#     if(arg == "heat"):
#         display_image(heat, True, True, True)
#     elif(arg == "cool"):
#         display_image(cool, False, True, True)
#     elif(arg == "home"):
#         display_image(home_1, True, True, True)
#     elif(arg == "gong"):
#         display_image(gong_2, None, True, True)
#     elif(arg == "dark"):
#         display_image(dark, None, False, False)
#     else:
#         display_image(error, None, False, True)
# else:
#     display_image(error, None, False, True)
# #scroll(cool, False)
# #sense.set_pixels(home_1)
# sense.low_light = False
# #time.sleep(2)
# #homekit_gradient()
#
# #scroll(dark)
# #fade_out()
