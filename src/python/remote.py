"""
this program controlls the car with inputs from a keyboard
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

# used to look if the button is already pressed
z_pressed = False
s_pressed = False
q_pressed = False
d_pressed = False

u_pressed = False

k_pressed = False

l_pressed = False

# is driving enabled or not
drive_enabled = False

# target name and name of the controller
target = 20
Iam = 60

# check for any new incomming messages
def on_message(client, userdata, message):

    # using the global variables
    global drive_enabled
    global z_pressed
    global s_pressed
    global q_pressed
    global d_pressed

    global u_pressed
    global k_pressed
    global l_pressed


    # check if its on the right topic
    if message.topic == "vroom":

        # is the message for me
        if message.payload[0] == 60:

            # if the fuction is 0
            if message.payload[2] == 0:

                # disable driving
                drive_enabled = False
                print("not enabled")

                # setting all the buttons to false
                z_pressed = False
                s_pressed = False
                q_pressed = False
                d_pressed = False

                u_pressed = False
                k_pressed = False
                l_pressed = False

                # arr to send for stopping the car
                arr = bytearray([20, 60, 0, 0, 11, 0, 0, 0])

                # send array to kill the car
                mqttc.publish("vroom",  arr)

            # if the function is 1
            elif message.payload[2] == 1:

                # enable driving
                drive_enabled = True
                print("enabled")

mqttc.on_message = on_message



# if the button is pressed
def pressed(letter):

    # making sure it is a string then you get 'n' so we wand n
    letter = str(letter)
    letter = letter[1]

    # using the global variables
    global z_pressed
    global s_pressed
    global q_pressed
    global d_pressed

    global u_pressed
    global k_pressed
    global l_pressed

    global drive_enabled

    global target
    global Iam

    # making the array to send
    arr = bytearray([target, Iam, 0, 0, 11, 0, 255, 0])

    # if drive is enabled than you can drive
    if drive_enabled == True:

        # button z (forward)
        if letter == "z":

            # checking if z or s is already pressed
            if z_pressed == False:
                if s_pressed == False:

                    # setting the destination and the speed
                    arr[2] = 1
                    arr[6] = 200

                    # send the array
                    mqttc.publish("vroom",  arr)

                    # print what is pressed
                    print("pressed z")
                    z_pressed = True

        # button s (back)
        if letter == "s":

            # checking if z or s is already pressed
            if s_pressed == False:
                if z_pressed == False:

                    # setting the destination and the speed
                    arr[2] = 2
                    arr[6] = 175

                    # send the array
                    mqttc.publish("vroom",  arr)

                    # print what is pressed
                    print("pressed s")
                    s_pressed = True

        # button q (left)
        if letter == "q":

            # checking if q or d is already pressed
            if q_pressed == False:
                if d_pressed == False:

                    # if the car is driving back
                    if s_pressed == True:

                        # set speed
                        arr[6] = 100

                    else:

                        # set speed if the car isn't driving back
                        arr[6] = 150

                    # set function
                    arr[2] = 3

                    # send the array
                    mqttc.publish("vroom",  arr)

                    # print what is pressed
                    print("pressed q")
                    q_pressed = True

        # button d (right)
        if letter == "d":

            # checking if q or d is already pressed
            if d_pressed == False:
                if q_pressed == False:

                    # if the car is driving back
                    if s_pressed == True:

                        # set speed
                        arr[6] = 100

                    else:

                        # set speed if the car isn't driving back
                        arr[6] = 150

                    # set function
                    arr[2] = 4

                    # send the array
                    mqttc.publish("vroom",  arr)

                    # print what is pressed
                    print("pressed d")
                    d_pressed = True

    # button u (start lights)
    if letter == "u":

        # check if already pressed
        if u_pressed == False:

            # setting the target, function and delay
            arr[0] = 21
            arr[2] = 1
            arr[6] = 225

           # send the array
            mqttc.publish("vroom",  arr)

            # print what is pressed
            print("pressed u")
            u_pressed = True

    # button k (lights out)
    elif letter == "k":

        # check if already pressed
        if k_pressed == False:

            # setting the target, function and delay
            arr[0] = 21
            arr[2] = 0
            arr[6] = 0

            # send the array
            mqttc.publish("vroom",  arr)

            # print what is pressed
            print("pressed k")
            k_pressed = True

    # button l (lights out and disable driving and stop car)
    elif letter == "l":

        # check if already pressed
        if l_pressed == False:

            # setting the target, function and delay
            arr[0] = 21
            arr[2] = 0
            arr[6] = 0

            # send the array
            mqttc.publish("vroom",  arr)

            # setting the target, function and speed
            arr[0] = 20
            arr[2] = 0
            arr[6] = 0

            # send the array
            mqttc.publish("vroom",  arr)

            # print what is pressed
            print("pressed l")

            # disable driving input
            l_pressed = True
            drive_enabled = False

            print("not enabled")

    # button p (to kill the program)
    if letter == "p":

        # setting the target, function and speed
        arr[0] = 20
        arr[2] = 0
        arr[6] = 0

        # send the array
        mqttc.publish("vroom",  arr)

        # print out exiting and then leave the program
        print('exiting')
        exit()


# if the button is released
def released(letter):

    # making sure it is a string then you get 'n' so we wand n
    letter = str(letter)
    letter = letter[1]

    # using the global variables
    global z_pressed
    global s_pressed
    global q_pressed
    global d_pressed

    global u_pressed
    global k_pressed
    global l_pressed

    global drive_enabled

    global target
    global Iam

    # making the array to send
    arr = bytearray([target, Iam, 0, 0, 11, 0, 255, 0])

    # if drive is enabled than you can drive
    if drive_enabled == True:

        # check if z is pressed
        if z_pressed == True:

            # button z released
            if letter == "z":

                # setting the destination and the speed
                arr[2] = 0
                arr[6] = 0

                # send the array
                mqttc.publish("vroom",  arr)

                # print what is released
                print("released z")
                z_pressed = False

        # check if s is pressed
        if s_pressed == True:

            # button z released
            if letter == "s":

                # setting the destination and the speed
                arr[2] = 0
                arr[6] = 0

                # send the array
                mqttc.publish("vroom", arr)

                # print what is released
                print("released s")
                s_pressed = False

        # check if q is pressed
        if q_pressed == True:

            # button z released
            if letter == "q":

                # setting the destination and the speed
                arr[2] = 5
                arr[6] = 0

                # send the array
                mqttc.publish("vroom", arr)

                # print what is released
                print("released q")
                q_pressed = False

        # check if d is pressed
        if d_pressed == True:

            # button z released
            if letter == "d":

                # setting the destination and the speed
                arr[2] = 6
                arr[6] = 0

                # send the array
                mqttc.publish("vroom", arr)

                # print what is released
                print("released d")
                d_pressed = False

    # check if u is pressed
    if u_pressed == True:

        # button z released
        if letter == "u":

            # print what is released
            print("released u")
            u_pressed = False

    # check if k is pressed
    if k_pressed == True:

        # button z released
        if letter == "k":

            # print what is released
            print("released k")
            k_pressed = False

    # check if l is pressed
    if l_pressed == True:

        # button z released
        if letter == "l":

            # print what is released
            print("released l")
            l_pressed = False


# when a press input do ...
def on_press(key):

    # for debug
    # print("a button was pressed")

    # do this function
    pressed(key)

# when a release input do ...
def on_release(key):

    # for debug
    # print("a button was pressed")

    # do this function
    released(key)


if __name__ == "__main__":

    # check if the buttons are pressed or released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
