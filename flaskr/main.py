from flask import Flask, render_template 
import get_tweets
  
# declaring app name 
app = Flask(__name__) 
  
# list of tweets
list_sources, list_tweets_text, list_times = [],[],[]

list_tweets = get_tweets.get("news",8)
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
  
if __name__ == "__main__":

# running app 
    app.static_folder = 'static'
    app.run(use_reloader = True, debug = True) 