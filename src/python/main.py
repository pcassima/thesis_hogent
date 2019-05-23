"""
Stable version of the shape and colour detection.
This script uses a web-cam connected to the computer and detects the three primary colours.
"""

# TODO: Use a class to avoid having to use the global statement

# ------------------------------------------- Imports ----------------------------------------------

import sys
import time

import math

try:
    import cv2
    import imutils
    import paho.mqtt.client as mqtt
except ImportError as e:
    print("Required modules not found")
    print(e)
    sys.exit()

# import numpy as np

# --------------------------------------- Global variables -----------------------------------------

__author__ = "P. Cassiman"
__version__ = '1.5.0'

# Vision variables are placed here for easy tuning.
# These should be changed; currently they are global variables (not preferred).

THRESHOLD_VALUE = 90
EDGE_LOWER_VALUE = 25
EDGE_UPPER_VALUE = 145

PERIMETER_LOWER_BOUND = 80
PERIMETER_UPPER_BOUND = 400

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

FINISH_LINE_1 = (FL_X1, FL_Y1)
FINISH_LINE_2 = (FL_X2, FL_Y2)

FINISH_LINE_COLOUR = (0, 0, 255)
FINISHED = False

LAP_TIMES = []
START_TIME = time.time()
CURRENT_LAP = 0

broker_address = '192.168.1.5'


# ------------------------------------------- Classes ----------------------------------------------

class Finish(object):
    """
    * To implement
    """
    # TODO: implement finish line class, to avoid using global variables.


class WebCam(cv2.VideoCapture):
    """
    WebCam class to act and deal with usb webcams. Class is an extension on the OpenCV VideoCapture class.
    """

    def __init__(self, channel: int = 0, resolution: tuple = (1440, 1080), exposure: int = -2, framerate: int = 40):
        # Call the super class to generate a video capture object.
        super(WebCam, self).__init__(channel)
        # Set the capture resolution, works best with 4:3 aspect ratio.
        self.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        # Set the exposure of the camera
        self.set(cv2.CAP_PROP_EXPOSURE, exposure)
        # Set the framerate on the webcam.
        self.set(cv2.CAP_PROP_FPS, framerate)

    def adjust_exposure(self, target: int = 127):
        """
        This method will read 5 frames and calculate the brightness from each.
        The brightness is averaged out between the 5 frames and used to adjust
        the exposure of the webcam.
        The desired exposure (target) has a margin, as the webcam's exposure
        can only be adjusted in increments. This is to avoid having the
        exposure bounce between two values.
        """
        while True:
            brightness = 0
            for i in range(5):
                # Read 5 frames and take the brightness from those.
                _, frame = self.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness += cv2.mean(frame)[0]
            # Average out the brightness
            brightness /= 5
            # If the brightness is not within a certain margin from the target adjust the exposure.
            if not (target - 32) < brightness < (target + 32):
                if brightness < target:
                    exposure = self.get(cv2.CAP_PROP_EXPOSURE)
                    if exposure == -1:
                        break
                    self.set(cv2.CAP_PROP_EXPOSURE, exposure + 1)
                elif target < brightness:
                    exposure = self.get(cv2.CAP_PROP_EXPOSURE)
                    if exposure == -15:
                        break
                    self.set(cv2.CAP_PROP_EXPOSURE, (exposure - 1))
                else:
                    break
            else:
                break

        # Return to the main program
        return


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


