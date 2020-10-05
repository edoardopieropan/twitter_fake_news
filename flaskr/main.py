# importing modules 
from flask import Flask, render_template 
  
# declaring app name 
app = Flask(__name__) 
  
# list of tweets
list_tweets =["SpaceX training of astronauts that will fly on board Dragon’s first operational mission is complete! When the crew arrives for pre-launch preparations at the launch site, they will participate in a run-through of day-of-launch activities with the launch and pad operations teams", "Charizard", "Squirtle", "Jigglypuff",  
           "Bulbasaur", "Bulbasaur"] 
  
# defining home page 
@app.route('/') 
def homepage(): 
  
# returning index.html and list 
# and length of list to html page 
    return render_template("index.html", len = len(list_tweets), list_tweets = list_tweets) 
  
if __name__ == "__main__":

# running app 
    app.static_folder = 'static'
    app.run(use_reloader = True, debug = True) 