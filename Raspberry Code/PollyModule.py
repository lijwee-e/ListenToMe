import boto3
import subprocess
import os
import time
from pygame import mixer

polly = None

#initialize polly
def initPolly():
    global polly
    region_name = os.environ['aws_region_name']
    polly = boto3.client('polly', region_name)
    

#function to play message
def playMessage(msg, filename):
    try:
        response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text=msg,
        TextType='text',
        VoiceId='Joanna')

        with open(filename, 'wb') as f:
            f.write(response['AudioStream'].read())
            
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
        
    except:
        print("Play Polly Failed!")
        pass

            
#function to play welcome message    
def playWelcomeMsg():
    d = time.strftime("%A %d")
    m = time.strftime("%B")
    msg = "Hi! You are listening to Piper Radio! Today is " + d +" of " + m
    playMessage(msg, "welcome.mp3")

    
    
    
