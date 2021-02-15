# Twitter Fake News - Fact Checking 
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

### __University project - Semantic Web__
Development of a web application based on Python and Flask for automatic *fact-checking* between tweets from Italy and two famous italian news debunkers.

## What is it?

This application let you download some tweets using [*Tweepy*](http://docs.tweepy.org/en/latest/) and test what a person think of a certain tweet: is it a fake news or not?
An algorithm of POS tagging and analysis based on [spaCy](https://spacy.io/usage) will try to automatically detect if a tweet is/talk about a fake news, comparing it with italian articles from *fact-checking* websites. Currently, using website scraping methods, 
we retrieve fake news debunking articles from [bufale.net](https://www.bufale.net/bufala/) and [BUTAC](https://www.butac.it/category/bufala/).

## Setup & Run

### Twitter Developer APIs
Twitter needs a developer authentication for use their APIs. Before start, please make sure to request your keys at https://developer.twitter.com/. Notice that it will take about 14 days according to Twitter.

Clone this repository.
Copy your keys in the *config.py* file. You will need:
1. consumer_key
1. consumer_secret

### Run the app
Create a virtual environment:
```bash
python3 -m venv project-venv/
```
activate it:
```bash
source venv/bin/activate
```
then install the requirements:
```bash
pip install -r requirements.txt
```
For language analysis we use [spaCy](https://spacy.io/usage) ([Github](https://github.com/explosion/spaCy)), a free open-source library for advanced Natural Language Processing (NLP) in Python. It supports also the Italian language. Beginners can have a look at https://spacy.io/usage/spacy-101.

To install spaCy on your machine you can run those commands on your terminal:
```bash
pip install -U spacy
python -m spacy download it_core_news_lg
```
in this case we are downloading the italian model <sup>1</sup>.

<sub><sup>1</sup> the *_lg* model supports multi-task CNN trained on UD Italian ISDT and WikiNER. Assigns context-specific token vectors, POS tags, dependency parses and named entities. The shorter model *_sm* was not enough for some advanced analysis.</sub>

For running the application:
```bash
flask run
```
then you can open the website at `localhost:5000` on your browser.


## Application structure

### > Homepage
The homepage contains some instruction explaining what the tester is meant to do.
When you launch the application for the first time you have to download some tweets using the form in the Tweet Sets page.
Once you collect some sets, you can start a new test from the Start Test page.

### > Tweet sets
An **administration page** for managing tweet sets. 

To download a new set you have to specify:
1. Name of the set
1. A search query (with or without hastags, e.g. #word, hello world, etc.)
1. Number of tweets 

When the submit button is pressed the application will add the new set in a *.json* containing all the previously downloaded sets:
```json
[
    {
        "id": "amadeus_1612474452",
        "set_name": "amadeus",
        "search_keyword": "sanremo",
        "tweets_number": 5
    },
    {
        "id": "covid_1612630237",
        "set_name": "covid",
        "search_query": "vaccini",
        "tweets_number": 5
    }
]
```
Note that the set id is the concatenation of the name and the creation timestamp.

The code will now compare all the founded tweets with articles from two fact-checking italian websites. 
The similarity methods are the following:

1. exp1: stop-words and punctuation removal + lemmatization. The tweet is compared with the article's **title**.
1. exp2: stop-words and punctuation removal + lemmatization. The tweet is compared with the article's **body**.
1. exp3: keep only nouns. The tweet is compared with the article's **title**.
1. exp4: keep only nouns. The tweet is compared with the article's **body**.
1. exp5: stop-words and punctuation removal + lemmatization. If len(tweet) = n, the tweet is compared with the first n words in the article's **body**.
1. exp6: stop-words and punctuation removal + lemmatization. The tweet is compared with the 30% of the words from the article's **body** with the greatest TF-IDF index.

Finally, the results will be stored in set specific *.json* file, structured like the following:
```json
[
    {
        "source": "tweet_author",
        "text": "This is a tweet!",
        "created_at": "2021-02-10 15:58:46",
        "id": 1359532267572453377,
        "progressive": "t0",
        "fact_checking": {
            "exp1": {
                "similarity": 0.58,
                "fn_url": "https://www.bufale.net/link_to_the article"
            },
            "exp2": {
                "similarity": 0.6,
                "fn_url": "https://www.bufale.net/link_to_the article"
            },
            "exp3": {
                "similarity": 0.39,
                "fn_url": "https://www.bufale.net/link_to_the article"
            },
            "exp4": {
                "similarity": 0.57,
                "fn_url": "https://www.bufale.net/link_to_the article"
            }
        }
    }
]
```
Each tweet in the *.json* contains information about the source, the text, the similarity obtained from the methods and for every experiment the url for the article with the higher similarity.

### > Test page
The subject is requested to choose a username and a **tweet set**, from those previously downloaded.

The tweets contained in the selected set will be displayed and the user will choose for each tweet between *True*, *Maybe* and *Fake*.

After finishing the test, a *.json* containing all the session info is saved:
```json
{
    "id": "andrea_1612475354",
    "username": "andrea",
    "tweets_set_id": "covid_1612630237",
    "start_timestamp": 1612973659,
    "finish_timestamp": 1612973701,
    "user_choices": {
        "1359532267572453377": "Maybe",
        "1358095041076617217": "Fake",
        "1358094894586359809": "True",
        "1358094801757999107": "Maybe",
        "1358094548744998913": "True"
    }
}
```
and the user is added to a *.json* containing all the test sessions:
```json
[
    {
        "id": "andrea_1612475354",
        "username": "andrea"
    },
    {
        "id": "edoardo_1612475580",
        "username": "edoardo"
    }
]
```
Note that a user/session id is the concatenation of the username and the start timestamp.

## License
Before use it we invite you to read the LICENSE.<br >

This file is distributed under the terms of the __GNU General Public License v3.0__<br >
Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. __Copyright and license notices must be preserved__. Contributors provide an express grant of patent rights.<br><hr>
Visit <http://www.gnu.org/licenses/> for further information.<br >

## References

***Web Semantico*** <br >
A.Y. 2019/2020 <br>
University of Verona (Italy) <br > <br >
Repository Authors: <br >
**Edoardo Pieropan** <br>
**Andrea Toaiari**
