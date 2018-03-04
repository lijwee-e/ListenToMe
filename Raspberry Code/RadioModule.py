import vlc
from time import sleep

#Radio Instance
instance = None
media = None
player = None

def initRadio(url):
    global instance
    global media
    global player
    #define VLC instance
    instance = vlc.Instance('--input-repeat=-1')
    #Define VLC player
    player=instance.media_player_new()
    #Define VLC media
    media=instance.media_new(url)
    #Set player media
    player.set_media(media)
    #Play the media
    player.play()
    
def changeChannel(url):
    global instance
    global media
    global player
    player.stop()
    media=instance.media_new(url)
    player.set_media(media)
    player.play()
    

def getSongTitle():
    sleep(2)
    song = media.get_meta(12)
    return song


    
