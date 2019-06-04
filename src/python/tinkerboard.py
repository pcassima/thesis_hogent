"""
Vision program designed to run on the Asus Tinkerboard.
The script is using the Raspberry Pi camera module V2.
Mostly this script is the same as the main.py script.
"""

# Imports

import sys
import time

import math

try:
    import cv2
    import imutils
    import paho.mqtt.client as mqtt
    # import numpy as np

except ImportError as e:
    print("Required modules not found")
    print e
    sys.exit()

# Global variables

__author__ = "P. Cassiman"
__version__ = "0.1.0"

# Vision parametres are placed here for convience.

THRESHOLD_VALUE = 90
EDGE_LOWER_VALUE = 25
EDGE_UPPER_VALUE = 145

# Classes

class RpiCameraModule(cv2.VideoCapture):
    """
    Class to use the Raspberry Pi camera module on the Asus Tinker Board.
    """

    _channel = "rkcamsrc io-mode=4 isp-mode=2A tuning-xml-path=/etc/cam_iq/IMX219.xml ! video/x-raw,format=NV12,width=640,height=480 ! videoconvert ! appsink"
