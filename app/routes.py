# todo: finire metodi con nuova modalità


# note: cambiato metodo salvataggio lista utenti

from app import app
from flask import render_template, request, flash, redirect, session, url_for

from app.scripts.get_tweets import create_tweets_set

from app.forms import TweetsSetDownloadForm, UserForm, TestForm
from wtforms import RadioField
from wtforms.validators import InputRequired

from app.utils import load_csv, write_csv, append_to_csv, load_json, write_json

from datetime import datetime
import os


# defining home page
@app.route("/")
@app.route("/index")
def index():
    if "session_id" in session:
        return redirect(url_for("test_tweets"))
    return render_template("index.html")


@app.route("/download_tweet_sets", methods=['GET', 'POST'])
def download_tweet_sets():
    if "session_id" in session:
        return redirect(url_for("test_tweets"))

    if os.path.exists(app.config['TWEETS_SETS_FILE']):
        data = load_json(app.config['TWEETS_SETS_FILE'])
    else:
        data = []

    form = TweetsSetDownloadForm()
    if form.validate_on_submit():
        new_set_id = form.set_name.data.replace(" ", "_") + "_" + str(int(datetime.timestamp(datetime.now())))
        new_set = {"id": new_set_id,
                   "set_name": form.set_name.data,
                   "search_query": form.search_query.data,
                   "tweets_number": int(form.tweets_number.data),
                   "bufale_pages": int(form.bufale_pages.data)}
        create_tweets_set(new_set_id, form.search_query.data, int(form.tweets_number.data), int(form.bufale_pages.data))
        data.append(new_set)
        write_json(app.config['TWEETS_SETS_FILE'], data)
        return redirect(url_for("download_tweet_sets"))

    return render_template("tweets_set_download.html", form=form, tweets_sets=data[::-1])


@app.route('/start_test', methods=['GET', 'POST'])
def start_test():
    if "session_id" in session:
        return redirect(url_for("test_tweets"))

    if os.path.exists(app.config['SESSIONS_FILE']):
        data = load_json(app.config['SESSIONS_FILE'])
    else:
        data = []

    # creating the choices for the select field
    if os.path.exists(app.config['TWEETS_SETS_FILE']):
        tweets_sets = load_json(app.config['TWEETS_SETS_FILE'])
    else:
        return redirect(url_for("download_tweet_sets"))

    tweets_sets = [(ts['id'], ts['id'] + " (" + ts["search_query"] + ")") for ts in tweets_sets[::-1]]
    form = UserForm()
    form.tweets_set_to_use.choices = tweets_sets
    if form.validate_on_submit():
        new_session_id = form.username.data.replace(" ", "_") + "_" + str(int(datetime.timestamp(datetime.now())))
        new_session = {"id": new_session_id,
                       "username": form.username.data,
                       "age": form.age.data,
                       "gender": form.gender.data}
        data.append(new_session)
        write_json(app.config['SESSIONS_FILE'], data)

        session["session_id"] = new_session_id
        session["username"] = form.username.data
        session["age"] = form.age.data
        session["gender"] = form.gender.data
        session["tweets_set_id"] = form.tweets_set_to_use.data
        session["start_timestamp"] = int(datetime.timestamp(datetime.now()))

        return redirect(url_for("test_tweets"))

    return render_template("start_test.html", form=form)


@app.route('/test_tweets', methods=['GET', 'POST'])
def test_tweets():
    if "session_id" not in session:
        return redirect(url_for("start_test"))

    tweets_set = load_json(os.path.join(app.config["TWEETS_SETS_DIR"], session["tweets_set_id"] + ".json"))

    class DynamicTestForm(TestForm):
        pass

    for t in tweets_set:
        field = RadioField(t["progressive"], choices=[("True", "True"), ("Maybe", "Maybe"), ("Fake", "Fake")], id=t["id"],
                           validators=[InputRequired()])
        setattr(DynamicTestForm, t["progressive"], field)

    form = DynamicTestForm()

    if form.validate_on_submit():
        user_choices = {}
        for t in tweets_set:
            user_choices[t["id"]] = form[t["progressive"]].data

        user_session = {"id": session["session_id"],
                        "username": session["username"],
                        "age": session["age"],
                        "gender": session["gender"],
                        "tweets_set_id": session["tweets_set_id"],
                        "start_timestamp": session["start_timestamp"],
                        "finish_timestamp": int(datetime.timestamp(datetime.now())),
                        "user_choices": user_choices}

        write_json(os.path.join(app.config['SESSIONS_DIR'], session["session_id"] + ".json"), user_session)
        return redirect(url_for("results"))

    # return test_tweets.html and list and length of list to html page
    return render_template("test_tweets.html", set_length=len(tweets_set), tweets=tweets_set, form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    if "session_id" not in session:
        return redirect(url_for("start_test"))

    session.pop("session_id")
    session.pop("username")
    session.pop("age")
    session.pop("gender")
    session.pop("tweets_set_id")
    session.pop("start_timestamp")

    return render_template("results.html")
