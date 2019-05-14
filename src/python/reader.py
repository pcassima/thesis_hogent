"""
This program reads everything that enters the mqtt network and decodes it to show what the message means
"""
# import libraries that are needed
import lib.paho.mqtt.client as mqtt
from pynput.keyboard import Key, Listener

# set mqttc as the client
mqttc = mqtt.Client()

# setting the mqtt broker adress and port
mqttc.connect("192.168.1.5", 1881)

# subscibing to the topic
mqttc.subscribe("vroom")

# starting the mqtt loop
mqttc.loop_start()

# show that the programme is ready
print("ready")

# check for any new incomming messages
def on_message(client, userdata, message):

    # check if its on the right topic
    if message.topic == "vroom":

        # show the full message (in bytes)
        print("Message: {}".format(message.payload))

        # check for who the message is
        if message.payload[0] == 20:

            print("To:      Car")

        elif message.payload[0] == 21:

            print("To:      Lights")

        elif message.payload[0] == 60:

            print("To:      Controller")

        elif message.payload[0] == 61:

            print("To:      Vision")

        # check from who the message is
        if message.payload[1] == 20:

            print("From:    Car")

        elif message.payload[1] == 21:

            print("From:    Lights")

        elif message.payload[1] == 60:

            print("From:    Controller")

        elif message.payload[1] == 61:

            print("From:    Vision")

        # what is the meaning of the message (for id 20)
        if message.payload[0] == 20:
            if message.payload[2] == 0:
                print("What:    Stop")
            elif message.payload[2] == 1:
                print("What:    Forward")
            elif message.payload[2] == 2:
                print("What:    Back")
            elif message.payload[2] == 3:
                print("What:    Left")
            elif message.payload[2] == 4:
                print("What:    Right")
            elif message.payload[2] == 5:
                print("What:    Left Stop")
            elif message.payload[2] == 6:
                print("What:    Right Stop")

            # show the speed of the car
            print("Speed:   {}".format(message.payload[6]))

        # what is the meaning of the message (for id 21)
        elif message.payload[0] == 21:
            if message.payload[2] == 0:
                print("What:    Lights out")

            if message.payload[2] == 1:
                print("What:    Start Countdown")

        # what is the meaning of the message (for id 60)
        elif message.payload[0] == 60:
            print("What:    Enable Steering")

        # print a line out
        print("##################################################")

mqttc.on_message = on_message

# if their is any button pressed on the keyboard
def on_press(key):

    # reform the key to a string and get the right char
    letter = key
    letter = str(letter)
    letter = letter[1]

    # check if the letter is p
    if letter == "p":

        # print out exiting and then leave the program
        print('exiting')
        exit()

if __name__ == "__main__":

    # check if the buttons are pressed (this is to quite the program)
    with Listener(on_press=on_press) as listener:
        listener.join()
