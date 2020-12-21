# Twitter Fake News - Fact Checking

### __University project - Semantic Web__
Project for automatic fact-checking of italian Twitter fake news.

## What is it?

This test application let you see some tweets received using [*Tweepy*](http://docs.tweepy.org/en/latest/) and let you choose for each one if in your opinion that could be potentially a fake news. Algorithm of POS tagging and analysis will try to automatically detect fake news tweets comparing the news in italian *fact-checking* sites. Currently using website scraping methods we retrive fake news from [bufale.net](https://www.bufale.net/bufala/) and [BUTAC](https://www.butac.it/category/bufala/).
## Setup & Run

### Twitter
Twitter needs a developer authentication for use their APIs, so before start request your keys at https://developer.twitter.com/ it will take about 14 days according to Twitter. Once ready you will access on the project page and have the *Consumer Keys* and *Authentication Tokens*.

Download this repository.
Copy your keys and tokens in the *config.py* file. You will need:
1. consumer_key
1. consumer_secret
1. access_token
1. access_token_secret

You can set the hasthtag and how many tweet to receive in the *routes.py* file.

If you want retweets to be received you need to delete the text `"-filter:retweets"` in *get_tweets.py*. Note that the text of retweeted messages will be truncaded by the API.

### Natural Language Processing (NLP)
For language analysis we use [spaCy](https://spacy.io/usage) ([Github](https://github.com/explosion/spaCy)), a free open-source library for advanced Natural Language Processing (NLP) in Python. It supports also the Italian language. Beginners can have a look at https://spacy.io/usage/spacy-101.
To install spaCy on your machine you can run those commands on your terminal:
```
pip install -U spacy
python3 -m spacy download it_core_news_md
```
in this case we are downloading the italian model <sup>1</sup>.

The analysis will be done by *nlp.py*.

<sub><sup>1</sup> the *_md* model supports multi-task CNN trained on UD Italian ISDT and WikiNER. Assigns context-specific token vectors, POS tags, dependency parses and named entities. The shorter model *_sm* was not enough for some advanced analysis.</sub>

### Run the app
Finally to test this application install the requirements 
then export FLASK_APP with
```
export FLASK_APP=twitter_fake_news.py
```
then launch flask
```
flask run
```
then open `localhost:5000` on your browser.

## License
Before use it we invite you to read the LICENSE.<br >

This file is distributed under the terms of the __GNU General Public License v3.0__<br >
Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. __Copyright and license notices must be preserved__. Contributors provide an express grant of patent rights.<br><hr>
Visit <http://www.gnu.org/licenses/> for further information.<br >

## References

***Web Semantico*** <br >
A.Y. 2019/2020 <br >
University of Verona (Italy) <br > <br >
Repository Authors: <br >
**Edoardo Pieropan** <br>
**Andrea Toaiari**
