import tweepy as tw
from app import app


# return n tweets containing the given hashtag
def get(hashtag, n):
    auth = tw.OAuthHandler(app.config['API_KEY'], app.config['API_SECRET'])
    auth.set_access_token(app.config['ACCESS_TOKEN'], app.config['ACCESS_TOKEN_SECRET'])
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
