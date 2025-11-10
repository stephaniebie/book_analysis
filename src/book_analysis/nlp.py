from collections import Counter
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    cleaned_text = text.lower().split()
    filtered_text = [word for word in cleaned_text if word.isalpha() and word not in stop_words]
    return filtered_text

def letter_frequency(text):
    text = text.lower()
    letter_counts = Counter(char for char in text if char.isalpha())
    return letter_counts

def word_frequency(filtered_text):
    word_counts = Counter(filtered_text)
    return word_counts

def bigram_frequency(filtered_text):
    bigrams = [(filtered_text[i], filtered_text[i + 1]) for i in range(len(filtered_text) - 1)]
    bigram_counts = Counter(bigrams)
    return bigram_counts

def trigram_frequency(filtered_text):
    trigrams = [(filtered_text[i], filtered_text[i + 1], filtered_text[i + 2]) for i in range(len(filtered_text) - 2)]
    trigram_counts = Counter(trigrams)
    return trigram_counts