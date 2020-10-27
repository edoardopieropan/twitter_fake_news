# Twitter Fake News - Fact Checking

### __University project - Semantic Web__
Project for automatic fact-checking of italian Twitter fake news.

## What is it?

This test application let you see some tweets received using [*Tweepy*](http://docs.tweepy.org/en/latest/) and let you choose for each one if in your opinion that could be potentially a fake news. Algorithm of POS tagging and analysis will try to automatically detect fake news tweets comparing the news in italian *fact-checking* sites. Currently using website scraping methods we retrive fake news from [bufale.net](https://www.bufale.net/bufala/) and [BUTAC](https://www.butac.it/category/bufala/).
## Setup & Run

Twitter needs a developer authentication for use their APIs, so before start request your keys at https://developer.twitter.com/ it will take about 14 days according to Twitter. Once ready you will access on the project page and have the *Consumer Keys* and *Authentication Tokens*.

Download this repository.
Copy your keys and tokens in the *twitter_keys.txt* file in the order:
1. consumer_key
1. consumer_secret
1. access_token
1. access_token_secret

You can now set the hasthtag and how many tweet to receive in the *main.py* file, in this case we are looking for #news and 8 tweets:

```python
list_tweets = get_tweets.get("news", 8)
```
If you want retweets to be received you need to delete the text `"-filter:retweets"` in *get_tweets.py*. Note that the text of retweeted messages will be truncaded by the API.

For language analysis we use [spaCy](https://spacy.io/usage) ([Github](https://github.com/explosion/spaCy)), a free open-source library for advanced Natural Language Processing (NLP) in Python. It supports also the Italian language. Beginners can have a look at https://spacy.io/usage/spacy-101.
To install spaCy on your machine you can run those commands on your terminal:
```
pip3 install spacy
python3 -m spacy download it_core_news_sm
```
in this case we are downloading the italian model.

Finally to test this application install the requirements and run
```
python3 main.py
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
