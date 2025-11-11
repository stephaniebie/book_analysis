from collections import Counter
from nltk.corpus import stopwords
import nltk
import re

nltk.download('stopwords')

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = text.replace("’", "'")
    text = re.sub(r"'s\b", "", text)
    text = re.sub(r"[^a-z]", " ", text)
    tokens = text.split()
    filtered_text = [word for word in tokens if word not in stop_words]
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

def sentence_metrics(raw_text: str) -> dict:

    sentences = re.split(r"[.!?]+", raw_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    word_counts = []
    starters = Counter()
    for s in sentences:
        s_clean = re.sub(r"[^a-zA-Z\'\s]", " ", s).lower()
        toks = [t for t in s_clean.split() if t]
        if toks:
            word_counts.append(len(toks))
            starters[toks[0]] += 1
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    distribution = Counter(word_counts)
    common_starters = starters.most_common(20)
    return {
        "num_sentences": len(sentences),
        "avg_words_per_sentence": avg_words,
        "sentence_length_distribution": distribution,
        "common_sentence_starters": common_starters,
    }



def load(filepath):

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def analyze_book(filepath):

    raw_text = load(filepath)
    filtered_tokens = preprocess_text(raw_text)

    results = {
        "total_chars": len(raw_text),
        "total_tokens_before": len(raw_text.split()),
        "total_tokens_after": len(filtered_tokens),
        "letter_freq": letter_frequency(raw_text),
        "word_freq": word_frequency(filtered_tokens),
        "bigram_freq": bigram_frequency(filtered_tokens),
        "trigram_freq": trigram_frequency(filtered_tokens)
    }
    return results