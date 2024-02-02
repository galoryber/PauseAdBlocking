# PauseAdBlocking
Using GPIO pins on the raspberrypi with PiHole to setup a button that temporarily disables ad-blocking. I installed a PiHole on a family members network, and wouldn't be there to help manage it. This helps them in case something is blocked that they need access to. 

### Setup
Must be run as root for gpio pin events (in some conditions) and to read the auth keys from PiHole dynamically. 
- /root/PauseAdBlock.py

Create a crontab entry to make sure the script is always running
- @reboot /usr/bin/python /root/PauseAdBlock.py