def finished():
    """
    Function triggered when the car crosses the finish line.

    """
    # !Should not be here
    # Access the global variables.
    global LAP_TIMES
    global START_TIME
    global CURRENT_LAP
    # Set the maximum amount of laps.
    max_laps = 3
    # Increment the current lap.
    CURRENT_LAP += 1
    # If the current lap is less then the maximum amount of allowed laps.
    if CURRENT_LAP <= max_laps + 1:
        # If it's the first lap, start the timer.
        if CURRENT_LAP == 1:
            LAP_TIMES = []
            START_TIME = time.time()
            print()
            print("Starting times")
        else:
            # During the other laps, calculate the lap time.
            lap_time = time.time() - START_TIME
            # If the lap time is longer than 5 seconds we can proceed.
            # This is done to filter out glitches in the vision system.
            if lap_time >= 5:
                # Set a new start time.
                START_TIME = time.time()
                # print the time to the terminal
                # TODO: add functionality to add lap time to the screen.
                print("lap: {}, lap time: {}".format(CURRENT_LAP - 1, lap_time))
                # Add the lap time to the list of lap times for later reference.
                LAP_TIMES.append(lap_time)
            else:
                # If the lap isn't longer than five seconds, undo the lap increment.
                CURRENT_LAP -= 1
    # If the current lap is the maximum (or last) lap.
    if CURRENT_LAP == max_laps + 1:
        # Disable controls to the car.
        order_66()
        # Print finished to the terminal.
        print('Finished')
        # Calculate the average and fastest lap times.
        average = sum(LAP_TIMES) / len(LAP_TIMES)
        fastest = min(LAP_TIMES)
        # Print the results to the terminal.
        print("Average time: {}, record:{}".format(average, fastest))
        print()
        # Reset the current lap
        CURRENT_LAP = 0

    # Return to the main program
    return


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


def mask_sides(window):
    """
    Function to mask off the side of the screen. Since the field of view for the camera is larger than the board,
    the 'overflow' is masked so that it's ignored by the rest of the program.
    """
    # Fill the sides with white rectangles
    # Left side of the screen
    cv2.rectangle(window, (0, 0), (150, 1200), (255, 255, 255), -1)
    # Bottom of the screen
    cv2.rectangle(window, (0, 1100), (1600, 1200), (255, 255, 255), -1)
    # Right side of the screen
    cv2.rectangle(window, (1560, 0), (1600, 1200), (255, 255, 255), -1)
    # top of the screen
    cv2.rectangle(window, (0, 0), (1600, 78), (255, 255, 255), -1)
    # Covering the black square on the track.
    cv2.rectangle(window, (0, 1200), (400, 800), (255, 255, 255), -1)

    # Return to the main program
    return


def order_66():
    """
    Command to disable all controls to the car.
    """
    # Create a delay here before sending the command
    # Not the right way to do it, but oh well...
    time.sleep(0.5)
    print("Creating mqtt object")
    mqtt_client = mqtt.Client()

    # setting the mqtt broker address and port
    print("Connecting to broker")
    try:
        mqtt_client.connect(broker_address, 1881)

        # starting the mqtt loop
        print("Starting mqtt loop")
        mqtt_client.loop_start()

        # making the array to send
        arr = bytearray([20, 61, 0, 0, 11, 0, 0, 0])

        arr[0] = 20  # stop the car
        print("Sending message to the car")
        mqtt_client.publish("vroom", arr)

        arr[0] = 21  # reset the lights
        print("Sending message to the lights")
        mqtt_client.publish("vroom", arr)

        arr[0] = 60  # disable the controls
        print("Sending message to the controls")
        mqtt_client.publish("vroom", arr)
        print("Stop the mqtt loop")
        mqtt_client.loop_stop(force=False)
        print("Disconnect from the loop")
        mqtt_client.disconnect()
    except ConnectionRefusedError:
        print("Connection was refused by server")
        print("Can the server be found on the same network?")


# --------------------------------------------- Main -----------------------------------------------


