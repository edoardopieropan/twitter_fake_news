from app.scripts.websitescraping import get_bufale

import re
import spacy
import time
import string
from spacy.lang.it import Italian
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


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

    print(f"doc1 --> {doc1}")
    print(f"doc2 --> {doc2}")

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
        tfidf_vector = TfidfVectorizer(use_idf=True)
        tfidf_matrix_doc2 = tfidf_vector.fit_transform([" ".join(doc2_tokens)])
        df = pd.DataFrame(tfidf_matrix_doc2[0].T.todense(), index=tfidf_vector.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)
        thirty_percent = int(len(doc2_tokens) * 30 / 100)
        doc2_tokens = df.head(thirty_percent).index.tolist()

    if method == 6:
        doc2_tokens = doc2_tokens[:len(doc1_tokens)]

    doc1 = nlp(" ".join(doc1_tokens))
    doc2 = nlp(" ".join(doc2_tokens))

    result = doc1.similarity(doc2)
    return result


def get_fact_checking(tweet_text, bufale):
    nlp = spacy.load('it_core_news_lg')
    # exp1: stop-words and punctuation removal + lemmatization. The tweet is compared with the article's **title**.
    # exp2: stop-words and punctuation removal + lemmatization. The tweet is compared with the article's **body**.
    # exp3: keep only nouns. The tweet is compared with the article's **title**.
    # exp4: keep only nouns. The tweet is compared with the article's **body**.
    # exp5: stop-words and punctuation removal + lemmatization. If len(tweet) = n, the tweet is compared with the
    # first n words in the article's **body**.
    # exp6: stop-words and punctuation removal + lemmatization. The tweet is compared with the 30% of the words from
    # the article's **body** with the greatest TF-IDF index.

    experiments = 6
    fact_checking = {}

    for i, b in enumerate(bufale):
        start = time.time()
        exp = []
        # exp1
        exp.append(round(get_similarity(tweet_text, b["title"], 1, nlp), 2))
        # exp2
        exp.append(round(get_similarity(tweet_text, b["body"], 2, nlp), 2))
        # exp3
        exp.append(round(get_similarity(tweet_text, b["title"], 3, nlp), 2))
        # exp4
        exp.append(round(get_similarity(tweet_text, b["body"], 4, nlp), 2))
        # exp5
        exp.append(round(get_similarity(tweet_text, b["body"], 5, nlp), 2))
        # exp6
        exp.append(round(get_similarity(tweet_text, b["body"], 6, nlp), 2))

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

        print(f"buf{i} - {time.time() - start}")

    return fact_checking


