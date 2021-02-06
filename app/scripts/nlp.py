import re
import spacy
import time

from app.scripts.websitescraping import get_bufale


def demojify(text):
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def preprocess(doc1, doc2):
    # remove emojis
    doc1 = demojify(doc1)
    doc2 = demojify(doc2)
    return doc1, doc2


def get_similarity(doc1, doc2, method, nlp):
    doc1, doc2 = preprocess(doc1, doc2)

    doc1 = nlp(doc1)
    doc2 = nlp(doc2)
    for i in range(3):
        d1 = []
        d2 = []
        if method == 1:
            for w in doc1:
                if not w.is_punct and not w.is_stop and w.pos_ != "DET":
                    d1.append(w.lemma_)

            for w in doc2:
                if not w.is_punct and not w.is_stop and w.pos_ != "DET":
                    d2.append(w.lemma_)
        elif method == 2:
            for w in doc1:
                if w.pos_ == "NOUN" or w.pos_ == "PNOUN":
                    d1.append(w.lemma_)

            for w in doc2:
                if w.pos_ == "NOUN" or w.pos_ == "PNOUN":
                    d2.append(w.lemma_)

        doc1 = nlp(" ".join(d1))
        doc2 = nlp(" ".join(d2))

    # print("doc1")
    # for w in doc1:
    #     print(f"word: {w.text}, lemma: {w.lemma_}, pos: {w.pos_}")
    #
    # print("\ndoc2")
    # for w in doc2:
    #     print(f"word: {w.text}, lemma: {w.lemma_}, pos: {w.pos_}")

    result = doc1.similarity(doc2)
    return result


def get_fact_checking(tweet_text, bufale):
    nlp = spacy.load('it_core_news_lg')
    # method 1 = similarity between tweet and the news title/body with all the tokens except stop_words,
    # punctuation and det articles
    # method 2 = similarity between tweet and the news title/body with only nouns and proper nouns
    # method 3 = if len(tweet) = n, similarity between tweet words and n words from the news title/body
    # with greater tf-idf
    # method 4 = similarity between 1/3 of the tweet and 30% of the words from the news title/body with greater tf_idf
    # method 5 = il len(tweet) = n, similarity between tweet words and first n words from the news title/body

    # experiment 1 = method 1 -> news title
    # experiment 2 = method 1 -> news body
    # experiment 3 = method 2 -> news title
    # experiment 4 = method 2 -> news body
    # experiment 5 = method 3 -> news title
    # experiment 6 = method 3 -> news body
    # experiment 7 = method 4 -> news title
    # experiment 8 = method 4 -> news body
    # experiment 9 = method 5 -> news title
    # experiment 10 = method 5 -> news body
    experiments = 4

    fact_checking = {}
    # for i in range(experiments):
    #     fact_checking[f"exp{i+1}"] = {
    #         "fn_url": "",
    #         "similarity": 0,
    #         "type": ""
    #     }

    # write_json("data/prova_bufale.json", bufale)
    # bufale = load_json("data/prova_bufale.json")

    for i, b in enumerate(bufale):
        start = time.time()
        exp = []
        # exp1
        exp.append(round(get_similarity(tweet_text, b["title"], 1, nlp), 2))
        # exp2
        exp.append(round(get_similarity(tweet_text, b["body"], 1, nlp), 2))
        # exp3
        exp.append(round(get_similarity(tweet_text, b["title"], 2, nlp), 2))
        # exp4
        exp.append(round(get_similarity(tweet_text, b["body"], 2, nlp), 2))
        print(f"buf{i} - {time.time() - start}")

        for e in range(experiments):
            if i == 0:
                fact_checking[f"exp{e+1}"] = {
                    "similarity": exp[e],
                    "fn_url": b["url"]
                }
            elif exp[e] > fact_checking[f"exp{e+1}"]["similarity"]:
                fact_checking[f"exp{e + 1}"] = {
                    "similarity": exp[e],
                    "fn_url": b["url"]
                }

    return fact_checking
