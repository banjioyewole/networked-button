import RPi.GPIO as GPIO

import time
import requests

# The arcade-button exposes only the single press event through Homekit, handling the double press and long press with http request to other devices on the network


# http://yourHomebridgeServerIp:webhook_port/?accessoryId=theAccessoryIdToTrigger&state=NEWSTATE
print("Waiting 30 sec to start...")
time.sleep(0)
print("Did Start Networked-Button")

base_url = "http://localhost:"
webhook_port = "8727"

base_opal_url = "http://192.168.1.62:"
opal_port = "42069"


last_direction = ""
last_type = -1
last_action = None
last_press_time = time.time() - 1
invalid_press_time = time.time() - 1
single_press = 0
double_press = 1
long_press = 2

# consumed_event = False
LOW_CONSUMED = False
UNCONSUMED = False

did_press = False


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
# Up is HIGH


def did_double_press():
    did_consume_button_event_in_low_state()
    print("double press")
    formed_base_url = base_url + webhook_port
    r = requests.get(formed_base_url, params={ "accessoryId" : "bigred", "buttonName": "Primary", "event": double_press })

def did_long_press():
    did_consume_button_event_in_low_state()
    print("did long press")
    formed_base_url = base_url + webhook_port
    r = requests.get(formed_base_url, params={ "accessoryId" : "bigred", "buttonName": "Primary", "event": long_press })


def did_single_press():
    print("did single press")
    formed_base_url = base_url + webhook_port
    r = requests.get(formed_base_url, params={ "accessoryId" : "bigred", "buttonName": "Primary", "event": single_press })

def did_consume_button_event_in_low_state():
        global LOW_CONSUMED
        global did_press
        global UNCONSUMED
        global last_press_time
        global invalid_press_time
        LOW_CONSUMED = True
        did_press = False
        UNCONSUMED = False
        last_press_time = invalid_press_time

while True: #DEFAULT BUTTON STATE IS "HIGH"
    time.sleep(0.0025)
    if GPIO.input(3) == GPIO.LOW:
        # print("LOW")
        #double press & long press

        if not LOW_CONSUMED:

            if did_press and UNCONSUMED and (time.time() - last_press_time) < 0.5:
                did_double_press()
                continue
                # time.sleep(1)
            if did_press and not UNCONSUMED and (time.time() - last_press_time) > 0.8 and (time.time() - last_press_time) < 1.0:
                did_long_press()
                continue

            # if did_press and UNCONSUMED and (time.time() - last_press_time) > 0.8 and (time.time() - last_press_time) < 1.0: #notPossible
            #     did_single_press_and_hold()
            #     continue

        #     time.sleep(0.2)
            if not did_press:
                last_press_time = time.time()
                did_press = True

        if LOW_CONSUMED:
            last_press_time = invalid_press_time


    elif GPIO.input(3) == GPIO.HIGH:
        # print("HIGH")
        #
        if LOW_CONSUMED:
            LOW_CONSUMED = False
            continue

        if (time.time() - last_press_time > 0.5) and (time.time() - last_press_time < 0.55):
            # if not consumed_event:
            if did_press:
                did_single_press()
                last_press_time = invalid_press_time
                did_press = False
                UNCONSUMED = False
        else:
            if did_press and (time.time() - last_press_time < 0.5):
                UNCONSUMED = True

        #
        #     elif consumed_event:
        #         consumed_event = False
        #         # is_pressed = False
        #
        # is_pressed = False
