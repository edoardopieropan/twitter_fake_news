import re
import spacy
import string
from spacy.lang.it import STOP_WORDS

nlp = spacy.load('it_core_news_md')

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def preprocess(doc1, doc2):
    #remove emojis
    doc1 = deEmojify(doc1)
    doc2 = deEmojify(doc2)

    #remove punctuation
    doc1 = doc1.translate(str.maketrans('', '', string.punctuation))
    doc2 = doc2.translate(str.maketrans('', '', string.punctuation))

    #remove stopwords
    doc1 = doc1.split()
    for word in doc1:
        if 'http' in word:
            doc1.remove(word)
        elif word in STOP_WORDS:
            doc1.remove(word)
        
    doc2 = doc2.split()
    for word in doc2:
        if 'http' in word:
            doc2.remove(word)
        elif word in STOP_WORDS:
            doc2.remove(word)

    doc1 = ' '.join(map(str, doc1)) 
    doc2 = ' '.join(map(str, doc2)) 
    return doc1, doc2


def get_similarity(doc1, doc2):

    doc1 = doc1.__str__()
    doc2 = doc2.__str__()

    doc1, doc2 = preprocess(doc1, doc2)

    doc1 = nlp(doc1)
    doc2 = nlp(doc2)
    
    # #see sentences
    # frase1 = doc1.text
    # frase2 = doc2.text

    # print('\nfrase: {}\nfrase2: {}'.format(frase1, frase2))

    return doc1.similarity(doc2)