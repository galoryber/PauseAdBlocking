import requests, time, logging
import RPi.GPIO as gpio

logging.basicConfig(filename='/root/scripts/piButton.log', format='%(levelname)s:%(asctime)s:%(message)s', encoding>

# On button press, pause PiHole DNS blocking for X number of minutes

piHoleIP = "192.168.100.151"
ledPinChannel = 31 #GPIO6 == PIN 31 https://i.pinimg.com/736x/c6/a9/39/c6a939f2c365e141abb18947752dbe8b.jpg
pinBoard= 37 # setmode(gpio.BOARD) Board 37 -> GPIO26
pauseTime = 120 # Two minutes
ledTimer = 0

# Authenticate to PiHole
def getAuth():
    with open("/etc/pihole/setupVars.conf","r") as f:
        auth = []
        for ln in f:
            if ln.startswith("WEBPASSWORD"):
                auth.append(ln)
    authString = auth[0].split('=')[1].rstrip() # WEBPASSWORD=asdfValueasdf

    return authString
webPass = getAuth()

# Self explanatory function name
def pause_AdBlocking(whatarg):
    logging.info("Pin " + str(whatarg) + " was pressed")
    piholeURL = "http://{}/admin/api.php?disable={}&auth={}".format(piHoleIP, pauseTime, webPass)
    response = requests.get(piholeURL)
    logging.info("Ad Blocking was paused for the next two minutes\n")
    ledWatcher(pauseTime)

# Build separate function for LED controls
def ledWatcher(onTimer):
    logging.info("Turning on " + str(ledPinChannel) + " for " + str(onTimer))
    gpio.output(ledPinChannel, True)
    logging.info("LED should be on")
    time.sleep(onTimer)
    gpio.output(ledPinChannel, False)
    logging.info("LED should be off now")

# Function have been defined
# setup pins and start operating
gpio.setmode(gpio.BOARD)
# setup button pin
gpio.setup(pinBoard, gpio.IN, pull_up_down=gpio.PUD_DOWN)
# setup led pin
gpio.setup(ledPinChannel, gpio.OUT)
# listen for button press events
gpio.add_event_detect(pinBoard, gpio.RISING, callback=pause_AdBlocking) # Setup event on pin rising edge

try:
    while True:
        time.sleep(0.25)
        pass

except KeyboardInterrupt:
    print("key interrupt") #do something here

finally:
    gpio.cleanup()
