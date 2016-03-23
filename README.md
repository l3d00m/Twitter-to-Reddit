# Twitter to Reddit
Simple python bot that crossposts Tweets to reddit

# Setup
Add a constants.py file in the subdirectory that looks like the following and add your keys.

```
global reddit_client_id
global reddit_client_secret
global reddit_client_refresh
global reddit_redirect_uri
global twitter_consumer_key
global twitter_consumer_key_secret
global twitter_access_token
global twitter_access_token_secret

# https://apps.twitter.com/app/new
twitter_consumer_key = ''
twitter_consumer_key_secret = ''
twitter_access_token = ''
twitter_access_token_secret = ''

# https://www.reddit.com/prefs/apps/
reddit_client_id = ''
reddit_client_secret = ''
reddit_redirect_uri = '"'
reddit_client_refresh = '' # Look below how to get the refresh token
```


# Get reddit refresh token
1) Setup a reddit client:
```
import praw
r = praw.Reddit(user_agent="USER AGENT")
r.set_oauth_app_info(client_id=reddit_client_id, client_secret=reddit_client_secret, redirect_uri=reddit_redirect_uri)
```

2) Get an access token:

```
url = r.get_authorize_url('uniqueKey', 'submit', True)
import webbrowser
webbrowser.open(url)
# Copy the access token from the addressbar
```


3) Get the refresh token from the access token:
```
access_information = r.get_access_information('ACCESS TOKEN YOU GOT ABOVE')
print(access_information['refresh_token'])
```

[Source](https://praw.readthedocs.org/en/stable/pages/oauth.html)
