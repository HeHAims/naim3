from transformers import pipeline

# Sentiment analysis con BERT multilingüe
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analizar_sentimiento(texto):
    return sentiment_pipeline(texto)