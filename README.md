# computerVisionCar
This project contains all code necessary to control a Lego car through object tracking through a computer camera

To implement the project, the two following scripts are needed:

objectTracking.py:
  This script uses Open CV to detect motion of a red object within a video feed. It then sends the x components of the object to an MQTT broker which the Pico will read in the 
  other script to move the Lego car. 

  Packages needed to run this script: cv2, paho-mqtt, time, and numpy.

BLEPico.py
  This script reads the MQTT data from the object tracking script, then sends a control command over Bluetooth to the Spike Prime.

  Packages needed to run this script: bluetooth, time, struct, network, ubinascii, mqtt, and the custom BLE library (see below)

CarStateMachine.py
  This script is a state machine for the control of the Spike Prime based car. States are controlled by reading messages sent over Bluetooth by the Pico which correspond to Forward, Left, Right, and Stop.

  Packages needed to run this script: time, hub, motor, uasyncio, BLELibrary

BLELibrary.py
  This is a custom library assembled by Chris Rogers for simple BLE control.
  
