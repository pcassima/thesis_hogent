"""
A implementation of our Protocol 2.0 in python.
The protocol is as follows:
[header][payload][tail]
The header consists of:
[destination][origin][function][channel][payload type][userdata]

The protocol is implemented as a message class with all the require operations as classmethods.

Based on the MQTT protocol designed by J. Sarrazyn.
"""

# TODO: write unittests

############################################# Imports ##############################################

import struct

# import lib.paho.mqtt.client as mqtt

######################################### Global variables #########################################

__author__ = 'P. Cassiman'
__version__ = '0.0.0'

############################################# Classes ##############################################


class Message(object):
    """
    Custom data structure to represent a message according to our protocol.
    """

    # TODO: write docstring.

    # Payload types:
    DATA_CHAR = 10
    DATA_UCHAR = 11
    DATA_INT = 12
    DATA_UINT = 13
    DATA_WORD = 14
    DATA_LONG = 15
    DATA_ULONG = 16
    DATA_FLOAT = 17
    DATA_STRING = 19

    def __init__(self,
                 destination: int = 0,
                 origin: int = 0,
                 function: int = 0,
                 channel: int = 0,
                 payload_type: int = 0,
                 userdata: int = 0):

        # User variables.
        self.destination = destination
        self.origin = origin
        self.function = function
        self.channel = channel
        self.payload_type = payload_type
        self.userdata = userdata

        # Variables used for message construction.
        self.header = bytearray([0, 0, 0, 0, 0, 0])
        self.payload = bytearray()
        self.tail = bytearray([0])

        # Actual message to be sent (or that is received).
        self.message = bytearray()

        # Updating the header to match the given parametres.
        self._update_header()

        # Creating the message.
        self._update_mesage()

    def _update_tail(self):
        """
        Method for implementing different message tails in the future.
        """

        raise NotImplementedError(
            "Different values for the tail are currently not yet supported.")

    def _update_header(self):
        """
        Function used to create the header.
        This function will add all the variables to the header.
        """

        # Adding the destination.
        if isinstance(self.destination, int):

            if self.destination in range(256):

                # When destination passes all tests update the value in the header.
                self.header[0] = self.destination
            else:

                # If the destination is outside of the set range raise a valueError.
                raise ValueError("Destination has to be in [0, 255].")
        else:

            # If destination has to wrong type raise a typeError.
            raise TypeError("Destination has to be int!")

        # Adding the origin.
        if isinstance(self.origin, int):

            if self.origin in range(256):

                # When origin passes all tests update the value in the header.
                self.header[1] = self.origin
            else:

                # If the origin is outside of the set range raise a valueError.
                raise ValueError("Origin has to be in [0, 255].")
        else:

            # If origin has to wrong type raise a typeError.
            raise TypeError("Origin has to be int!")

        # Adding the function.
        if isinstance(self.function, int):

            if self.function in range(256):

                # When function passes all tests update the value in the header.
                self.header[2] = self.function

            else:

                # If the function is outside of the set range raise a valueError.
                raise ValueError("Function has to be in [0, 255].")

        else:

            # If function has to wrong type raise a typeError.
            raise TypeError("Function has to be int!")

        # Adding the channel.
        if isinstance(self.channel, int):

            if self.channel in range(256):

                # When channel passes all tests update the value in the header.
                self.header[3] = self.channel

            else:

                # If the channel is outside of the set range raise a valueError.
                raise ValueError("Channel has to be in [0, 255].")
        else:

            # If channel has to wrong type raise a typeError.
            raise TypeError("Channel has to be int!")

        # Adding the payload type
        if isinstance(self.payload_type, int):

            if self.payload_type in range(256):

                # When payload type passes all tests update the value in the header.
                self.header[4] = self.payload_type
            else:

                # If the payload type is outside of the set range raise a valueError.
                raise ValueError("Payload type has to be in [0, 255].")
        else:

            # If payload type has to wrong type raise a typeError.
            raise TypeError("Payload type has to be int!")

        # Adding the userdata.
        if isinstance(self.userdata, int):

            if self.userdata in range(256):

                # When userdata passes all tests update the value in the header.
                self.header[5] = self.userdata

            else:

                # If the userdata is outside of the set range raise a valueError.
                raise ValueError("Userdata has to be in [0, 255].")
        else:

            # If userdata has to wrong type raise a typeError.
            raise TypeError("Userdata has to be int!")

        return

    def _update_mesage(self):
        """
        This function will update the message variable with the three parts.
        """

        self.message = self.header + self.payload + self.tail

        return

    def _update_payload(self, payload_type, payload):
        """
        Function to set the payload type and payload.
        This function will also call the other required _update methods.

        Arguments:
            payload_type {[type]} -- [description]
            payload {[type]} -- [description]
        """

        # Set the payload type to to the given value.
        self.payload_type = payload_type
        # Update the header
        self._update_header()
        # Update the payload.
        self.payload = payload
        # Update the message.
        self._update_mesage()

    def decode(self):
        """[summary]

        Returns:
            [type] -- [description]
        """

        # TODO: write method docstring

        # Extracting the information from the header.
        self.destination = self.message[0]
        self.origin = self.message[1]
        self.function = self.message[2]
        self.channel = self.message[3]
        self.payload_type = self.message[4]
        self.userdata = self.message[5]

        # Updating the header variable.
        self._update_header()

        # Take the last byte and save it to the tail (while maintaining the bytearray type).
        self.tail = bytearray(self.message[-1])

        # Extracting the payload from the message. (6th byte until the before last).
        self.payload = self.message[5:-1]

        if (self.payload_type == self.DATA_CHAR) or (self.payload_type == self.DATA_STRING):

            # Decode string or character
            return self.payload.decode("utf-8")

        elif self.payload_type == self.DATA_UCHAR:

            # Decode unsigned character
            return struct.unpack("<B", self.payload)

        elif self.payload_type == self.DATA_INT:

            # Decode signed integer
            return struct.unpack("<i", self.payload)

        elif self.payload_type == self.DATA_UINT:

            # Decode unsigned integer
            return struct.unpack("<I", self.payload)

        elif self.payload_type == self.DATA_LONG:

            # Decode signed long
            return struct.unpack("<l", self.payload)

        elif self.payload_type == self.DATA_ULONG:

            # Decode unsigned long
            return struct.unpack("<L", self.payload)

        elif self.payload_type == self.DATA_FLOAT:

            # Decode float.
            return struct.unpack("<f", self.payload)

    def set_message(self, message: bytearray):
        """
        sets the entire message variable.
        this function can be used to set a received message.

        Arguments:
            message {bytearray} -- The message.

        Raises:
            TypeError -- When the message is not a bytearray.
        """

        if isinstance(message, bytearray):
            self.message = message
            return
        else:
            raise TypeError("Message needs to be bytearray")

    def get_message(self):
        """
        Gets the current message.

        Returns:
            bytearray -- The message bytearray.
        """

        return self.message

    def set_destination(self, destination: int):
        """
        Sets the destination for the message.

        Arguments:
            destination {int} -- The destination for the message.

        Raises:
            TypeError -- When the parameter is not an int.
        """

        if isinstance(destination, int):
            self.destination = destination
        else:
            raise TypeError("Expected int for destination.")
        return

    def get_destination(self):
        """
        Gets the current destination of the message.

        Returns:
            int -- Current destination of the message.
        """

        return self.destination

    def set_origin(self, origin: int):
        """
        Sets the origin of the message.

        Arguments:
            origin {int} -- The origin of the message.

        Raises:
            TypeError -- When the parameter is not an int.
        """

        if isinstance(origin, int):
            self.origin = origin
        else:
            raise TypeError("Expected int for origin.")
        return

    def get_origin(self):
        """
        Gets the current origin of the message.

        Returns:
            int -- Current origin of the message.
        """

        return self.origin

    def set_function(self, function: int):
        """
        Sets the function of the message.

        Arguments:
            function {int} -- The function of the message.

        Raises:
            TypeError -- When the parameter is not an int.
        """

        if isinstance(function, int):
            self.function = function
        else:
            raise TypeError("Expected int for function.")
        return

    def get_function(self):
        """
        Gets the current function of the message.

        Returns:
            int -- The function of the message.
        """

        return self.function

    def set_channel(self, channel: int):
        """
        Sets the channel of the message.

        Arguments:
            channel {int} -- The channel of the message.

        Raises:
            TypeError -- When the parameter is not an int.
        """

        if isinstance(channel, int):
            self.channel = channel
        else:
            raise TypeError("Expected int for channel.")
        return

    def get_channel(self):
        """
        Gets the current channel of the message.

        Returns:
            int -- The current channel of the message.
        """

        return self.channel

    def set_userdata(self, userdata: int):
        """
        Sets the userdate of the message.

        Arguments:
            userdata {int} -- The userdata of the message.

        Raises:
            TypeError -- When the parameter is not an int.
        """

        if isinstance(userdata, int):
            self.userdata = userdata
        else:
            raise TypeError("Expected int for userdata.")
        return

    def get_userdata(self):
        """
        Gets the current userdata of the message.

        Returns:
            int -- The current userdata of the message.
        """

        return self.userdata

    def set_payload_type(self, payload_type: int):
        """
        Sets the payload type of the message.
        ! Is currently not needed as the payload type is determined and set automatically.

        Arguments:
            payload_type {int} -- The payload type of the message.

        Raises:
            TypeError -- When the parameter is not an int.
        """

        if isinstance(payload_type, int):
            self.payload_type = payload_type
        else:
            raise TypeError("Expected int for payload_type.")
        return

    def get_payload_type(self):
        """
        Gets the current payload type of the message.

        Returns:
            int -- The current payload type of the message.
        """

        return self.payload_type

    def create_payload(self, payload):
        """
        This function will create the payload aad set the payload type automatically.
        The function will also call the required methods for updating the message.

        Arguments:
            payload {var} -- The payload that we want to send.

        Raises:
            ValueError -- If the value is outside the range of signed datatypes.
            ValueError -- If the value is outside the range of unsigned datatypes.
            TypeError -- If the payload is not of a recognized datatype.
        """

        if isinstance(payload, int):

            # Do something when payload is an int
            if payload < 0:

                # use signed datatypes
                if - 32768 <= payload <= 32767:

                    # Set the payload type and payload via the method.
                    self._update_payload(
                        self.DATA_INT, struct.pack("<i", payload))

                    return

                elif - 2147483648 <= payload <= 2147483647:

                    # Set the payload type and payload via the method.
                    self._update_payload(
                        self.DATA_LONG, struct.pack("<l", payload))

                    return

                else:

                    raise ValueError("Value out of signed range.")

            else:

                # Use unsigned datatypes
                if payload <= 255:

                    # Set the payload type and payload via the method.
                    self._update_payload(
                        self.DATA_UCHAR, struct.pack("<B", payload))

                    return

                elif payload <= 65535:

                    # Set the payload type and payload via the method.
                    self._update_payload(
                        self.DATA_UINT, struct.pack("<I", payload))

                    return

                elif payload <= 4294967295:

                    # Set the payload type and payload via the method.
                    self._update_payload(
                        self.DATA_ULONG, struct.pack("<L", payload))

                    return

                else:

                    raise ValueError("Value out of unsigned range.")

        elif isinstance(payload, float):

            # Set the payload type and payload via the method.
            self._update_payload(self.DATA_FLOAT, self.fl2bin(payload))

            return

        elif isinstance(payload, str):

            # A string is split into two cases; a string with length 1 is treated as a character,
            # while longer strings are treated as normal strings. The only difference this makes is
            # the payload type in the header.
            if len(payload) == 1:

                # Set the payload type and payload via the method.
                self._update_payload(
                    self.DATA_CHAR, bytearray(payload, "utf-8"))

                return

            else:

                # Set the payload type and payload via the method.
                self._update_payload(
                    self.DATA_STRING, bytearray(payload, "utf-8"))

                return

        else:

            raise TypeError("Payload has unknown or unsupported type.")

    @staticmethod
    def fl2bin(var: float) -> bytearray:
        """
        This function uses the pack method to convert a floating point number to a bytearray.
        The bytearray is little endian.

        Arguments:
            var {float} -- The float to be converted to a bytearray.

        Raises:
            TypeError -- A TypeError is raised when the variable is not a float.

        Returns:
            bytearray -- The bytearray representing the float.
        """

        if isinstance(var, float):

            # converting the float to a bytearray using the struct method.
            return struct.pack("<f", var)

        else:

            raise TypeError("Variable to converted has to be float!")

    @staticmethod
    def bin2fl(var: bytearray) -> float:
        """
        This function uses the unpack method to convert a bytearray to a floating point number.
        The bytearray is little endian.

        Arguments:
            var {bytearray} -- The bytearray to be converted to a float.

        Raises:
            ValueError -- [description]
            TypeError -- A TypeError is raised when the variable is not a bytearray.

        Returns:
            float -- The floating point number represented by the bytearray.
        """

        if isinstance(var, bytearray):

            if len(var) == 4:

                # Converting the bytearray to a float.
                return struct.unpack('<f', var)

            else:

                raise ValueError("Bytearray needs to have length 4!")
        else:

            raise TypeError("Variable to be converted has to be bytearray!")


