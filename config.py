import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nopenopesorry'
    API_KEY = "bkb3u2pn4UTrNow1C14decjBV"
    API_SECRET = "GDtds66AA927ahj1D5ovYCrN3CTFO1htzj9BQkiOHc9Sek5Er0"

    TWEETS_SETS_JSON = os.path.join("data", "tweets_sets.json")
    USERS_JSON = os.path.join("data", "users.json")

    TWEETS_SETS_DIR = os.path.join("data", "tweets_sets", "")
    USERS_DIR = os.path.join("data", "users", "")

    ACCESS_TOKEN = ""
    ACCESS_TOKEN_SECRET = ""
