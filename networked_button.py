from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
from time import time
from gem_led_patterns import *
import requests
sense = SenseHat()

e = (0, 0, 0)
w = (255, 255, 255)

sense.clear()

# http://yourHomebridgeServerIp:webhook_port/?accessoryId=theAccessoryIdToTrigger&state=NEWSTATE
print("Did Start Networked-Button")
base_url = "http://localhost:"
webhook_port = "7278"

last_direction = ""
# last_press_time = time()

single_press = 0
double_press = 1
long_press = 2


def preform_action(direction, press_type):
    print("called preform_action")
    print("direction " + direction)
    print("press_type" + str(press_type))
    direction = "core" if direction == "middle" else direction
    if len(last_direction) > 0:
        pass
    else:
        return
    formed_base_url = base_url + webhook_port
    r = requests.get(formed_base_url, params={ "accessoryId" : "sapphire_joystick" , "buttonName": direction.capitalize(), "event" : press_type })

while True:

  for event in sense.stick.get_events():
    print("did get event")
    # Check if the joystick was pressed
    if event.action == ACTION_PRESSED:
      # Check which direction
      last_direction = event.direction
      preform_action(event.direction, single_press)

      if event.direction == "up":
        # sense.show_letter("U")      # Up arrow
        quick_up()
      elif event.direction == "down":
        # sense.show_letter("D")      # Down arrow
        quick_down()
      elif event.direction == "left":
        # sense.show_letter("L")      # Left arrow
        quick_homekit()
      elif event.direction == "right":
        # sense.show_letter("R")      # Right arrow
        quick_homekit()
    elif event.direction == "middle":
        # sense.show_letter("C")      # Enter key
        quick_gong()

    # elif event.action == ACTION_HELD:
        # preform_action(event.direction, long_press)

    # elif event.action == ACTION_RELEASED:
    #     if time() - last_press_time < 1 :
    #         continue
    #     else:
    #         preform_action(event.direction, single_press)


      # Wait a while and then clear the screen
    # sleep(0.5)
    # sense.clear()