if __name__ == "__main__":

    print_message()
    print("Starting vision")

    print("Number of CPU's: {}".format(cv2.getNumberOfCPUs()))
    print("Number of threads: {}".format(cv2.getNumThreads()))

    print("Creating capture object")
    # Creating a webcam object.
    CAP = WebCam(channel=1)

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
    TXT_COLOUR = (0, 150, 150)

    print("Performing exposure adjust")
    CAP.adjust_exposure(150)

    # As long as the window is opened keep running.
    # This allows the windows close button ('X') to be functional.
    print("Starting main loop")
    print()
    print()
    # while (cv2.getWindowProperty('frame', 0) or
    #        cv2.getWindowProperty('canny', 0) or
    #        cv2.getWindowProperty('threshold', 0)) >= 0:
    count = 0
    while True:

        # Set the finish line colour.
        FINISH_LINE_COLOUR = (0, 0, 255)
        # Set the finished variable to false.
        FINISHED = False

        # Read a frame from the web-cam.
        if count == 150:
            # Every 150 frames (or 5 seconds) perform auto adjust for the exposure
            count = 0
            CAP.adjust_exposure(150)
        _, FRAME = CAP.read()
        count += 1
        # Create a copy of the frame
        INPUT_FRAME = FRAME.copy()

        # Mask the sides of the screen
        mask_sides(INPUT_FRAME)
        # convert the image to greyscale.
        GRAY = cv2.cvtColor(INPUT_FRAME, cv2.COLOR_BGR2GRAY)
        # Use a gaussian blur to reduce noise in the image.
        KERNEL = (9, 9)
        GRAY = cv2.GaussianBlur(GRAY, KERNEL, 0)

        # use a binary threshold on the image.
        _, THRESHOLD = cv2.threshold(GRAY, 85, 255, cv2.THRESH_BINARY)
        # Create a colour copy of the threshold image
        THRESHOLD_COPY = cv2.cvtColor(THRESHOLD, cv2.COLOR_GRAY2BGR)

        # Detect the edges in the image.
        EDGED = cv2.Canny(THRESHOLD, 25, 145)
        # Reduce noise on the detected edges.
        # EDGED = cv2.GaussianBlur(EDGED, (3, 3), 0)
        # Create a colour copy of the edge frame.
        EDGED_COPY = cv2.cvtColor(EDGED, cv2.COLOR_GRAY2BGR)

        # Find the contours in the image.
        CONTOURS = cv2.findContours(EDGED.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Get the contours (to deal with different versions of OpenCV).
        CNTS = imutils.grab_contours(CONTOURS)

        for c in CNTS:
            # Approximate the contour.
            PERIMETER = cv2.arcLength(c, True)

            if PERIMETER_LOWER_BOUND <= PERIMETER <= PERIMETER_UPPER_BOUND:
                # Approximate the shape based on the perimeter (with a margin; here 3%).
                # If two adjacent points in the contour have a distance that is less than 3% of the perimeter, they
                # will be treated as a single point.
                approx = cv2.approxPolyDP(c, 0.03 * PERIMETER, True)
                # Draw the contour.
                if len(approx) == 3:
                    # Triangles.
                    M = cv2.moments(c)
                    if M['m00'] != 0:
                        # Extract the centre of the triangle coordinates.
                        cX = int(M['m10'] / M['m00'])
                        cY = int(M['m01'] / M['m00'])
                        # Name the colour of the triangle.
                        colour = FRAME[cY, cX]
                        colour_name = name_colour(colour)
                        # If the triangle is red.
                        if colour_name == 'red':
                            # Create a bounding rectangle for the triangle.
                            (x, y, w, h) = cv2.boundingRect(approx)
                            # Calculate the aspect ratio of the bounding box.
                            ar = w / float(h)
                            # Our triangles are half a square (diagonally) and have a bounding rectangle with an
                            # aspect ratio of 0.5 to 2 use this to further filter out noise.
                            if 0.45 <= ar <= 2.05:
                                # Draw the contour on the frame.
                                cv2.drawContours(FRAME, [c], -1, (0, 0, 255), 2)
                                # Write text on the resulting frame.
                                cv2.putText(FRAME, 'Car', (cX - 16, cY - 16),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)
                                # TODO: Implement lap times
                                if CURRENT_LAP != 0:
                                    current_time = time.time() - START_TIME
                                    float_time, int_time = math.modf(current_time)
                                    time_str = "{}:{:03d}".format(int(int_time), int(float_time * 1000))
                                    cv2.putText(FRAME, time_str, (cX - 16, cY + 16),
                                                cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                                # Draw the bounding box on the edged frame.
                                cv2.rectangle(EDGED_COPY, (x - 8, y - 8), (x + w + 8, y + h + 8), (0, 0, 255), 2)
                                # Draw the bounding box on the threshold frame.
                                cv2.rectangle(THRESHOLD_COPY, (x - 8, y - 8), (x + w + 8, y + h + 8), (0, 0, 255), 2)

                                # Check for a finish line crossing.
                                if (FL_X1 <= cX <= FL_X2) and (FL_Y1 <= cY <= FL_Y2):
                                    FINISH_LINE_COLOUR = (0, 150, 0)
                                    if not FINISHED:
                                        finished()
                                        FINISHED = True

                elif len(approx) == 4:
                    # squares and rectangles.
                    pass

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
                #                 cv2.putText(FRAME, 'Square', (cX-24, cY-16),
                #                             cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)
                #             else:
                #                 cv2.putText(FRAME, 'Rectangle', (cX - 24, cY - 16),
                #                             cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                #             cv2.putText(FRAME, colour_name, (cX - 16, cY + 16),
                #                         cv2.FONT_HERSHEY_SIMPLEX, 1, TXT_COLOUR, 2)

                else:
                    # Do something for other shapes.
                    pass

        cv2.rectangle(FRAME, FINISH_LINE_1, FINISH_LINE_2, FINISH_LINE_COLOUR, 3)
        cv2.putText(FRAME, 'FINISH', (FL_X1 - 32, FL_Y2 + 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, FINISH_LINE_COLOUR, 2)

        # Draw the parameters on the screen.
        cv2.rectangle(FRAME, (0, 0), (300, 100), (255, 255, 255), -1)
        cv2.putText(FRAME, 'Threshold: {}'.format(THRESHOLD_VALUE), (2, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 2)
        cv2.putText(FRAME, 'Canny lower: {}'.format(EDGE_LOWER_VALUE), (2, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 2)
        cv2.putText(FRAME, 'Canny upper: {}'.format(EDGE_UPPER_VALUE), (2, 72),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 2)

        # Put the title on canny edge detection.
        cv2.rectangle(EDGED_COPY, (0, 0), (450, 50), (255, 255, 255), -1)
        cv2.putText(EDGED_COPY, 'Canny edge detection', (4, 32), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 0), 2)

        # Put the title on threshold.
        cv2.rectangle(THRESHOLD_COPY, (0, 0), (350, 50), (255, 255, 255), -1)
        cv2.putText(THRESHOLD_COPY, 'Binary threshold', (4, 32), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 0), 2)

        # Show the resulting frames.
        cv2.imshow('frame', FRAME)
        cv2.imshow('threshold', THRESHOLD_COPY)
        cv2.imshow('edged', EDGED_COPY)

        if cv2.waitKey(1) & 0xff == ord('q'):
            # If the "q" is pressed, close to program by breaking the loop.
            break

        if SAVE_FRAMES:
            COUNT += 1

            if COUNT == 100:
                print('saving frames')
                NOT_SAVED = True

            if NOT_SAVED:
                # Save the input.
                cv2.imwrite('input.png', INPUT_FRAME)
                # Save the result.
                cv2.imwrite('result.png', FRAME)
                # Save the threshold image.
                cv2.imwrite('threshold.png', THRESHOLD_COPY)
                # Save the canny edge detection result.
                cv2.imwrite('canny.png', EDGED_COPY)
                print('saved frames')
                NOT_SAVED = False

    # Release the capture object.
    CAP.release()
    # Destroy all windows and finish the program.
    cv2.destroyAllWindows()