############################################ Functions #############################################

def test_functions():
    """
    Function for testing the class methods.
    later to be changed to unittests.
    """

    test_message = Message()

    test_payload_type = test_message.DATA_ULONG

    test_destination = 24
    test_origin = 100
    test_function = 254
    test_channel = 80

    test_payload = 100005548

    test_message.set_destination(test_destination)
    if test_message.destination == test_destination:
        print("Update destination success!")
    else:
        print("-"*16)
        print("Update destination failed!")
        print("-"*16)

    test_message.set_origin(test_origin)
    if test_message.origin == test_origin:
        print("Update origin success!")
    else:
        print("-"*16)
        print("Update origin failed!")
        print("-"*16)

    test_message.set_function(test_function)
    if test_message.function == test_function:
        print("Update function success!")
    else:
        print("-"*16)
        print("Update function failed!")
        print("-"*16)

    test_message.set_channel(test_channel)
    if test_message.channel == test_channel:
        print("Update channel success!")
    else:
        print("-"*16)
        print("Update channel failed!")
        print("-"*16)

    test_message.create_payload(test_payload)
    if test_message.payload_type == test_payload_type:
        print("Auto update payload type success!")
    else:
        print("-"*16)
        print("Auto update payload type failed!")
        print("-"*16)

    # test_message._update_mesage()
    result = test_message.message.hex()
    payload = result[12:len(result) - 2]
    payload = [payload[i:i + 2] for i in range(0, len(payload), 2)]
    payload.reverse()
    payload_string = ""
    for byte in payload:
        payload_string += byte
    print(result)
    print("header: {};{};{};{};{};{}".format(result[0:2], result[2:4], result[4:6], result[6:8],
                                             result[8:10], result[10:12]))
    print("payload: {}".format(payload_string))
    print("tail: {}".format(result[len(result) - 2:len(result)]))

    print("\n"*2)

    test_message_array = bytearray([53, 211, 12, 3, 19, 0, 72, 101, 108, 108, 111, 44, 32, 116,
                                    104, 105, 115, 32, 105, 115, 32, 97, 32, 116, 101, 115, 116,
                                    33, 0])

    test_message.set_message(test_message_array)

    test_message.decode()

    print(test_message.destination)
    print(test_message.origin)
    print(test_message.function)
    print(test_message.channel)
    print(test_message.payload_type)
    print(test_message.userdata)
    print(test_message.payload)
    print(test_message.tail)


############################################### Main ###############################################

if __name__ == "__main__":

    test_functions()
