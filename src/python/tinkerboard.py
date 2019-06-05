"""
Vision program designed to run on the Asus Tinkerboard.
The script is using the Raspberry Pi camera module V2.
Mostly this script is the same as the main.py script.
"""

# ------------------------------------------- Imports ----------------------------------------------

import sys
import time

import math

from lib.camera import TinkerCamera

try:
    import cv2
    import imutils
    # import paho.mqtt.client as mqtt
    # import numpy as np

except ImportError as e:
    print("Required modules not found")
    print(e)
    sys.exit()

# --------------------------------------- Global variables -----------------------------------------

__author__ = "P. Cassiman"
__version__ = "0.1.0"

# Vision parametres are placed here for convenience.

THRESHOLD_VALUE = 90
EDGE_LOWER_VALUE = 25
EDGE_UPPER_VALUE = 145

PERIMETER_LOWER_BOUND = 80
PERIMETER_UPPER_BOUND = 400

MAIN_FRAME_RESOLUTION = (960, 720)
SECONDARY_FRAME_RESOLUTION = (720, 540)

# ------------------------------------------- Classes ----------------------------------------------


# ------------------------------------------ Functions ---------------------------------------------

def name_colour(pixel_colour: tuple = (0, 0, 0)) -> str:
    """
    Function to find and name to colour of a given pixel.
    The colour is given in a tuple in BGR format.

    Arguments:
        pixel_colour {tuple} -- The colour in BGR format.

    Returns:
        str -- The name of the colour.
    """
    # Split the pixel into three separate variables.
    blue = pixel_colour[0]
    green = pixel_colour[1]
    red = pixel_colour[2]

    # Start with a blank name.
    c_name = ''

    # If all colours are above 250 the colour is white.
    if blue > 250 and green > 250 and red > 250:
        c_name = 'white'
    # If all colours are below 50 the colour is black.
    elif blue < 50 and green < 50 and red < 50:
        c_name = 'black'

    # Extract the other primary colours.
    # TODO: improve the "algorithm" for checking colours.
    elif blue > green and blue > red:
        c_name = 'blue'
    elif green > blue and green > red:
        c_name = 'green'
    elif red > blue and red > green:
        c_name = 'red'

    return c_name


def print_message():
    """
    Will write a simple message to the terminal when the program first starts.
    To show the name and author of the program.
    """
    # Variables for the message.
    message_width = 120
    message_1 = "Vision system for line-followers"
    message_2 = "Based on OpenCV"
    message_3 = "Written by P. Cassiman"

    # Clearing the screen.
    print()
    print()
    # Starting with the border around the message.
    print("#" * message_width)
    print("#" + " " * (message_width - 2) + "#")

    # Call the function to correctly format the message lines.
    print(create_line(message_width, message_1))
    print(create_line(message_width, message_2))
    print(create_line(message_width, ""))
    print(create_line(message_width, message_3))

    # Ending with the border around the screen.
    print("#" + " " * (message_width - 2) + "#")
    print("#" * message_width)
    # Adding more whitespace at the end.
    print()
    print()

    # Return to the main program
    return


def create_line(width: int = 80, message: str = "Hello world!") -> str:
    """
    Will format a string to the given width.
    The line will start and end with a "#".
    The message is centered, the rest of the space is filled with whitespace.

    Keyword Arguments:
        width {int} -- The target width to format. (default: {80})
        message {str} -- The message to be formatted. (default: {"Hello world!"})

    Returns:
        str -- The formatted line as a string.
    """
    # Start with a blank line.
    line = ""
    # Add the first "#" sign.
    line += "#"
    # Calculate the needed whitespace.
    space = (width - 2 - len(message)) / 2
    # The left white space is rounded down and converted to an int.
    space_left = int(math.floor(space))
    # The right white space is rounded up and converted to an int.
    space_right = int(math.ceil(space))

    # Add the left white space.
    line += " " * space_left
    # Add the actual message.
    line += message
    # Add the right whitespace.
    line += " " * space_right
    # Add the closing "#" sign.
    line += "#"
    # Return the line.
    return line


# --------------------------------------------- Main -----------------------------------------------

if __name__ == "__main__":
    print_message()
    print("Starting vision")

    print("Number of CPU's: {}".format(cv2.getNumberOfCPUs()))
    print("Number of threads: {}".format(cv2.getNumThreads()))

    print("Creating capture object")
    # Creating a webcam object.
    CAP = TinkerCamera()

    print("Creating result window")
    # Create a window to show the results
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    # Set the window to a 4:3 aspect ratio
    cv2.resizeWindow("frame", MAIN_FRAME_RESOLUTION)

    # time.sleep(1)

    print("Setting font")
    # Chose the font to be used
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    TXT_COLOUR = (0, 150, 150)

    print("Performing exposure adjust")
    CAP.adjust_exposure(150)

    # As long as the window is opened keep running.
    # This allows the windows close button ('X') to be functional.
    print("Starting main loop")
    print()
    print()

    while cv2.getWindowProperty('frame', 0) >= 0:

        if cv2.waitKey(1) & 0xff == ord('q'):
            # If the "q" is pressed, close to program by breaking the loop.
            break
            
    # Release the capture object.
    CAP.release()
    # Destroy all windows and finish the program.
    cv2.destroyAllWindows()
