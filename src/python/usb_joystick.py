import paho.mqtt.client as mqtt
import serial

class Message:

    def __init__(self):
        self.bytes = []

    def add_byte (self, byte):
        self.bytes.append(byte)

if __name__ == "__main__":

    mqttc = mqtt.Client()

    mqttc.connect("192.168.1.5", 1881)

    mqttc.subscribe("vroom")

    mqttc.loop_start()

    ser = serial.Serial("com5", 115200, timeout=0,
                        parity=serial.PARITY_EVEN, rtscts=1)

    m = Message()

    print("ready")

    while True:

        ard = ser.read()

        if ard:

            by = ord(ard)

            if by == 83:
                m.add_byte(by)
                print(m.bytes)

                arr = bytearray(m.bytes)

                mqttc.publish("vroom", arr)
                m.bytes.clear()

            elif by != 84:
                m.add_byte(by)

            elif by == 84:
                m.add_byte(by)
                print(m.bytes)

                arr = bytearray(m.bytes)

                mqttc.publish("vroom", arr)

                print("goodbye")
                exit()