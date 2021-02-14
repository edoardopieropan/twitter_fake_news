import re
import spacy
import string
from spacy.lang.it import Italian

from websitescraping import get_bufale
import json

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def load_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
        return data


def write_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


nlp = spacy.load('it_core_news_lg')
punctuations = string.punctuation
stop_words = spacy.lang.it.stop_words.STOP_WORDS
parser = Italian()


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

    # # remove punctuation
    # doc1 = doc1.translate(str.maketrans('', '', string.punctuation))
    # doc2 = doc2.translate(str.maketrans('', '', string.punctuation))

    # #
    # # remove stopwords
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


# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]

    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]

    # return preprocessed list of tokens
    return mytokens


def get_similarity(doc1, doc2, method):
    # doc1 = doc1.__str__()
    # doc2 = doc2.__str__()
    # doc1, doc2 = preprocess(doc1, doc2)

    # print("doc1")
    # for w in doc1:
    #     print(f"word: {w.text}, lemma: {w.lemma_}, pos: {w.pos_}")
    #
    # print("\ndoc2")
    # for w in doc2:
    #     print(f"word: {w.text}, lemma: {w.lemma_}, pos: {w.pos_}")

    # doc1 = nlp(' '.join([str(w) for w in doc1]))
    # doc2 = nlp(' '.join([str(w) for w in doc2 if str(w) not in STOP_WORDS]))

    # doc1 = nlp(doc1)
    # doc2 = nlp(doc2)
    # for i in range(2):
    #     d1 = []
    #     d2 = []
    #     if method == 1:
    #         for w in doc1:
    #             if (not w.is_punct and not w.is_stop and w.pos_ != "DET"):
    #                 d1.append(w.lemma_)
    #
    #         for w in doc2:
    #             if (not w.is_punct and not w.is_stop and w.pos_ != "DET"):
    #                 d2.append(w.lemma_)
    #     elif method == 2:
    #         for w in doc1:
    #             if w.pos_ == "NOUN" or w.pos_ == "PNOUN":
    #                 d1.append(w.lemma_)
    #
    #         for w in doc2:
    #             if w.pos_ == "NOUN" or w.pos_ == "PNOUN":
    #                 d2.append(w.lemma_)

        # doc1 = nlp(" ".join(d1))
        # doc2 = nlp(" ".join(d2))

    # doc1 = spacy_tokenizer(doc1)
    # doc2 = spacy_tokenizer(doc2)

    bow_vector = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 1))
    tfidf_vector = TfidfVectorizer(tokenizer=spacy_tokenizer, use_idf=True, norm=None)

    bow_vector2 = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 1))
    tfidf_vector2 = TfidfVectorizer(tokenizer=spacy_tokenizer, use_idf=True, norm=None)

    # d = bow_vector.fit_transform()
    # dd = tfidf_vector.fit_transform()
    # d = [doc1, doc2]
    # d2 = bow_vector2.fit_transform(doc1)
    dd2 = tfidf_vector2.fit_transform([doc2])

    # print(d2)
    print(dd2)



    # print("doc1")
    # for w in doc1:
    #     print(f"word: {w.text} - lemma: {w.lemma_} - pos: {w.pos_} - space: {w.is_space} - norm: {w.vector_norm}")
    #
    # print("\ndoc2")
    # for w in doc2:
    #     print(f"word: {w.text}, lemma: {w.lemma_}, pos: {w.pos_} - space: {w.is_space} - norm: {w.vector_norm}")

    result = doc1.similarity(doc2)
    # print(f"similarity: {result}")

    return result


if __name__ == "__main__":
    # method 1 = similarity between tweet and the news title/body with all the tokens except stop_words, punctuation and det articles
    # method 2 = similarity between tweet and the news title/body with only nouns and proper nouns
    # method 3 = if len(tweet) = n, similarity between tweet words and n words from the news title/body with greater tf-idf
    # method 4 = similarity between 1/3 of the tweet and 30% of the words from the news title/body with greater tf_idf
    # method 5 = il len(tweet) = n, similarity between tweet words and first n words from the news title/body

    # experiment 1 = method 1 -> news title
    # experiment 2 = method 1 -> news body
    # experiment 3 = method 2 -> news title
    # experiment 4 = method 2 -> news body
    # experiment 5 = method 3 -> news title
    # experiment 6 = method 3 -> news body
    # experiment 7 = method 4 -> news title
    # experiment 8 = method 4 -> news body#
    # experiment 9 = method 5 -> news title
    # experiment 10 = method 5 -> news body

    # tweets = load_json("C:/Users/atoai/Desktop/twitter_fake_news/data/tweets_sets/ponzio_pilato_1612972806.json")
    # results = []
    # # bufale = websitescraping.get_bufale(3)
    bufale = get_bufale(2)
    # # write_json("data/prova_bufale.json", bufale)
    # # bufale = load_json("data/prova_bufale.json")
    #
    # print(f"tweets: {len(tweets)}, bufale: {len(bufale)}")
    #
    # for t in tweets[0:1]:
    #     # tweet_res = {"tweet_id": t["id"]}
    #     # tweet_res["results"] = []
    #     for b in bufale[3:4]:
    #         # m = {
    #         #     "id_bufala": b["id"],
    #         #     "title_bufala": b["title"],
    #         #     "first_method": (round(get_similarity(t["text"], b["title"], 1), 2)),
    #         #     "second_method": (round(get_similarity(t["text"], b["body"], 1), 2)),
    #         #     "third_method": (round(get_similarity(t["text"], b["title"], 2), 2)),
    #         #     "fourth_method": (round(get_similarity(t["text"], b["body"], 2), 2))
    #         # }
    #         # tweet_res["results"].append(m)
    #         print(round(get_similarity(t["text"], b["body"], 1), 2))
    #     # results.append(tweet_res)

    # doc1 = "ciao mi chiamo gianni ciao ancora e ciao di nuovo"
    doc1 = bufale[3]["body"]
    tfidf_vector2 = TfidfVectorizer(tokenizer=spacy_tokenizer, use_idf=True, norm=None)
    dd2 = tfidf_vector2.fit_transform([doc1])
    doc1 = spacy_tokenizer(doc1)
    fn = tfidf_vector2.get_feature_names()
    print("hi")
    # print(results)
    # write_json("data/prova_results.json", results)
