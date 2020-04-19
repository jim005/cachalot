#!/usr/bin/env python

# -------------------------------------------
# Affichage du niveau d'eau de la cuve "Cachalot"
#
#
# sources et inspirations (many thanks) :
#    https://www.fred-j.org/?p=364
#
# Capteur NO / Hauteurs par rapport au sol : 200 mm, 405 mm, 615 mm, 825 mm, 1035 mm
#
#
#
# -------------------------------------------

import RPi.GPIO as GPIO
import time
import requests


DEBUG = 1;

#-------------[ CABLAGE ]--------------------

# Cable de la sonde de 0(20%) a 4(100%)
CAPTEUR_GPIO = [4, 17, 27, 22, 24];
CAPTEUR_0_DISTANCE = 20
CAPTEUR_1_DISTANCE = 40.5
CAPTEUR_2_DISTANCE = 61.5
CAPTEUR_3_DISTANCE = 82.5
CAPTEUR_4_DISTANCE = 103.5


# Jeedom
JEEDOM_IP =  "192.168.1.33"
JEEDOM_VIRTUAL_APIKEY = "JiVW21qvOqNPVHe5tbXbxOhLMhK1OfM8"
JEEDOM_VIRTUAL_COMMANDE_ID = 749



#-------------[ Initialisation ]--------------

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering

for i in range(5):
    GPIO.setup(CAPTEUR_GPIO[i], GPIO.IN) # Set pin as GPIO in


#-------------[ Main ]--------------

def measure():

    print ("\n\n\n");

    for i in range(5):

        WATER_LEVEL = 0

        if GPIO.input(CAPTEUR_GPIO[0]) == False:
            WATER_LEVEL =  CAPTEUR_4_DISTANCE
            break
        if GPIO.input(CAPTEUR_GPIO[1]) == False:
            WATER_LEVEL = CAPTEUR_3_DISTANCE
            break
        if GPIO.input(CAPTEUR_GPIO[2]) == False:
            WATER_LEVEL = CAPTEUR_2_DISTANCE
            break
        if GPIO.input(CAPTEUR_GPIO[3]) == False:
            WATER_LEVEL = CAPTEUR_1_DISTANCE
            break
        if GPIO.input(CAPTEUR_GPIO[4]) == False:
            WATER_LEVEL = CAPTEUR_0_DISTANCE
            break


    # debug
    if DEBUG :

        for i in range(5):

            if (i == 0):
                P = " 100"
            elif (i == 1):
                P = " 80 "
            elif (i == 2):
                P = " 60 "
            elif (i == 3):
                P = " 40 "
            elif (i == 4):
                P = " 20 "

            if GPIO.input(CAPTEUR_GPIO[i]) == True:
                print ("  ",P,"%   |          |     GPIO ",CAPTEUR_GPIO[i])
            else:
                print ("  ",P,"%   |##########|     GPIO ",CAPTEUR_GPIO[i])


    return WATER_LEVEL


# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
while True:
    try:

        valeur = measure();
        print (measure())
        payload = {'plugin': 'virtual', 'apikey': JEEDOM_VIRTUAL_APIKEY, 'type': 'virtual', 'id': JEEDOM_VIRTUAL_COMMANDE_ID, 'value': valeur}
        r = requests.post("http://" + JEEDOM_IP + "/core/api/jeeApi.php", params=payload)

        # debug
        if DEBUG :
            print(payload)
            print ("----------")
            print ("\n\n\n")
            time.sleep(1)          # 1 seconde
        else:
            time.sleep(30*60*60)   # 30 minutes

    except KeyboardInterrupt:
        # User pressed CTRL-C
        # Reset GPIO settings
        GPIO.cleanup()

print('all done, bye')
