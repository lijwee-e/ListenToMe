import tweepy
import os

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def postTweet(msg):
  try:
    cfg = { 
      "consumer_key"        : os.environ["tw_consumer_key"],
      "consumer_secret"     : os.environ["tw_consumer_secret"],
      "access_token"        : os.environ["tw_access_token"],
      "access_token_secret" : os.environ["tw_access_token_secret"]
      }

    api = get_api(cfg)
    tweet = "I'm listening to "+msg + " #DellEMCPiedPiper #ListenToMe"
    status = api.update_status(status=tweet)
    return True

  except:
    return False
