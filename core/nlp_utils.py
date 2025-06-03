from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
from gensim.models import Word2Vec, KeyedVectors

# Inicialización de spaCy (descarga el modelo antes: python -m spacy download es_core_news_sm)
nlp = spacy.load("es_core_news_sm")

# Cargar modelo preentrenado Word2Vec o GloVe
# w2v = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
# glove = KeyedVectors.load_word2vec_format('glove.6B.100d.txt', no_header=True)

# core/nlp_utils.py
def analizar_sentimiento_sklearn(texto):
    # Aquí deberías cargar un modelo entrenado y preprocesar el texto
    # Por ejemplo, usando un pipeline guardado con joblib
    # from joblib import load
    # model = load("sentiment_model.joblib")
    # return model.predict([texto])[0]
    # Por ahora, solo un ejemplo simple:
    if "feliz" in texto or "bien" in texto:
        return "positivo"
    elif "triste" in texto or "mal" in texto:
        return "negativo"
    else:
        return "neutral"

# core/transformers_utils.py
def analizar_sentimiento(texto):
    # ... tu implementación con transformers ...
    return "neutral"  # ejemplo