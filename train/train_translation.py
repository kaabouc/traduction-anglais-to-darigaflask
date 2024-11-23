import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras.layers import Embedding, GRU, Dense
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split

# Load Dataset
data = pd.read_csv("dataset.csv")
darija = data['darija'].tolist()
english = data['english'].tolist()

# Tokenizer
def tokenize(sentences, num_words=10000):
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=num_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(sentences)
    sequences = tokenizer.texts_to_sequences(sentences)
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, padding="post")
    return tokenizer, padded_sequences

# Tokenize Darija and English sentences
darija_tokenizer, darija_sequences = tokenize(darija)
english_tokenizer, english_sequences = tokenize(english)

# Split into Training and Validation
X_train, X_val, y_train, y_val = train_test_split(darija_sequences, english_sequences, test_size=0.2, random_state=42)

# Model Definition
embedding_dim = 256
units = 512
vocab_size_darija = len(darija_tokenizer.word_index) + 1
vocab_size_english = len(english_tokenizer.word_index) + 1

class Translator(Model):
    def __init__(self, vocab_size, embedding_dim, units):
        super().__init__()
        self.embedding = Embedding(vocab_size, embedding_dim)
        self.gru = GRU(units, return_sequences=True, return_state=True)
        self.dense = Dense(vocab_size, activation="softmax")

    def call(self, x, state=None):
        x = self.embedding(x)
        output, state = self.gru(x, initial_state=state)
        x = self.dense(output)
        return x, state

# Instantiate Models
darija_to_english = Translator(vocab_size_darija, embedding_dim, units)
english_to_darija = Translator(vocab_size_english, embedding_dim, units)

# Compile and Train
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
darija_to_english.compile(optimizer="adam", loss=loss_object)
darija_to_english.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

# Save the Model
darija_to_english.save("darija_to_english_model.h5")
