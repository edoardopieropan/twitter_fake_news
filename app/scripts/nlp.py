from app.scripts.websitescraping import get_bufale

import re
import spacy
import time
import string
from spacy.lang.it import Italian
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
#import spellcheck
import enchant
import language_tool_python




punctuations = string.punctuation + "’" + "“" + "”"
stop_words = spacy.lang.it.stop_words.STOP_WORDS
parser = Italian()


def demojify(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U0001F1F2-\U0001F1F4"  # Macau flag
                               u"\U0001F1E6-\U0001F1FF"  # flags
                               u"\U0001F600-\U0001F64F"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U0001F1F2"
                               u"\U0001F1F4"
                               u"\U0001F620"
                               u"\u200d"
                               u"\u2640-\u2642"
                               "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', text)


def preprocess(doc1, doc2):
    # remove emojis
    doc1 = demojify(doc1)
    doc2 = demojify(doc2)
    return doc1, doc2


# Creating our tokenizer function
def spacy_tokenizer(sentence, method, nlp):
    # Creating our token object, which is used to create documents with linguistic annotations.
    # tokens = parser(sentence)
    tokens = nlp(sentence)

    # Lemmatizing each token and converting each token into lowercase
    if method == 3 or method == 4:
        tokens = [word for word in tokens if word.pos_ == "NOUN" or word.pos_ == "PNOUN"]

    if method == 5 or method == 6:
        tokens = [word for word in tokens if word.pos_ != "DET"]

    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]

    # Removing stop words
    # tokens = [word for word in tokens if word not in stop_words and word not in punctuations]

    # Removing links, punctuations and characters
    if method != 3 and method != 4:
        tokens = [word for word in tokens if (not word.startswith("http")) and
                  len(set(word).intersection(set(punctuations))) == 0 and
                  len(word) > 1 and
                  word not in stop_words]

    # return preprocessed list of tokens
    return tokens


def get_similarity(doc1, doc2, method, nlp):
    doc1, doc2 = preprocess(doc1, doc2)

    # print(f"doc1 --> {doc1}")
    # print(f"doc2 --> {doc2}")

    doc1_tokens = spacy_tokenizer(doc1, method, nlp)
    doc2_tokens = spacy_tokenizer(doc2, method, nlp)

    # print("------ doc1 -------")
    # for i, w in enumerate(doc1_tokens):
    #     print(f"word {i} - {w}")
    #
    # print("\n------ doc2 -------")
    # for i, w in enumerate(doc2_tokens):
    #     print(f"word {i} - {w}")

    if method == 5:
        doc2_tokens = doc2_tokens[:len(doc1_tokens)]

    doc1 = nlp(" ".join(doc1_tokens))
    doc2 = nlp(" ".join(doc2_tokens))

    result = doc1.similarity(doc2)
    return result


def get_similarity_corpus(tweet, buf_body, nlp, corpus):
    doc1, doc2 = preprocess(tweet, buf_body)

    doc1_tokens = spacy_tokenizer(doc1, 6, nlp)
    doc2_tokens = spacy_tokenizer(doc2, 6, nlp)

    tfidf_vector = TfidfVectorizer(use_idf=True)
    # tfidf_matrix_doc2 = tfidf_vector.fit_transform([" ".join(doc2_tokens)])
    tfidf_vector.fit(corpus)
    tfidf_matrix_doc2 = tfidf_vector.transform([" ".join(doc2_tokens)])
    df = pd.DataFrame(tfidf_matrix_doc2[0].T.todense(), index=tfidf_vector.get_feature_names(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False)
    thirty_percent = int(len(doc2_tokens) * 30 / 100)
    doc2_tokens = df.head(thirty_percent).index.tolist()

    doc1 = nlp(" ".join(doc1_tokens))
    doc2 = nlp(" ".join(doc2_tokens))

    result = doc1.similarity(doc2)
    return result


def get_fact_checking(tweet_text, bufale):
    nlp = spacy.load('it_core_news_lg')
    # test1: stop-words and punctuation removal + lemmatization. The tweet is compared with the article's **title**.
    # test2: stop-words and punctuation removal + lemmatization. The tweet is compared with the article's **body**.
    # test3: keep only nouns. The tweet is compared with the article's **title**.
    # test4: keep only nouns. The tweet is compared with the article's **body**.
    # test5: stop-words and punctuation removal + lemmatization. If len(tweet) = n, the tweet is compared with the
    # first n words in the article's **body**.
    # test6: stop-words and punctuation removal + lemmatization. The tweet is compared with the 30% of the words from
    # the article's **body** with the greatest TF-IDF index.

    tests = 7
    fact_checking = {}
    corpus = []

    for b in bufale:
        corpus.append(b["body"])

    for i, b in enumerate(bufale):
        start = time.time()
        test_results = []
        # test1
        test_results.append(round(get_similarity(tweet_text, b["title"], 1, nlp), 2))
        # test2
        test_results.append(round(get_similarity(tweet_text, b["body"], 2, nlp), 2))
        # test3
        test_results.append(round(get_similarity(tweet_text, b["title"], 3, nlp), 2))
        # test4
        test_results.append(round(get_similarity(tweet_text, b["body"], 4, nlp), 2))
        # test5
        test_results.append(round(get_similarity(tweet_text, b["body"], 5, nlp), 2))
        # test6
        test_results.append(round(get_similarity_corpus(tweet_text, b["body"], nlp, corpus), 2))
        #restituisce errore,tipo_errore sullo spellcheck
        test_results.append(spellcheck(tweet_text))

        for e in range(tests):
            if e==6:
                fact_checking[f"test{e + 1}"] = {
                    "Spellcheck": test_results[e]
                }
            else:
                if i == 0:
                    fact_checking[f"test{e+1}"] = {
                        "similarity": test_results[e],
                        "fn_url": b["url"]
                    }
                elif test_results[e] > fact_checking[f"test{e+1}"]["similarity"]:
                    fact_checking[f"exp{e + 1}"] = {
                        "similarity": test_results[e],
                        "fn_url": b["url"]
                    }

        print(f"buf{i} - {time.time() - start}")

    return fact_checking

def spellcheck(text):
    print("SpellCheck")
    tool = language_tool_python.LanguageToolPublicAPI('it')
    #text='frase sbaliata    di prova!!! ciao'
    #per informazioni sui tipi di errore rilevati in italiano
    #https: // community.languagetool.org / rule / list?lang = it & offset = 0 & max = 10
    text = demojify(text)
    matchesita = tool.check(text)
    d = enchant.Dict("en_US")
    my_mistakes = []
    for rules in matchesita:
        if len(matchesita) >= 0:
            worderrorit = text[rules.offset:rules.errorLength + rules.offset]
            if worderrorit[0]!='@' and worderrorit[0]!='#':#togli parole con # o @
                errorcategory = rules.category
                #print(errorcategory)
                #print("ita: -"+worderrorit+"-")
                if errorcategory=='TYPOS':
                    if d.check(worderrorit)== False:#controlla se parola non è inglese
                        my_mistakes.append([text[rules.offset:rules.errorLength + rules.offset], errorcategory])
                else:
                    my_mistakes.append([text[rules.offset:rules.errorLength + rules.offset], errorcategory])

    #print(text)
    #print("errori" + str(len(my_mistakes)))
    #print(my_mistakes)
    if len(my_mistakes)>0:
        return len(my_mistakes), my_mistakes
    return 0 , "Nessun errore trovato"