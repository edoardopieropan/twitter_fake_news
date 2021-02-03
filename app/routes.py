# todo: alcuni tweet potrebbero non essere più disponibili, visualizzarli con card normale e aggiungere disclaimer
# todo: se arrivo in una qualsiasi view function con la sessione settata poppo l'utente
# todo: aggiungere messaggi di errore se vado in una pagina senza permesso
# todo: il calcolo dei metodi viene fatto alla creazione del set, non ha senso farlo dopo
# todo: aggiungere generazione form dinamica, salvato il segnalibro con spiegazioni
# todo: salvare in json utente/sessione sia timestamp inizio che fine


from app import app
from flask import render_template, request, flash, redirect, session, url_for

from app.scripts.get_tweets import create_tweets_set
from app.scripts import websitescraping
from app.scripts import nlp

from app.forms import TweetsSetDownloadForm, UserForm

from app.utils import load_csv, write_csv, append_to_csv, load_json, write_json

from datetime import datetime
import os


# defining home page
@app.route("/")
@app.route("/index")
def index():
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
        create_tweets_set(new_set_id, form.search_keyword.data, int(form.tweets_number.data))
        data.append(new_set)
        write_json(app.config['TWEETS_SETS_FILE'], data)
        return redirect(url_for("download_tweets_sets"))

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
        return redirect(url_for("index"))
    tweets_sets = [(ts['id'], ts['id']) for ts in tweets_sets]
    form = UserForm()
    form.tweets_set_to_use.choices = tweets_sets
    if form.validate_on_submit():
        new_user_id = form.username.data.replace(" ", "_") + "_" + str(int(datetime.timestamp(datetime.now())))
        new_user = {"id": new_user_id,
                    "username": form.username.data,
                    "tweets_set": form.tweets_set_to_use.data,
                    "test_timestamp": int(datetime.timestamp(datetime.now()))}
        data.append(new_user)
        write_json(app.config['USERS_FILE'], data)

        session["user_id"] = new_user_id
        session["tweets_set"] = form.tweets_set_to_use.data

        return redirect(url_for("test_tweets"))

    return render_template("start_test.html", form=form)


@app.route('/test_tweets', methods=['GET', 'POST'])
def test_tweets():
    if "user_id" not in session:
        return redirect(url_for("start_test"))

    tweets_set = load_json(os.path.join(app.config["TWEETS_SETS_DIR"], session["tweets_set"] + ".json"))

    # return test_tweets.html and list and length of list to html page
    return render_template("test_tweets.html", set_length=len(tweets_set), tweets=tweets_set)


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