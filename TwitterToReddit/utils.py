import datetime
import logging

from TwitterToReddit import constants
from TwitterToReddit.bot import subreddit, reddit_auth


def extract_image_url(tweet):
    """
    :param tweet: Tweet Object to get the link from
    :return The direct link to the Tweet's image if available
    """

    print("extracting images")
    if 'media' in tweet.entities:
        for media in tweet.entities['media']:
            if media['type'] != 'photo':
                print("media is not image")
                continue

            return media['media_url']

    return ''


def submit_to_reddit(url):
    """
    Posts a link to the given subreddit
    :param url: Url to add to the reddit link post
    """

    if url == '':
        logging.warning("url is emtpy")
        return

    now = datetime.datetime.now()
    title = 'Uploadplan vom ' + str(now.day) + "." + str(now.month) + "." + str(now.year)

    logging.info("Submitting \"" + url + "\" to" + subreddit + ". Title is: " + title)

    # use the refresh token to get new access information regularly (at least every hour):
    reddit_auth.refresh_access_information(constants.reddit_client_refresh)
    # Submit the post
    post_url = reddit_auth.submit(subreddit, title, url=url)

    logging.info("Submitted the post, url is " + post_url)