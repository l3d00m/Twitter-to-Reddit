# Twitter to Reddit
Simple python bot that crossposts tweets with a specific hashtag/user to reddit

# Setup
Add a constants.py file in the subdirectory that looks like the following and add your keys.

```
global reddit_client_id
global reddit_client_secret
global reddit_client_refresh
global twitter_consumer_key
global twitter_consumer_key_secret

# From here: https://apps.twitter.com/app/new
twitter_consumer_key = ''
twitter_consumer_key_secret = ''

# From here: https://www.reddit.com/prefs/apps/
reddit_client_id = ''
reddit_client_secret = ''
reddit_redirect_uri = ''
reddit_client_refresh = '' # Look below how to get the refresh token
```


## Get reddit refresh token
Just follow the steps on [this site](https://grant.outofindex.com/reddit), which I find super helpful. The needed scope is `submit`.

Alternatively [here](https://praw.readthedocs.io/en/v6.4.0/tutorials/refresh_token.html#refresh-token) is the provided tutorial by the `praw`-Library 

# Run the bot

`python main.py`