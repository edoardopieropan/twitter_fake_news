from app import app
from flask import render_template
from flask import request

from app.scripts import get_tweets
from app.scripts import websitescraping
from app.scripts import nlp

import datetime
import json

# list of tweets
list_sources, list_tweets_text, list_times, list_ids = [], [], [], []

list_tweets = get_tweets.get("bufala", 8)
for tweet in list_tweets:
    list_sources.append(tweet[0])
    list_tweets_text.append(tweet[1])
    list_times.append(tweet[2])
    list_ids.append(tweet[3])


# defining home page
@app.route('/')
@app.route('/index')
def homepage():
    # returning index.html
    return render_template("index.html")

@app.route('/tweets')
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

    bufale = websitescraping.get_bufale(2)
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
    time = str(datetime.datetime.now())

    choices.update({"results":app_results})

    wrapper={time:choices}

    ## Save file
    # with open("data.json",'a+') as f: 
    #     json.dump(wrapper, f, ensure_ascii=False, indent=4)
    #     print("File updated...")