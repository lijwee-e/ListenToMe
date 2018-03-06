import os
import redis


r = None

def initDBLocal():
    global r
    r = redis.Redis(host=os.environ["redis_host"], port=os.environ["redis_port"], password=os.environ["redis_pwd"])

def initDB(rhostname, rport, pwd):
    global r
    r = redis.Redis(host=hostname, port=rport, password=pwd)
    
#update redis db
def addRadioStation(alias, url, site):
    global r
    radioStationID = r.incr('ID')
    r.hmset('ID:'+str(radioStationID),{'alias':alias, 'url':url, 'site':site})


#get total number of statio    
def getTotalStation():
    global r
    numberOfStation = len(r.keys('ID:*'))
    return numberOfStation

#get all radio station and return as list
def getListOfStation():
    global r
    radioDict = {}
    for station in r.keys('ID:*'):
        radioDict[station] = [r.hget(station,'alias'), r.hget(station,'url'),r.hget(station,'site') ]
    return radioDict
    
