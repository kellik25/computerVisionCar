import bluetooth
import time
import struct
import network
import ubinascii
from wifisecrets import Tufts_Wireless as wifi
import mqtt
from BLELibrary import Yell

#centroid range 200 to 1300
#700 middle
#under 100 stop value
def whenCalled(topic, msg):
    global wcdata
    print((topic.decode(), msg.decode()))
    # wcdata = (topic.decode(), msg.decode())
    wcdata = msg.decode()
    #led.on()
    time.sleep(0.5)
    #led.off()

def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("MAC " + mac)

    station.connect(wifi['ssid'],wifi['pass'])
    while not station.isconnected():
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())


try:
    connect_wifi(wifi)
    fred = mqtt.MQTTClient('listen', '10.243.28.115', keepalive=60)
    fred.connect()
    fred.set_callback(whenCalled)
    fred.subscribe('ME035')
    L = Yell('Fred', verbose = True)
    if L.connect_up():
        print(' L connected')
        while L.is_connected:

            fred.check_msg()
            try:
                print(wcdata)
                if int(wcdata) <= 100:
                    L.send("Stop")
                elif int(wcdata) <= 400:
                    L.send("Right")
                elif int(wcdata) <= 900:
                    L.send("Forward")
                elif int(wcdata) <= 1300:
                    L.send("Left")
                else:
                    L.send("stop")
            except:
                print("except")

            '''
            time.sleep(4)
            L.send("Forward")
            time.sleep(4)
            L.send("Left")
            time.sleep(4)
            L.send("Right")
            time.sleep(4)
            L.send("Stop")
            '''
except Exception as e:
    print(e)
finally:
    L.disconnect()
    print('closing up')

'''
while True:
    fred.check_msg()
    try:
        print(f"wcdata:{wcdata}")
        print(wcdata)
    except:
        print("except")
    time.sleep(2)
    p.send("Forward")
    time.sleep(2)
    p.send("Left")
    time.sleep(2)
    p.send("Right")
    time.sleep(2)
    p.send("Stop")
    time.sleep(.1)

p.disconnect()
'''
