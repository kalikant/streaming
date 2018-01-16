import keywords
import tweepy
import json
from  StreamProducer import JSONProducer

class StreamListener(tweepy.StreamListener):

       
    def on_status(self, status):
        
        if status.retweeted:
            return

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        if geo is not None:
            geo = json.dumps(geo)

        if coords is not None:
            coords = json.dumps(coords)
        
        
        msg=status._json
        print(msg)
        JSONProducer.publishJSONData(self,msg)
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(keywords.TWITTER_APP_KEY, keywords.TWITTER_APP_SECRET)
auth.set_access_token(keywords.TWITTER_KEY, keywords.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=keywords.TRACK_TERMS)
