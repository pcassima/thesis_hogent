"""
Stable version of the shape and colour detection.
This script uses a webcam connected to the computer and detects the three primary colours.
"""

############################################# Imports ##############################################

import time
import math

import cv2
import imutils
import numpy as np

from message import print_message

######################################### Global variables #########################################

__author__ = 'P. Cassiman'
__version__ = '1.5.0'

THRESHOLD_VALUE = 90
EDGE_LOWER_VALUE = 25
EDGE_UPPER_VALUE = 145

PERIMETER_LOWER_BOUND = 80
PERIMETER_UPPER_BOUND = 800

MAIN_FRAME_RESOLUTION = (960, 720)
SECONDARY_FRAME_RESOLUTION = (720, 540)

SAVE_FRAMES = False

NOT_SAVED = False
COUNT = 0

# Finish line variables
FL_X1 = 1075
FL_X2 = 1150

FL_Y1 = 70
FL_Y2 = 280

finish_line_1 = (FL_X1, FL_Y1)
finish_line_2 = (FL_X2, FL_Y2)

Finish_colour = (0, 0, 255)
FINISHED = False

lap_times = []
start_time = time.time()
lap = 0

############################################# Classes ##############################################

############################################ Functions #############################################


def name_colour(pixel_colour):
    """
    Function to find and name to colour of a given pixel.
    The colour is given in a tuple in BGR format.

    Arguments:
        pixel_colour {tuple} -- The colour in BGR format.

    Returns:
        int -- The name of the colour.
    """

    blue = pixel_colour[0]
    green = pixel_colour[1]
    red = pixel_colour[2]
    c_name = ''
    if blue > 250 and green > 250 and red > 250:
        c_name = 'white'
    elif blue < 50 and green < 50 and red < 50:
        c_name = 'black'
    elif blue > green and blue > red:
        c_name = 'blue'
    elif green > blue and green > red:
        c_name = 'green'
    elif red > blue and red > green:
        c_name = 'red'

    return c_name


def finished():
    global lap_times
    global start_time
    global lap
    max_laps = 3
    lap += 1
    if (lap <= max_laps+1):
        if lap == 1:
            lap_times = []
            start_time = time.time()
            print()
            print("Starting times")
        else:
            lap_time = time.time() - start_time
            if lap_time >= 5:
                start_time = time.time()

                # print("Crossed finish line!")
                print("lap: {}, lap time: {}".format(lap-1, lap_time))
                lap_times.append(lap_time)
            else:
                lap -= 1
    if lap == max_laps+1:
        print('Finished')
        average = sum(lap_times) / len(lap_times)
        fastest = min(lap_times)
        print("Average time: {}, record:{}".format(average, fastest))
        print()
        lap = 0


def print_message():
    # Variables for the message
    message_width = 120
    message_1 = "Vision system for linefollowers"
    message_2 = "Based on OpenCV"
    message_3 = "Written by P. Cassiman"

    # Clearing the screen
    print()
    print()
    # Starting with the border around the message
    print("#" * message_width)
    print("#" + " "*(message_width - 2) + "#")

    print(create_line(message_width, message_1))
    print(create_line(message_width, message_2))
    print(create_line(message_width, ""))
    print(create_line(message_width, message_3))

    # Ending with the border around the screen
    print("#" + " "*(message_width - 2) + "#")
    print("#" * message_width)
    # Adding more whitespace at the end
    print()
    print()


def create_line(width, message):
    line = ""
    line += "#"
    space = (width-2-len(message)) / 2
    space_left = int(math.floor(space))
    space_right = int(math.ceil(space))

    line += " " * space_left
    line += message
    line += " " * space_right
    line += "#"
    return line

############################################### Main ###############################################


