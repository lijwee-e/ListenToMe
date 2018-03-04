#Import Audio Module
import alsaaudio

masterVolume = alsaaudio.Mixer("PCM")

#get current volume
def getVolume():
    global masterVolume
    if masterVolume != None:
        return masterVolume.getvolume()
    else:
        return -1
    
#set currentVolume()
def setVolume(volumeLevel):
    if masterVolume != None:
        masterVolume.setvolume(volumeLevel)
        return True
    else:
        return False
