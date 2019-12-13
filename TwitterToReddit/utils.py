import datetime
import logging

import praw


from TwitterToReddit import constants

reddit = praw.Reddit(client_id=constants.reddit_client_id,
                     client_secret=constants.reddit_client_secret,
                     refresh_token=constants.reddit_client_refresh,
                     user_agent="Twitter X-Poster by l3d00m")


def extract_image_url(tweet):
    """
    :param tweet: Tweet Object to get the link from
    :return The direct link to the Tweet's image if available
    """

    logging.debug("extracting images")
    if 'media' in tweet.entities:
        logging.debug("tweet entities has media")
        for media in tweet.entities['media']:
            if media['type'] != 'photo':
                logging.info("media is not image")
                continue

            return media['media_url_https']

    logging.info("Couldn't find any media")
    return ''


def submit_to_reddit(url):
    """
    Posts a link to the given subreddit
    :param url: Url to add to the reddit link post
    """
    from TwitterToReddit.bot import subreddit

    if url == '':
        logging.warning("url is emtpy")
        return

    now = datetime.datetime.now()
    title = 'Tweet at ' + str(now.day) + "." + str(now.month) + "." + str(now.year)

    logging.info("Submitting \"" + url + "\" to" + subreddit + ". Title is: " + title)

    # Submit the post
    reddit.subreddit(subreddit).submit(title=title, url=url)