if __name__ == "__main__":

    print_message()
    print("Starting vision")

    print("Creating capture object")
    # Enable the video capture on channel 0
    CAP = cv2.VideoCapture(0)

    print("Setting video resolution")
    # Set the capture resolution, works best with 4:3 aspect ratio.
    CAP.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    CAP.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print("Setting and locking video exposure")
    # Set the exposure of the camera
    CAP.set(cv2.CAP_PROP_EXPOSURE, -2)

    print("Creating result window")
    # Create a window to show the results
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    # Set the window to a 4:3 aspect ratio
    cv2.resizeWindow("frame", MAIN_FRAME_RESOLUTION)

    print("Creating threshold window")
    # Create a window to show the results
    cv2.namedWindow("threshold", cv2.WINDOW_NORMAL)
    # Set the window to a 4:3 aspect ratio
    cv2.resizeWindow("threshold", SECONDARY_FRAME_RESOLUTION)

    print("Creating canny edge window")
    # Create a window to show the results
    cv2.namedWindow("edged", cv2.WINDOW_NORMAL)
    # Set the window to a 4:3 aspect ratio
    cv2.resizeWindow("edged", SECONDARY_FRAME_RESOLUTION)

    # time.sleep(1)

    print("Setting font")
    # Chose the font to be used
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    TXT_COLOUR = (0, 255, 255)

    # As long as the window is opened keep running.
    # This allows the windows close button ('X') to be functional.
    print("Starting main loop")
    print()
    print()
    while (cv2.getWindowProperty('frame', 0) or
           cv2.getWindowProperty('canny', 0) or
           cv2.getWindowProperty('threshold', 0)) >= 0:

        # Read a frame from the webcam.
        _, FRAME = CAP.read()
        if SAVE_FRAMES:
            # Create a copy of the frame
            INPUT_FRAME = FRAME.copy()
        FRAME_COPY = FRAME.copy()
        # Fill the sides with white rectangles
        # Left side of the screen
        cv2.rectangle(FRAME_COPY, (0, 0), (150, 1200), (255, 255, 255), -1)
        # Bottom of the screen
        cv2.rectangle(FRAME_COPY, (0, 1100), (1600, 1200), (255, 255, 255), -1)
        # Right side of the screen
        cv2.rectangle(FRAME_COPY, (1560, 0), (1600, 1200), (255, 255, 255), -1)
        # top of the screen
        cv2.rectangle(FRAME_COPY, (0, 0), (1600, 78), (255, 255, 255), -1)
        # Covering the black square on the track.
        cv2.rectangle(FRAME_COPY, (0, 1200), (400, 800), (255, 255, 255), -1)


        # convert the image to greyscale.
        GRAY = cv2.cvtColor(FRAME_COPY, cv2.COLOR_BGR2GRAY)
        # Use a gaussian blur to reduce noise in the image.
        KERNEL = (9, 9)
        GRAY = cv2.GaussianBlur(GRAY, KERNEL, 0)

        # use a binary threshold on the image.
        _, THRESHOLD = cv2.threshold(GRAY, 85, 255, cv2.THRESH_BINARY)

        if SAVE_FRAMES:
            # Create a colour copy of the threshold image
            THRESHOLD_COPY = cv2.cvtColor(THRESHOLD, cv2.COLOR_GRAY2BGR)

        # Detect the edges in the image.
        EDGED = cv2.Canny(THRESHOLD, 25, 145)
        # Reduce noise on the detected edges
        # EDGED = cv2.GaussianBlur(EDGED, (3, 3), 0)

        if SAVE_FRAMES:
            # Create a colour copy of the edge frame
            EDGED_COPY = cv2.cvtColor(EDGED, cv2.COLOR_GRAY2BGR)

        # Find the contours in the image
        CONTOURS = cv2.findContours(
            EDGED.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Get the contours (to deal with different versions of OpenCV)
        CNTS = imutils.grab_contours(CONTOURS)

        for c in CNTS:
            # Approximate the contour.
            PERIMETER = cv2.arcLength(c, True)

            if PERIMETER_LOWER_BOUND <= PERIMETER <= PERIMETER_UPPER_BOUND:
                # Approximate the shape based on the perimeter (with a margin; here 3%)
                approx = cv2.approxPolyDP(c, 0.03 * PERIMETER, True)
                # Draw the contour.
                if len(approx) == 3:
                    # Triangles.
                    M = cv2.moments(c)
                    if M['m00'] != 0:
                        # Extract the centre of the triangle coordinates
                        cX = int(M['m10'] / M['m00'])
                        cY = int(M['m01'] / M['m00'])
                        # Name the colour of the triangle
                        colour = FRAME[cY, cX]
                        colour_name = name_colour(colour)
                        # If the triangle is red
                        if colour_name == 'red':
                            # Create a bounding rectangle for the triangle
                            (x, y, w, h) = cv2.boundingRect(approx)
                            # Calculate the aspect ratio of the bounding box
                            ar = w / float(h)
                            # Our triangles are half a square (diagonally) use this to further filter
                            # out noise.
                            if 0.45 <= ar <= 2.05:
                                # Draw the contour on the frame
                                cv2.drawContours(FRAME, [c], -1, (0, 0, 255), 2)
                                # Write text on the resulting frame
                                cv2.putText(FRAME, 'Car', (cX-16, cY-16), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, TXT_COLOUR, 2)
                                # TODO: Implement lap times
                                cv2.putText(FRAME, 'Lap time', (cX - 16, cY + 16),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                                # Draw the bounding box on the edged frame
                                cv2.rectangle(EDGED_COPY, (x-8, y-8),
                                            (x+w+8, y+h+8), (0, 0, 255), 2)
                                # Draw the bounding box on the threshold frame
                                cv2.rectangle(THRESHOLD_COPY, (x-8, y-8),
                                            (x+w+8, y+h+8), (0, 0, 255), 2)

                                # Check for a finish line crossing
                                if (FL_X1 <= cX <= FL_X2) and (FL_Y1 <= cY <= FL_Y2):
                                    Finish_colour = (0, 255, 0)
                                    if not FINISHED:
                                        finished()
                                        FINISHED = True
                                else:
                                    Finish_colour = (0, 0, 255)
                                    FINISHED = False

                # elif len(approx) == 4:
                #     # squares and rectangles.
                #     M = cv2.moments(c)
                #     if M['m00'] != 0:
                #         cX = int(M['m10'] / M['m00'])
                #         cY = int(M['m01'] / M['m00'])
                #         colour = FRAME[cY, cX]
                #         colour_name = name_colour(colour)
                #         if colour_name == 'black':
                #             (x, y, w, h) = cv2.boundingRect(approx)
                #             ar = w / float(h)
                #             cv2.drawContours(FRAME, [c], -1, (0, 0, 255), 3)
                #             if 0.85 <= ar <= 1.15:
                #                 cv2.putText(FRAME, 'Square', (cX-24, cY-16), cv2.FONT_HERSHEY_SIMPLEX,
                #                             1, TXT_COLOUR, 2)
                #             else:
                #                 cv2.putText(FRAME, 'Rectangle', (cX - 24, cY - 16),
                #                             cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                #             cv2.putText(FRAME, colour_name, (cX - 16, cY + 16),
                #                         cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                else:
                    # Do something
                    pass

        cv2.rectangle(FRAME, finish_line_1, finish_line_2, Finish_colour, 3)
        cv2.putText(FRAME, 'FINISH', (FL_X1 - 32, FL_Y2 + 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, Finish_colour, 2)

        # Draw the parametres on the screen
        cv2.rectangle(FRAME, (0, 0), (300, 100), (255, 255, 255), -1)
        cv2.putText(FRAME, 'parameter 1:', (2, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 2)
        cv2.putText(FRAME, 'parameter 2:', (2, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 2)
        cv2.putText(FRAME, 'parameter 3:', (2, 72),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 2)

        # Put the title on canny edge detection
        cv2.rectangle(EDGED_COPY, (0, 0), (450, 50), (255, 255, 255), -1)
        cv2.putText(EDGED_COPY, 'Canny edge detection', (4, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 0), 2)

        # Put the title on threshold
        cv2.rectangle(THRESHOLD_COPY, (0, 0), (350, 50), (255, 255, 255), -1)
        cv2.putText(THRESHOLD_COPY, 'Binary threshold', (4, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 0), 2)

        cv2.imshow('frame', FRAME)
        cv2.imshow('threshold', THRESHOLD)
        cv2.imshow('edged', EDGED)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

        if SAVE_FRAMES:
            COUNT += 1

            if COUNT == 100:
                print('saving frames')
                NOT_SAVED = True

            if NOT_SAVED:
                # Save the input
                cv2.imwrite('input.png', INPUT_FRAME)
                # Save the result
                cv2.imwrite('result.png', FRAME)
                # Save the threshold image
                cv2.imwrite('threshold.png', THRESHOLD_COPY)
                # Save the canny edge detection result
                cv2.imwrite('canny.png', EDGED_COPY)
            print('saved frames')
            NOT_SAVED = False

    CAP.release()
    cv2.destroyAllWindows()
