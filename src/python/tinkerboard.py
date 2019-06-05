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
    else:
        c_name = 'gray'

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

    # frame counter for the auto-exposure:
    frame_counter = 0

    print("Starting main loop")
    # As long as the window is opened keep running.
    # This allows the windows close button ('X') to be functional.
    while cv2.getWindowProperty('frame', 0) >= 0:

        # Check the need for auto exposure adjustment
        if frame_counter % 120 == 0:
            # Every 120 frames (or ~4 seconds) perform auto adjust for the exposure
            # Here the auto exposure is dissabled
            # CAP.adjust_exposure(150)
            pass

         # Read a frame from the web-cam.
        _, FRAME = CAP.read()
        frame_counter += 1

        # Convert the frame the grayscale
        GRAY = cv2.cvtColor(FRAME, cv2.COLOR_BGR2GRAY)

        # Use a gaussian blur to reduce noise in the image.
        KERNEL = (9, 9)
        GRAY = cv2.GaussianBlur(GRAY, KERNEL, 0)

        # use a binary threshold on the image.
        _, THRESHOLD = cv2.threshold(GRAY, 85, 255, cv2.THRESH_BINARY)

        # Detect the edges in the image.
        EDGED = cv2.Canny(THRESHOLD, 25, 145)
        # Reduce noise on the detected edges.
        EDGED = cv2.GaussianBlur(EDGED, (3, 3), 0)

        # Find the contours in the image.
        CONTOURS = cv2.findContours(EDGED.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Get the contours (to deal with different versions of OpenCV).
        CNTS = imutils.grab_contours(CONTOURS)

        for c in CNTS:
            # Approximate the contour.
            PERIMETER = cv2.arcLength(c, True)

            if PERIMETER_LOWER_BOUND <= PERIMETER <= PERIMETER_UPPER_BOUND:
                # Approximate the shape based on the perimeter (with a margin; here 3%).
                # If two adjacent points in the contour have a distance that is less than 3% of the
                # perimeter, they will be treated as a single point.
                approx = cv2.approxPolyDP(c, 0.03 * PERIMETER, True)

                M = cv2.moments(c)
                # If the shape has a valid centre, proceed.
                if M['m00'] != 0:
                    # Extract the coordinates of the shape centre.
                    # The centre of mass is used as the centre of the shape. When using the normal
                    # centre it could give problems where the centre is located outside of the
                    # shape. By using the centre of mass this problem is greatly reduced (however)
                    # Not avoided completely.
                    cX = int(M['m10'] / M['m00'])
                    cY = int(M['m01'] / M['m00'])
                    # Name the colour of the shape.
                    colour_name = name_colour(FRAME[cY, cX])

                    # Create a bounding rectangle for the triangle.
                    (x, y, w, h) = cv2.boundingRect(approx)
                    # Calculate the aspect ratio of the bounding box.
                    ar = w / float(h)
                    if len(approx) >= 3:
                        # Draw the contour on the frame.
                        cv2.drawContours(FRAME, [c], -1, (0, 0, 255), 2)
                        # Add the name of the colour.
                        cv2.putText(FRAME, colour_name, (cX - 16, cY + 16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                    # Determine the shape
                    if len(approx) == 3:
                        # Triangles
                        cv2.putText(FRAME, 'Triangle', (cX - 16, cY - 16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                    elif len(approx) == 4:
                        # Squares, rectangles etc
                        # If the width and height are with 15% of eachother the shape is determined
                        # as a square.
                        if 0.85 <= ar <= 1.15:
                            cv2.putText(FRAME, 'Square', (cX-24, cY-16),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                        # Other wise the shape is determined to be a rectangle.
                        else:
                            cv2.putText(FRAME, 'Rectangle', (cX - 24, cY - 16),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                    elif len(approx) == 5:
                        # Pentagons
                        cv2.putText(FRAME, 'Pentagon', (cX - 16, cY - 16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                    elif len(approx) == 6:
                        # Hexagons
                        cv2.putText(FRAME, 'Hexagon', (cX - 16, cY - 16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                    elif len(approx) == 7:
                        # Heptagons
                        cv2.putText(FRAME, 'Heptagon', (cX - 16, cY - 16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                    elif len(approx) == 8:
                        # Octagons
                        cv2.putText(FRAME, 'Octagon', (cX - 16, cY - 16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                    else:
                        # Circles (or close enough)
                        cv2.putText(FRAME, 'Circle', (cX - 16, cY - 16),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

        # Put the title on threshold.
        cv2.rectangle(FRAME, (0, 0), (350, 50), (255, 255, 255), -1)
        cv2.putText(FRAME, 'Results', (4, 32), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 0), 2)

        # Show the resulting frames.
        cv2.imshow('frame', FRAME)

        if cv2.waitKey(1) & 0xff == ord('q'):
            # If the "q" is pressed, close to program by breaking the loop.
            break

    # Release the capture object.
    CAP.release()
    # Destroy all windows and finish the program.
    cv2.destroyAllWindows()
