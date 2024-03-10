import requests, time, logging, threading, os
import RPi.GPIO as gpio

logging.basicConfig(filename='/root/scripts/piButton.log', format='%(levelname)s:%(asctime)s:%(message)s', encoding='utf-8', level=logging.DEBUG)

# On button press, pause PiHole DNS blocking for X number of minutes

# Look up WLAN 0 IP address and set it
piHoleIP = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
ledPinChannel = 31 #GPIO6 == PIN 31 https://i.pinimg.com/736x/c6/a9/39/c6a939f2c365e141abb18947752dbe8b.jpg
pinBoard= 37 # setmode(gpio.BOARD) Board 37 -> GPIO26
pauseTime = 120 # Two minutes
ledTimer = 0

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
    resp = requests.get(piholeURL)
    logging.info("Ad Blocking was paused for the next two minutes")
    # # turn on notification LED
    t = threading.Thread(target=ledWatcher, args=[pauseTime])
    t.run()
    return resp

def ledWatcher(onTimer):
    logging.info("Turning on " + str(ledPinChannel) + " for " + str(onTimer))
    while onTimer > 0:
        gpio.output(ledPinChannel, True)
        sleepTime = 1
        onTimer -= sleepTime
        time.sleep(sleepTime)
    logging.info("Turning off " + str(ledPinChannel) + "\n\n")
    gpio.output(ledPinChannel, False)


gpio.setmode(gpio.BOARD)

# setup button pin
gpio.setup(pinBoard, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# setup led pin
gpio.setup(ledPinChannel, gpio.OUT)

# listen for button press events
# Appears that subsequent button presses are 'queued' for after the function returns. 
buttonThread = threading.Thread(target=gpio.add_event_detect(pinBoard, gpio.RISING, callback=pause_AdBlocking)) # Setup event on pin rising edge
buttonThread.run()

try:
    while True:
        time.sleep(0.25) # Keeps program running forever, listening for button events, sleep keeps CPU usage low
        pass

except KeyboardInterrupt:
    gpio.cleanup()
    stoppedMsg = "Button press program was manually stopped"
    logging.warning(stoppedMsg)
    print(stoppedMsg)

finally:
    gpio.cleanup()
    logging.error("Button press program has closed")
