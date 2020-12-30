import tweepy
from datetime import datetime
from datetime import date
import logging
import time
import threading
import os, random

# Authenticate to Twitter - create OAuthHandler object and set access token
auth = tweepy.OAuthHandler("zyqCvH35mkc9ZvdCXNbHKA4l0", 
    "NRC9EXYC76va6k4GetMbwYO9U1OB0M1wN9e11F1Cn7k4lwSUix")
auth.set_access_token("913931733485195264-xHeXN54btJjNBr7Jo4H1qtaX499COSc", 
    "Iy9gyY1tqPd1dn9qpEszPsYOAXGwSvhfQ6FLPO16jKGmg")

# Create tweepy API object using OAuthHandler object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def follow_followers(api):
    while True:
        logger.info("Retrieving and following followers")
        for follower in tweepy.Cursor(api.followers).items():
            if not follower.following:
                logger.info(f"Following {follower.name}")
                follower.follow()
        logger.info("Waiting on followers...")
        time.sleep(60)

def tweet(api):
    while True:
        if datetime.now().strftime("%H:%M") == "15:00":
            logger.info("Tweeting")
            file = os.listdir(os.getcwd())[random.randint(1, len(os.listdir(os.getcwd())))]
            api.update_with_media(os.getcwd() + "/" + file, status="bark bark\n\n" + str(date.today()))
        logger.info("Waiting on tweeting...")
        time.sleep(60)

def reply(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        logger.info(f"Answering to {tweet.user.screen_name}")
        logger.info(tweet.id)
        api.update_status(status = "@" + tweet.user.screen_name + " @" + tweet.user.screen_name + " bark bark\n\n" + datetime.now().strftime("%H:%M:%S"), in_reply_to_status_id = tweet.id)
    return new_since_id

def reply_thread(api):
    since_id = 1
    while True:
        since_id = reply(api, since_id)
        logger.info("Waiting on mentions...")
        time.sleep(60)

api.update_with_media(os.getcwd() + "/charlie.jpg", status="bark bark\n\n" + str(date.today()))

threads = list()

logging.info("create and start Following thread")
ff = threading.Thread(target=follow_followers, args=(api,))
threads.append(ff)
ff.start()

logging.info("create and start Tweeting thread")
t = threading.Thread(target=tweet, args=(api,))
threads.append(t)
t.start()

logging.info("create and start Replying thread")
r = threading.Thread(target=reply_thread, args=(api,))
threads.append(r)
r.start()
