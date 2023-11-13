# computerVisionCar
This project contains all code necessary to control a Lego car through object tracking through a computer camera

To implement the project, the two following scripts are needed:

objectTracking.py:
  This script uses Open CV to detect motion of a red object within a video feed. It then sends the x components of the object to an MQTT broker which the Pico will read in the 
  other script to move the Lego car. 

  Packages needed to run this script: cv2, paho-mqtt, time, and numpy.

INSERT OTHER SCRIPT AND DESCRIPTION HERE.
