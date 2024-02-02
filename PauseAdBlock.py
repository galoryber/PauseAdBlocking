import requests, time, logging
import RPi.GPIO as gpio

logging.basicConfig(filename='/root/scripts/piButton.log', format='%(levelname)s:%(asctime)s:%(message)s', encoding='utf-8', level=logging.DEBUG)

# On button press, pause PiHole DNS blocking for X number of minutes

piHoleIP = "192.168.100.151"
pinChannel = 26 # GPIO26 == PIN 37
pinBoard= 37 # setmode(gpio.BOARD) Board 37 -> GPIO26
pauseTime = 120 # Two minutes

def getAuth():
    with open("/etc/pihole/setupVars.conf","r") as f:
        auth = []
        for ln in f:
            if ln.startswith("WEBPASSWORD"):
                auth.append(ln)
    authString = auth[0].split('=')[1].rstrip() # WEBPASSWORD=asdfValueasdf

    return authString

webPass = getAuth()

def pause_AdBlocking(whatarg):
    logging.info("Pin " + str(whatarg) + " was pressed")
    piholeURL = "http://{}/admin/api.php?disable={}&auth={}".format(piHoleIP, pauseTime, webPass)
    response = requests.get(piholeURL)

    logging.info("Ad Blocking was paused for the next two minutes\n")
    return response

gpio.setmode(gpio.BOARD)
gpio.setup(pinBoard, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.add_event_detect(pinBoard, gpio.RISING, callback=pause_AdBlocking) # Setup event on pin rising edge

try:
    while True:
        time.sleep(0.25)
        pass

except KeyboardInterrupt:
    print("key interrupt") #do something here

finally:
    gpio.cleanup()
