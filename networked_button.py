# from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import RPi.GPIO as GPIO
# from time import sleep
# from time import time
import time
# from gem_led_patterns import *
import requests
# sense = SenseHat()

# e = (0, 0, 0)
# w = (255, 255, 255)

# sense.clear()

# senseWrapper = LuminousClass()
# myLumen.sense.clear()
# senseWrapper.quick_up()

# The arcade-button exposes only the single press event through Homekit, handling the double press and long press with http request to other devices on the network


# http://yourHomebridgeServerIp:webhook_port/?accessoryId=theAccessoryIdToTrigger&state=NEWSTATE
print("Did Start Networked-Button")
base_url = "http://localhost:"
webhook_port = "7278"

base_opal_url = "http://192.168.1.62:"
opal_port = "42069"


last_direction = ""
last_type = -1
last_action = None
last_press_time = time.time() - 1

single_press = 0
double_press = 1
long_press = 2

consumed_event = False
is_pressed = False
last_press_time = time.time()



def preform_action(direction, press_type):
    global last_direction
    global last_type
    print("Made Network Request with direction " + direction + " and press type " + ("LONG" if press_type == 2 else "SINGLE"))
    direction = "core" if direction == "middle" else direction
    threading.Thread(target=senseWrapper.illumination_handler, args=(direction,press_type,)).start()
    if last_direction == direction and last_type == press_type:
        return
    last_direction = direction
    last_type = press_type
    formed_base_url = base_url + webhook_port
    r = requests.get(formed_base_url, params={ "accessoryId" : "sapphire_joystick" , "buttonName": direction.capitalize(), "event" : press_type })


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)


def did_double_press():
    global consumed_event
    consumed_event = True
    print("double press")

def did_long_press():
    global consumed_event
    consumed_event = True
    print("did long press")

def did_single_press():
    print("did single press")

while True:
    time.sleep(0.05)
    if GPIO.input(3) == GPIO.LOW:
        #double press & long press
        if not is_pressed and (time.time() - last_press_time) < 0.5:
            did_double_press()
            time.sleep(1)
        if is_pressed and (time.time() - last_press_time) > 0.8 and (time.time() - last_press_time) < 1.0:
            did_long_press()
            time.sleep(0.2)
        if not is_pressed:
            last_press_time = time.time()
        is_pressed = True

    elif GPIO.input(3) == GPIO.HIGH:

        if time.time() - last_press_time > 0.5 and time.time() - last_press_time < 0.55:
            if not consumed_event:
                did_single_press()
                # is_pressed = False

            elif consumed_event:
                consumed_event = False
                # is_pressed = False

        is_pressed = False



#
# while True:
#     event = senseWrapper.sense.stick.wait_for_event()
#
#     # Check if the joystick was pressed
#     if event.action == ACTION_PRESSED:
#         last_action = ACTION_PRESSED
#
#
#     elif event.action == ACTION_HELD:
#         if last_action == ACTION_HELD:
#             continue
#         last_action = ACTION_HELD
#         preform_action(event.direction, long_press)
#
#     elif event.action == ACTION_RELEASED:
#         if last_action == ACTION_HELD:
#             last_action = ACTION_RELEASED
#             continue
#         preform_action(event.direction, single_press)
