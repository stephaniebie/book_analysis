from collections import Counter
from nltk.corpus import stopwords
from nltk.util import ngrams
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk

nltk.download('stopwords')

def count_letter_frequencies(text):

    text = text.lower()

    letter_frequencies = Counter(char for char in text if char.isalpha())

    return letter_frequencies

def word_counts(text):
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in text.lower().split() if word not in stop_words]

    word_counts = counter(filtered_words)

    return word_counts



    