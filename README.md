# Networked-Button

## Visual Experiance
![Button Press and Lights Change](https://github.com/banjioyewole/networked-button/blob/master/networked_button_demo.gif?raw=true)

## Top Level

This project makes network requests based on Joystick movement on the `SenseHAT` and display corresponding patterns on the LED Matrix. 

This is achieved by the included `network_button.py` and `gem_led_patterns.py`, the former handling joystick action parsing and network request and starting the latter with an non-blocking call to the top level `illumination_handler()` method. 

This script is only one half. When paired with the `homebridge-http-switch` homebridge library, you can create a virtual switch that can be activated by the network requests made by `network_button`! Learn more 

This Script makes http request to localhost to get the `homebridge-http-switch` library to activate buttons in HomeKit. The registered URLs correspond to different buttons which can be bound to different scenes within the Home app.

### Links

[Homebridge](https://github.com/homebridge/homebridge) | The foundation for emulating hardware in Homekit!

[`homebridge-http-switch`](https://www.npmjs.com/package/homebridge-http-switch]) | Add http switches to your home today!

Networked-Button requires Python Library [`Requests`](https://github.com/psf/requests)