if __name__ == "__main__":
    nlp_ = spacy.load('it_core_news_lg')
    b = {'title': 'Terremoto in Croazia e calo dei contagi: per i complottisti c’è correlazione, ma non sanno leggere un grafico', 'url': 'https://www.bufale.net/terremoto-in-croazia-e-calo-dei-contagi-per-i-complottisti-ce-correlazione-ma-non-sanno-leggere-un-grafico/', 'body': 'Al terremoto in Croazia è conseguito immediatamente il calo dei contagi. Questo, secondo chi pubblica il post che oggi prendiamo in analisi, è dovuto all’abbassamento delle misure di contenimento della pandemia nel Paese che, a sua volta, avrebbe fatto emergere la\xa0 “grande farsa della pandemia” . In poche parole: misure saltate per via del terremoto, calo dei contagi e dunque\xa0 scacco matto “covidioti” . In primo luogo ricordiamo che la parola\xa0 “covidiota”  nasce per descrivere proprio il negazionista complottaro ( qui la fonte ), ma visto che stiamo parlando di salute e infodemia, rimettiamo ordine.       La farsa è saltata. Per un problema reale: In Croazia a causa del terremoto sono saltate le misure anti-Covid, compresi lockdown e tamponi farlocchi.  Risultato: i contagi sono crollati dell’81% e tutti i virologi del pianeta non se lo spiegano.     “L’ho letto su tanti articoli”, ma non vengono indicati   Sono\xa0 corsi e ricorsi , come si può ben vedere dallo screenshot pubblicato. Chi posta questo contenuto non fornisce la fonte delle sue esternazioni, nemmeno a chi chiede:\xa0 “Davvero?” . La risposta è:\xa0 “Sì, l’ho letto in diversi articoli” . Quali siano questi articoli e quale la fonte del grafico non è dato saperlo, ma con un po’ di pazienza si raggiungono tutte le informazioni che ci servono.   I dati del terremoto e dei contagi   Iniziamo dal grafico mostrato, generato dal servizio\xa0 Our World in Data  e che possiamo facilmente controllare a  questo indirizzo .\xa0È possibile inoltre incorporare il grafico. Lo riportiamo di seguito:     Dopo l’impennata di ottobre, con un picco che si individua nella prima metà di dicembre 2020 si registra, in effetti, un calo notevole. Gli autori del post fanno riferimento alla prima metà di gennaio 2021. Il dato da analizzare è:  c’è stato veramente un calo di contagi proprio in corrispondenza del terremoto?   La prima scossa, in Croazia,  si è registrata il 29 dicembre 2020 . Se il calo dei contagi fosse davvero correlato con lo scoppio del terremoto e dunque con l’annullamento delle misure restrittive, allora vedremmo la curva dei contagi scendere intorno alla data del sisma.  Purtroppo per chi pubblica certi post, invece,\xa0non è così .   Al 23 dicembre 2020, dunque ben\xa0 6 giorni prima della prima scossa , la curva ci mostra che il calo dei contagi era già in essere. Questa è la prima incongruenza messa in rete da chi ha creato il post.   Annullato il lockdown in Croazia? Quando?   Resta da capire in quale momento la Croazia avrebbe annullato il lockdown.  Risulta, ad esempio , che dal 28 novembre al 21 dicembre 2020 fosse in atto un\xa0 lockdown parziale  per il contenimento dei contagi alla luce delle festività natalizie. Misure, queste, che sono state  estese fino all’8 gennaio . Il picco dei contagi, in effetti,  era preoccupante . L’Unità di Crisi  faceva sapere  che il quadro epidemico in Croazia era tra i peggiori in Europa.   Ad oggi il Governo croato  ha esteso fino al 28 febbraio  (lo dicono dal Ministero, non da\xa0 GocceDiLuna ) le misure restrittive, dunque  non si registra alcuna interruzione di lockdown in seguito ai terremoti . Per la scossa del 6 gennaio, per esempio,  la stampa riportava :\xa0 “Un’emergenza che si aggiunge a quella sanitaria dovuta al coronavirus, con tutto quello che questo comporta a livello di  misure di prevenzione  da rispettare in una situazione difficilissima” .   In nessuna parte della Croazia, dunque, è stato annullato il lockdown e tanto meno nelle zone colpite dal terremoto . Il calo dei contagi, piuttosto, è stato possibile proprio  grazie alle misure restrittive  iniziate verso la fine di novembre, e il Ministro dell’Interno\xa0 Vili Beroš\xa0 ha confermato , a gennaio, che il calo dell’incidenza è sì dovuto all’impegno e alle chiusure, ma per scongiurare definitivamente il pericolo bisogna sempre essere prudenti. La curva  mostra un’incidenza ancora in calo .   Riepilogo   Tra la fine di novembre e la prima metà di dicembre la Croazia è stata teatro di uno sciame sismico. Secondo i complottisti le scosse hanno portato il governo del Paese ad annullare il lockdown e miracolosamente i contagi sarebbero diminuiti.\xa0 “La farsa è saltata” , scrivono.     La curva dei contagi ha cominciato a ridursi dal 15 dicembre in poi, ben  14 giorni prima del sisma ;   Dal 28 novembre il governo croato ha disposto il  lockdown parziale  per contenere i contagi durante le festività;   I complottisti parlano di\xa0 annullamento del lockdown  ma ciò non è mai avvenuto;   Il calo dei contagi è coinciso proprio con i primi giorni del lockdown parziale, misura che si è rivelata efficace, dimostrata dall’incidenza registrata in questi giorni.     I complottisti usano la fotografia di un grafico, non\xa0 il link a quel grafico  che consentirebbe ai lettori di accedere alle informazioni e confrontare le coordinate temporali. Il terremoto in Croazia e il calo dei contagi, dunque, non hanno alcuna correlazione tra loro se non nei pensieri dei negazionisti e dei complottisti.'}
    tweet_text = "Salvate il soldato #Conte. Dopo l’eliminazione dalla Coppa Italia della sua Inter per mano della ex Juventus, il tecnico pugliese è finito sul banco degli imputati ▶ Ecco come la pensano i nostri opinionisti ⚽ https://t.co/61D5jykBZp"

    print(b)

    start = time.time()
    exp1 = round(get_similarity(tweet_text, b["title"], 1, nlp_), 2)
    print(exp1)
    print(f"time - {time.time() - start}")
    start = time.time()
    exp2 = round(get_similarity(tweet_text, b["body"], 2, nlp_), 2)
    print(exp2)
    print(f"time - {time.time() - start}")
    start = time.time()
    exp3 = round(get_similarity(tweet_text, b["title"], 3, nlp_), 2)
    print(exp3)
    print(f"time - {time.time() - start}")
    start = time.time()
    exp4 = round(get_similarity(tweet_text, b["body"], 4, nlp_), 2)
    print(exp4)
    start = time.time()
    exp5 = round(get_similarity(tweet_text, b["body"], 5, nlp_), 2)
    print(exp5)
    start = time.time()
    exp5 = round(get_similarity(tweet_text, b["body"], 6, nlp_), 2)
    print(exp5)
    print(f"time - {time.time() - start}")

