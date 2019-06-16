"""
Library file to hold all camera classes, as of now the webcam and Raspberry Pi camera module.

Copyright (C) 2019, Pieter-Jan Cassiman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# ------------------------------------------- Imports ----------------------------------------------

import sys
from typing import Union

try:
    import cv2
except ImportError as e:
    print('OpenCV not found')
    print(e)
    sys.exit()
# --------------------------------------- Global variables -----------------------------------------

__author__ = 'P. Cassiman'
__version__ = '0.1.0'

# ------------------------------------------- Classes ----------------------------------------------


class Camera(cv2.VideoCapture):
    """
    Class to extend the VideoCapture object of OpenCV. This class makes it easier to implement
    cameras. By isolating a lot of the settings and commands related to the camera into this class.
    A lot of the settings have common default values, so that they don't need to be specified.
    """

    def __init__(self, channel: int = 0, resolution: tuple = (1280, 720),
                 exposure: int = -2, framerate: int = 30) -> cv2.VideoCapture:
        # Call the super class to generate a video capture object.
        super(Camera, self).__init__(channel)
        # Set all the required parameters for the camera.
        self._set_params(resolution, exposure, framerate)

    def _set_params(self, resolution: tuple,
                    exposure: int, framerate: int) -> None:
        """
        Classmethod to set the various paramters for the camera.

        Arguments:
            resolution {tuple} -- Resolution for the camera
            exposure {int} -- Exposure value for the camera
            framerate {int} -- The framerate of the camera

        Returns:
            None
        """
        # Set the capture resolution, works best with 4:3 aspect ratio.
        self.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        # Set the exposure of the camera
        self.set(cv2.CAP_PROP_EXPOSURE, exposure)
        # Set the framerate on the webcam.
        self.set(cv2.CAP_PROP_FPS, framerate)

        return

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


class WebCam(Camera):
    """
    WebCam class to act and deal with usb webcams.
    This class is an extension on the OpenCV VideoCapture class.
    """

    def __init__(self, channel: int = 0, resolution: tuple = (1440, 1080),
                 exposure: int = -2, framerate: int = 40) -> cv2.VideoCapture:
        # Call the super class to generate a video capture object.
        super(WebCam, self).__init__(channel)
        # Set all the required parameters for the camera.
        self._set_params(resolution, exposure, framerate)


class TinkerCamera(Camera):
    """
    Class to use the Raspberry Pi camera module V2 on the Asus Tinker Board.
    The V2 camera module uses the IMX219 8-Mp sensor.
    """

    _channel = "rkcamsrc io-mode=4 isp-mode=2A tuning-xml-path=/etc/cam_iq/IMX219.xml ! video/x-raw,format=NV12, \
        width = 640, height = 480!videoconvert!appsink "

    def __init__(self, channel: Union[int, str] = None, resolution: tuple = (1440, 1080),
                 exposure: int = -2, framerate: int = 40) -> cv2.VideoCapture:

        if isinstance(channel, (int, str)):
            # If no channel is defined use the default channel for the camera on the Tinker Board
            super(TinkerCamera, self).__init__(channel)
        else:
            # If a channel is given use that one.
            super(TinkerCamera, self).__init__(self._channel)
        # Set all the required parameters for the camera.
        self._set_params(resolution, exposure, framerate)

# ------------------------------------------ Functions ---------------------------------------------


# --------------------------------------------- Main -----------------------------------------------

if __name__ == '__main__':
    pass
