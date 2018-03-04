#Project Title: ListenToMe
#Author: Li Jwee
#Data Created: 04 Feb 18
#Date Modified: 02 Mar 18
#Version: 0.1 Beta

#Import Modules
import RPi.GPIO as GPIO
import ADC0832
import time
import os.path
import os
from time import sleep

#User Define Modules
from LCDModule import *
from TwitterModule import *
from VolumeModule import *
from RadioModule import *
from DatabaseModule import *



#Variable Declarations
################################################################################################### 
#I/O Devices Declarations

#Blue Button
TweetBtnPin = 15
TweetEnable = True

#Rotary Encoder
RoAPin = 11    # pin11
RoBPin = 12    # pin12
RBtnPin = 13    # Rotarty Button Pin


globalRadioChannel = 0
flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

#Potentiometer
Last_Volume_Value = 0
Current_Volume_Value = 0


#LCD Screen
LCDScreen = ""

####################################################################################################
#Radio Variable
MAXRADIOCHANNEL = 0
RadioDict = {}

####################################################################################################
# General I/O Devices Functions

def setup():
	global LCDScreen
	global MAXRADIOCHANNEL
	global RadioDict
	
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	#Rotary
	GPIO.setup(RoAPin, GPIO.IN)    # input mode
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(RBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(RBtnPin, GPIO.FALLING, callback=btnResetChannel)
	
	#Potentiometer
	ADC0832.setup()
	Current_Volume_Value = Last_Volume_Value = ADC0832.getResult()

	
	#LCD Screen
	LCDScreen = Screen(bus=1, addr=0x3f, cols=16, rows=2)
	LCDScreen.enable_backlight()
        LCDScreen.clear()
	LCDScreen.display_data("Piper Radio", "")

	#BlueButton
	GPIO.setup(TweetBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

	#credential setup
	if os.path.isfile("setenv.py"):
            print "running local"
            import setenv
        else:
            print "I must be in CF"

        #initialize database
	initDB()
	MAXRADIOCHANNEL = getTotalStation()
	RadioDict = getListOfStation()
	

	#intialize radio
	initRadio(RadioDict["radioStationID:0"][1])

	

	
def destroy():
	global LCDScreen
	#clear display
	LCDScreen.disable_backlight()
	LCDScreen.clear()
	# Release resource
	GPIO.cleanup()             
	
	print "\n GPIO cleaned up completed."
	
def loop():
	global globalRadioChannel
	global LCDScreen
	tmp = 0	# Rotary Temporary

	while True:
		rotaryChangeChannel()
		changeVolume(ADC0832.getResult())
		if tmp != globalRadioChannel:
			print 'globalRadioChannel = %d' % globalRadioChannel
			tmp = globalRadioChannel
		if GPIO.input(TweetBtnPin) == GPIO.LOW and TweetEnable:
                        TweetMusic(getSongTitle())
		
			
############################################################################################
#Rotary Input
def rotaryChangeChannel():
	global flag
	global Last_RoB_Status
	global Current_RoB_Status
	global globalRadioChannel
	global RadioDict
	Last_RoB_Status = GPIO.input(RoBPin)
	while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			globalRadioChannel = (globalRadioChannel + 1) % MAXRADIOCHANNEL
			changeChannel(RadioDict["radioStationID:" + str(globalRadioChannel)][1])
			LCDScreen.display_data("Piper Radio", RadioDict["radioStationID:" + str(globalRadioChannel)][0])
			
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			globalRadioChannel = (globalRadioChannel - 1) % MAXRADIOCHANNEL
			changeChannel(RadioDict["radioStationID:" + str(globalRadioChannel)][1])
			LCDScreen.display_data("Piper Radio", RadioDict["radioStationID:" + str(globalRadioChannel)][0])

def btnResetChannel(channel):
	global globalRadioChannel
	global RadioDict
	global MAXRADIOCHANNEL
	#Reset Channel
	globalRadioChannel = 0

	#in the event if database is updated
	if getTotalStation() != MAXRADIOCHANNEL:
                MAXRADIOCHANNEL = getTotalStation()
                RadioDict = getListOfStation()
                
	changeChannel(RadioDict["radioStationID:" + str(globalRadioChannel)][1])
	LCDScreen.display_data("Piper Radio", RadioDict["radioStationID:" + str(globalRadioChannel)][0])
	

#Potentiometer Input
def changeVolume(vol):
	global Last_Volume_Value
	global Current_Volume_Value
	Current_Volume_Value = vol
	#only set volume when the difference in value is more than 1
	#to address circuit fluctuation  
	if abs(Current_Volume_Value - Last_Volume_Value) > 1:
		volumeValue = float(Current_Volume_Value) / 255 * 100
		Last_Volume_Value = Current_Volume_Value
		setVolume(int(volumeValue))
		print("Current Volume:%d" % (volumeValue))
		delay(10)

#Blue button
def TweetMusic(msg):
        global TweetEnable
        TweetEnable = False
        print "Button Pressed"
        LCDScreen.display_data("Posting Tweet", "...")
        postTweet(msg)
        LCDScreen.display_data("Tweeted!", "")
        sleep(1)
        LCDScreen.display_data("Piper Radio", RadioDict["radioStationID:" + str(globalRadioChannel)][0])
        TweetEnable = True
				
#################################################################################################

#Main Application

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

