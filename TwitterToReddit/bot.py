import praw
import tweepy

import json
import datetime

from TwitterToReddit import constants

# http://gettwitterid.com/
twitter_user_id = '109850283'
# optional:
twitter_hashtag = '#uploadplan'
subreddit = 'l3d00m'

r = praw.Reddit(user_agent="Twitter X-Poster by l3d00m")
r.set_oauth_app_info(client_id=constants.reddit_client_id, client_secret=constants.reddit_client_secret,
                     redirect_uri="http://127.0.0.1")


class Tweet(object):
    def __init__(self, json):
        if 'delete' in json:
            print("is deleted")
            return
        self.text = json['text']
        self.user = json['user']
        self.user_id = self.user['id']
        self.id = json['id']
        self.entities = json['entities']

    def __repr__(self):
        return '<TwitterToReddit.__init__.Tweet ({0})>'.format(self.id)


def extract_image(tweet):
    """
    Source: https://github.com/joealcorn/TweetPoster
    :param tweet: Tweet Object to get the link from
    """

    print("rehosting images")
    if 'media' in tweet.entities:
        for media in tweet.entities['media']:
            if media['type'] != 'photo':
                print("media is not image")
                continue

            url = media['media_url']
            reddit(url)


def reddit(url):
    """ https://praw.readthedocs.org/en/stable/pages/oauth.html
    :param url: Url to add to the reddit link post
    """

    # https://praw.readthedocs.org/en/stable/pages/oauth.html#step-4-exchanging-the-code-for-an-access-token-and-a-refresh-token
    # Get an access token:
    #
    # url = r.get_authorize_url('uniqueKey', 'submit', True)
    # import webbrowser
    # webbrowser.open(url)

    # https://praw.readthedocs.org/en/stable/pages/oauth.html#step-6-refreshing-the-access-token
    # Copy the access token and get the refresh token
    #
    # access_information = r.get_access_information('CODE YOU GOT ABOVE')
    # print(access_information['refresh_token'])

    if url == '':
        print("url is emtpy")
        return

    # use the refresh token:
    r.refresh_access_information(constants.reddit_client_refresh)

    now = datetime.datetime.now()
    print("Submitting \"" + url + "\" to" + subreddit)
    r.submit(subreddit,
             'Uploadplan vom ' + str(now.day) + "." + str(now.month) + "." + str(now.year)
             # + " um "+ str(now.hour) + ":" + str(now.minute)
             , url=url)


class StdOutListener(tweepy.StreamListener):
    """ Handles data received from the stream.
        http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html """

    def on_data(self, data):
        # Prints the text of the tweet
        print(data)
        tweet = Tweet(json.loads(data))
        if tweet.user_id == twitter_user_id:
            extract_image(tweet)

        return True  # To continue listening

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True  # To continue listening


def main():
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(constants.twitter_consumer_key, constants.twitter_consumer_key_secret)
    auth.set_access_token(constants.twitter_access_token, constants.twitter_access_token_secret)

    stream = tweepy.Stream(auth, listener)
    if twitter_hashtag != '':
        stream.filter(follow=[twitter_user_id], track=[twitter_hashtag])
    else:
        stream.filter(follow=[twitter_user_id])
