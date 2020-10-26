import tweepy as tw
from pathlib import Path

#return n tweets containing the given hashtag 
def get(hashtag, n):

    #import twitter api keys
    filename = Path(__file__).parent / "../twitter_keys.txt"
    with filename.open() as f:
        keys = f.readlines()
        consumer_key = keys[0].strip("\n") #consumer_key
        consumer_secret = keys[1].strip("\n") #consumer_secret
        access_token = keys[2].strip("\n") #access_token
        access_token_secret = keys[3].strip("\n") #access_token_secret

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    search_words = "#" + hashtag + "-filter:retweets"
    date_since = "2020-10-25"

    # Collect tweets
    tweets = tw.Cursor(api.search,
                tweet_mode="extended",
                q=search_words,
                lang="it",
                since=date_since).items(n)

    return [[tweet.user.screen_name, tweet.full_text, tweet.created_at] for tweet in tweets]
