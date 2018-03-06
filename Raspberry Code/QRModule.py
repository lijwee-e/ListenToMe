import os
import time
import pyqrcode
import boto

import os


client = None
db = None
session = None
bucket = None

youtubeBaseSearchURL = "https://www.youtube.com/results?search_query="


#ECS
#initialize ECS    
def initECS():
    global session
    global bucket
    session = boto.connect_s3(os.environ["ecs_access_key_id"], os.environ["ecs_secret_key"], host=os.environ["ecs_host"])  
    bucket = session.get_bucket(os.environ["ecs_bucket"] )

def postToECS(src, imageName):
    if bucket != None:
        photo = bucket.new_key(imageName)
        photo.set_contents_from_filename(src)
        photo.set_metadata('title', imageName.split(".")[0])
        
        photo.set_acl('public-read')

def getAllImage():
    imageList = []
    for bucket in session.get_all_buckets():
        if os.environ["ecs_bucket"] in bucket.name:
            for object in bucket.list():
                imageList.append(object.key)

    return imageList

                
        

#QR Code
def genQRCode(tweetMsg):
    try:
        qrImg = pyqrcode.create(youtubeBaseSearchURL + tweetMsg.replace(" ", "+"))
        if not os.path.exists("qrCode"):
            os.makedirs("qrCode")
        dest = os.path.join("qrCode", tweetMsg + ".png")
        qrImg.png(dest, scale=5)
        print("QR Code generated")
        #post to ECS
        postToECS(dest, tweetMsg+".png")
        print("Posted to ECS")
        #remove file from local
        os.remove(dest)
        print("local copy removed")
    except:
        print("QR Code Generating Failed")
        pass

    
