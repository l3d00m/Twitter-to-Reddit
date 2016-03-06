import json
import logging
import sys

import tweepy

from TwitterToReddit import constants
from TwitterToReddit.utils import extract_image_url
from TwitterToReddit.utils import submit_to_reddit

# http://gettwitterid.com/; optional
twitter_user_id = '109850283'
# optional
twitter_hashtag = '#uploadplan'
# subreddit to post to; required
subreddit = 'l3d00m'


class Tweet(object):
    """
    Source: https://github.com/joealcorn/TweetPoster
    """

    def __init__(self, json):
        if 'delete' in json:
            self.deleted = True
            logging.debug("is deleted")
            return
        self.deleted = False
        self.text = json['text']
        self.user = json['user']
        self.id = json['id']
        self.entities = json['entities']

    def __repr__(self):
        return '<TwitterToReddit.utils.Tweet ({0})>'.format(self.id)


class StdOutListener(tweepy.StreamListener):
    """
    Handles data received from the stream.
    http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
    """

    def on_data(self, data):
        logging.debug(data)

        tweet = Tweet(json=json.loads(data))

        if tweet.deleted:
            return True

        if twitter_user_id == '' or str(tweet.user['id']) != twitter_user_id:
            logging.debug("Author has another id (" + str(tweet.user['id']) + "), not posting")
            # Check if user is given and if true, then it should equal the tweet author;
            # otherwise we will return True
            return True

        image_url = extract_image_url(tweet)
        if image_url != '':
            submit_to_reddit(image_url)

        return True  # To continue listening

    def on_error(self, status_code):
        logging.warning('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        logging.warning('Timeout...')
        return True  # To continue listening

    def on_disconnect(self, notice):
        logging.critical('We got disconnected by twitter')
        sys.exit(1)


def main():
    if subreddit == '':
        logging.critical("no subreddit given")
        return

    listener = StdOutListener()

    twitter_auth = tweepy.OAuthHandler(constants.twitter_consumer_key, constants.twitter_consumer_key_secret)
    twitter_auth.set_access_token(constants.twitter_access_token, constants.twitter_access_token_secret)

    stream = tweepy.Stream(twitter_auth, listener)
    if twitter_hashtag != '':
        stream.filter(follow=[twitter_user_id], track=[twitter_hashtag])
    elif twitter_user_id != '':
        stream.filter(follow=[twitter_user_id])
    else:
        logging.warning("No filter given! Either 'twitter_user_id' or 'twitter_hashtag' should have a valid value!")
