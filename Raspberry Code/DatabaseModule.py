import os
import redis


r = None

def initDB():
    global r
    r = redis.Redis(host=os.environ["redis_host"], port=os.environ["redis_port"], password=os.environ["redis_pwd"])

#update redis db
def addRadioStation(alias, url):
    global r
    radioStationID = r.incr('radioStationID')
    r.hmset('radioStationID:'+str(radioStationID),{'alias':alias, 'url':url})

#get total number of statio    
def getTotalStation():
    global r
    numberOfStation = len(r.keys('radioStationID:*'))
    return numberOfStation

#get all radio station and return as list
def getListOfStation():
    global r
    radioDict = {}
    for station in r.keys('radioStationID:*'):
        radioDict[station] = [r.hget(station,'alias'), r.hget(station,'url')]
    return radioDict
    
