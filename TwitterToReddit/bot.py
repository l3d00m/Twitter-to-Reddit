import json
import logging

import praw
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

reddit_auth = praw.Reddit(user_agent="Twitter X-Poster by l3d00m")
reddit_auth.set_oauth_app_info(client_id=constants.reddit_client_id, client_secret=constants.reddit_client_secret,
                               redirect_uri=constants.reddit_redirect_uri)

twitter_auth = tweepy.OAuthHandler(constants.twitter_consumer_key, constants.twitter_consumer_key_secret)
twitter_auth.set_access_token(constants.twitter_access_token, constants.twitter_access_token_secret)


class Tweet(object):
    """
    Source: https://github.com/joealcorn/TweetPoster
    """

    def __init__(self, json):
        if 'delete' in json:
            print("is deleted")
            return
        self.text = json['text']
        self.user = json['user']
        self.id = json['id']
        self.entities = json['entities']

    def __repr__(self):
        return '<TwitterToReddit.utils.Tweet ({0})>'.format(self.id)


class StdOutListener(tweepy.StreamListener):
    """ Handles data received from the stream.
        http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html """

    def on_data(self, data):
        tweet_json = json.loads(data)
        print(tweet_json)

        tweet = Tweet(tweet_json)

        if twitter_user_id == '' or tweet.user['id'] != twitter_user_id:
            # Check if user is given and if true, then it should equal the tweet author;
            # otherwise we will return True
            return True

        image_url = extract_image_url(tweet)
        if image_url == '':
            # image_url = tweet.$LINK
            # todo use normal tweet link then
            return True

        submit_to_reddit(image_url)

        return True  # To continue listening

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening


def main():
    if subreddit == '':
        logging.critical("no subreddit given")
        return

    listener = StdOutListener()

    stream = tweepy.Stream(twitter_auth, listener)
    if twitter_hashtag != '':
        stream.filter(track=[twitter_hashtag])
    elif twitter_user_id != '':
        stream.filter(follow=[twitter_user_id])
    else:
        logging.warning("No filter given! Either 'twitter_user_id' or 'twitter_hashtag' should have a valid value!")
