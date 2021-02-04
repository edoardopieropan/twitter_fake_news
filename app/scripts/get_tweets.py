import tweepy as tw
from app import app
import os

from app.utils import write_json, load_json


# return n tweets containing the given hashtag
def get_tweets(search_query, n):
    auth = tw.OAuthHandler(app.config['API_KEY'], app.config['API_SECRET'])
    auth.set_access_token(app.config['ACCESS_TOKEN'], app.config['ACCESS_TOKEN_SECRET'])
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search query and the date_since date as variables
    search_query = search_query + "-filter:retweets"
    date_since = "2021-01-01"

    # Collect tweets
    tweets = tw.Cursor(api.search,
                       tweet_mode="extended",
                       q=search_query,
                       lang="it",
                       since=date_since).items(n)

    return [[tweet.user.screen_name, tweet.full_text, tweet.created_at, tweet.id] for tweet in tweets]


def create_tweets_set(new_set_id, search_keyword, num_tweets):
    # list of tweets
    tweets = []
    list_sources, list_tweets_text, list_times, list_ids = [], [], [], []

    list_tweets = get_tweets(search_keyword, num_tweets)
    for i, tweet in enumerate(list_tweets):
        list_sources.append(tweet[0])
        list_tweets_text.append(tweet[1])
        list_times.append(tweet[2])
        list_ids.append(tweet[3])
        t = {"source": tweet[0],
             "text": tweet[1],
             "created_at": tweet[2].strftime("%Y-%m-%d %H:%M:%S"),
             "id": tweet[3],
             "progressive": f"t{i}"}
        tweets.append(t)

    write_json(os.path.join(app.config['TWEETS_SETS_DIR'], new_set_id + ".json"), tweets)
