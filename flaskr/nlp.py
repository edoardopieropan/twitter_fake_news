import spacy

nlp = spacy.load('it_core_news_md')

def get_similarity(frase1, frase2):
    #nlp = spacy.load("it_core_news_sm")
    frase1 = nlp(frase1.__str__())
    frase2 = nlp(frase2.__str__())

    return frase1.similarity(frase2)