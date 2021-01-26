from app import app
from flask import render_template, request, flash, redirect

from app.scripts import get_tweets
from app.scripts import websitescraping
from app.scripts import nlp

from app.forms import TweetsSetDownloadForm, UserForm

from app.utils import load_csv, write_csv, append_to_csv, load_json, write_json

from datetime import datetime
import os

NUM_PAGES = 2


def create_tweet_set(new_set_id, search_keyword, num_tweets):
    # list of tweets
    tweets = []
    list_sources, list_tweets_text, list_times, list_ids = [], [], [], []

    list_tweets = get_tweets.get(search_keyword, num_tweets)
    for tweet in list_tweets:
        list_sources.append(tweet[0])
        list_tweets_text.append(tweet[1])
        list_times.append(tweet[2])
        list_ids.append(tweet[3])
        t = {"source": tweet[0],
             "text": tweet[1],
             "created_at": tweet[2].strftime("%Y-%m-%d %H:%M:%S"),
             "id": tweet[3]}
        tweets.append(t)

    write_json(os.path.join(app.config['TWEETS_SETS_DIR'], new_set_id + ".json"), tweets)


# defining home page
@app.route("/")
@app.route("/index")
def homepage():
    # returning index.html
    return render_template("index.html")


@app.route("/download_tweets_sets", methods=['GET', 'POST'])
def download_tweets_sets():
    form = TweetsSetDownloadForm()
    if os.path.exists(app.config['TWEETS_SETS_FILE']):
        data = load_json(app.config['TWEETS_SETS_FILE'])
    else:
        data = []
    if form.validate_on_submit():
        new_set_id = form.set_name.data.replace(" ", "_") + "_" + str(int(datetime.timestamp(datetime.now())))
        new_set = {"id": new_set_id,
                   "set_name": form.set_name.data,
                   "search_keyword": form.search_keyword.data,
                   "tweets_number": int(form.tweets_number.data)}
        create_tweet_set(new_set_id, form.search_keyword.data, int(form.tweets_number.data))
        data.append(new_set)
        write_json(app.config['TWEETS_SETS_FILE'], data)
        return redirect('/download_tweets_sets')

    return render_template("tweets_set_download.html", form=form, tweets_sets=data)


@app.route('/start_test', methods=['GET', 'POST'])
def start_test():
    if os.path.exists(app.config['USERS_FILE']):
        data = load_json(app.config['USERS_FILE'])
    else:
        data = []
    # creating the choices for the select field
    if os.path.exists(app.config['TWEETS_SETS_FILE']):
        tweets_sets = load_json(app.config['TWEETS_SETS_FILE'])
    else:
        # TODO: add error message, create at least one tweets set
        return redirect("/index")
    tweets_sets = [(ts['id'], ts['id']) for ts in tweets_sets]
    form = UserForm()
    form.tweets_set_to_use.choices = tweets_sets
    if form.validate_on_submit():
        new_user_id = form.username.data.replace(" ", "_") + "_" + str(int(datetime.timestamp(datetime.now())))
        new_user ={"id": new_user_id,
                   "username": form.username.data,
                   "tweets_set": form.tweets_set_to_use.data,
                   "test_timestamp": int(datetime.timestamp(datetime.now()))}
        data.append(new_user)
        write_json(app.config['USERS_FILE'], data)
        return redirect("/start_test")

    return render_template("start_test.html", form=form)



@app.route('/tweets', methods=['GET'])
def tweetPage():
    # returning list_tweets.html and list
    # and length of list to html page
    return render_template("list_tweets.html", len=len(list_tweets), list_tweets=list_tweets_text, list_sources=list_sources,
                           list_times=list_times, list_ids=list_ids)


@app.route('/results', methods=['POST'])
def results():
    user_choices={}
    if request.method == 'POST':
        user_choices=request.get_json()

    bufale = websitescraping.get_bufale(NUM_PAGES)
    results = []
    for t in list_tweets_text:
        results_tmp = []
        for b in bufale:
            results_tmp.append(float(round(nlp.get_similarity(t, b) * 100, 2)))
        results.append(max(results_tmp))

    save_results(user_choices, results)

    return render_template("results.html", len=len(list_tweets), list_tweets=list_tweets_text,
                           list_sources=list_sources, list_times=list_times, list_results=results, list_ids=list_ids)


def save_results(choices, app_results):
    time = str(datetime.now())

    choices.update({"results":app_results})

    wrapper={time:choices}

    ## Save file
    # with open("data.json",'a+') as f: 
    #     json.dump(wrapper, f, ensure_ascii=False, indent=4)
    #     print("File updated...")