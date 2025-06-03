from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

def build_lstm_model(vocab_size=10000, embedding_dim=128):
    model = Sequential([
        Embedding(vocab_size, embedding_dim),
        LSTM(64, return_sequences=True),
        LSTM(32),
        Dense(1, activation='sigmoid')
    ])
    return model