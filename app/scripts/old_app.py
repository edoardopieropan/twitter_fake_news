from flask import Flask, render_template 
import get_tweets
import nlp
import websitescraping

NUM_PAGES = 2

# declaring app name 
app = Flask(__name__) 
  
# list of tweets
list_sources, list_tweets_text, list_times = [],[],[]

list_tweets = get_tweets.get("news", 8)
for tweet in list_tweets:
    list_sources.append(tweet[0])
    list_tweets_text.append(tweet[1])
    list_times.append(tweet[2])
  
# defining home page 
@app.route('/') 
def homepage(): 
  
# returning index.html and list 
# and length of list to html page 
    return render_template("index.html", len = len(list_tweets), list_tweets = list_tweets_text, list_sources = list_sources, list_times = list_times) 

@app.route('/results')
def results():
    bufale = websitescraping.get_bufale(NUM_PAGES)
    results = []
    for t in list_tweets_text:
        results_tmp = []
        for b in bufale:
            results_tmp.append(float(round(nlp.get_similarity(t, b)*100, 2)))
        results.append(max(results_tmp))

    return render_template("results.html", len = len(list_tweets), list_tweets = list_tweets_text, list_sources = list_sources, list_times = list_times, list_results = results)

if __name__ == "__main__":

# running app 
    app.static_folder = 'static'
    app.run(host="localhost", use_reloader = True, debug = True) 