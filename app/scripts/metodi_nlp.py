import re
import spacy
import string
from spacy.lang.it import STOP_WORDS

import websitescraping
import json


def load_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
        return data


def write_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


nlp = spacy.load('it_core_news_lg')


def deEmojify(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def preprocess(doc1, doc2):
    # remove emojis
    doc1 = deEmojify(doc1)
    doc2 = deEmojify(doc2)

    # remove punctuation
    doc1 = doc1.translate(str.maketrans('', '', string.punctuation))
    doc2 = doc2.translate(str.maketrans('', '', string.punctuation))

    # remove stopwords
    # doc1 = doc1.split()
    # for word in doc1:
    #     if 'http' in word:
    #         doc1.remove(word)
    #     elif word in STOP_WORDS:
    #         doc1.remove(word)
    #
    # doc2 = doc2.split()
    # for word in doc2:
    #     if 'http' in word:
    #         doc2.remove(word)
    #     elif word in STOP_WORDS:
    #         doc2.remove(word)
    #
    # doc1 = ' '.join(map(str, doc1))
    # doc2 = ' '.join(map(str, doc2))
    return doc1, doc2


def get_similarity(doc1, doc2, method):
    # doc1 = doc1.__str__()
    # doc2 = doc2.__str__()
    doc1, doc2 = preprocess(doc1, doc2)
    doc1 = nlp(doc1)
    doc2 = nlp(doc2)
    doc1 = nlp(' '.join([str(w) for w in doc1 if not w.is_stop]))
    doc2 = nlp(' '.join([str(w) for w in doc2 if not w.is_stop]))

    print([str(w.pos_) for w in doc1])
    print([str(w.pos) for w in doc2])

    if method == 1:
        result = doc1.similarity(doc2)
    else:
        result = 0

    return result


if __name__ == "__main__":
    tweets = load_json("data/tweets_sets/amadeus_1612001232.json")
    results = []
    # bufale = websitescraping.get_bufale(3)
    # write_json("data/prova_bufale.json", bufale)
    bufale = load_json("data/prova_bufale.json")

    print(f"tweets: {len(tweets)}, bufale: {len(bufale)}")

    for t in tweets:
        tweet_res = {"tweet_id": t["id"]}
        tweet_res["results"] = []
        for b in bufale:
            m = {"id_bufala": b["id"],
                 "title_bufala": b["title"],
                 "first_method": float(round(get_similarity(t["text"], b["title"], 1) * 100, 2)),
                 "second_method": float(round(get_similarity(t["text"], b["title"], 2) * 100, 2)),
                 "third_method": float(round(get_similarity(t["text"], b["title"], 3) * 100, 2))}
            tweet_res["results"].append(m)
        results.append(tweet_res)

    write_json("data/prova_results.json", results)
