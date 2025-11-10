import re
import nltk
import string
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))


def preprocess_text(
    raw: str, keep_apostrophe_inside_word: bool = True
) -> tuple[str, list[str], int, int]:
    """
    Preprocess text:
      - lowercases
      - optionally keeps internal apostrophes (e.g., don't -> don't)
      - removes punctuation/digits (except allowed apostrophes)
      - tokenizes by whitespace
      - returns: cleaned_text (str), tokens (list), token_count_before (int), token_count_after (int)
    """
    raw_lower = raw.lower()
    # optional: normalize unicode, etc (skipped for brevity)
    token_before = raw_lower.split()
    token_count_before = len(token_before)

    if keep_apostrophe_inside_word:
        # replace punctuation except apostrophe
        # we remove digits and punctuation except apostrophe
        allowed = "'"
        # build translation table for punctuation/digits removal (except apostrophe)
        remove_chars = (
            "".join(ch for ch in string.punctuation if ch not in allowed)
            + string.digits
        )
        trans = str.maketrans({c: " " for c in remove_chars})
        cleaned = raw_lower.translate(trans)
        # collapse multiple whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
    else:
        # remove all punctuation and digits
        trans = str.maketrans({c: " " for c in string.punctuation + string.digits})
        cleaned = raw_lower.translate(trans)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # tokenization by whitespace
    tokens = cleaned.split()
    token_count_after = len(tokens)

    return cleaned, tokens, token_count_before, token_count_after


def remove_stopwords(
    tokens: list[str], stopword_set: set = STOPWORDS
) -> tuple[list[str], int]:
    kept = [t for t in tokens if t not in stopword_set]
    removed_count = len(tokens) - len(kept)
    return kept, removed_count


def letter_frequency(text: str) -> tuple[Counter, int]:
    """
    Returns Counter for letters a-z and total letters counted.
    """
    letters = re.findall(r"[a-z]", text.lower())
    c = Counter(letters)
    total = sum(c.values())
    return c, total


def ngram_counts(tokens: list[str], n: int) -> Counter:
    """
    Return Counter of n-grams (joined by space). O(len(tokens) * n)
    """
    if n <= 0:
        return Counter()
    ngrams = (" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1))
    return Counter(ngrams)


def plot_letter_freq(counter: Counter, total_letters: int):
    df = pd.DataFrame(
        [
            (
                k,
                counter.get(k, 0),
                counter.get(k, 0) / total_letters if total_letters > 0 else 0,
            )
            for k in list("abcdefghijklmnopqrstuvwxyz")
        ],
        columns=["letter", "count", "prop"],
    )
    df.plot.bar(x="letter", y="count", legend=False, figsize=(12, 4))
    plt.title("Letter frequency (a-z)")
    plt.ylabel("count")
    plt.show()


def plot_top_words(counter: Counter, top_k: int = 40):
    top = counter.most_common(top_k)
    df = pd.DataFrame(top, columns=["word", "count"])
    df.plot.bar(x="word", y="count", legend=False, figsize=(14, 5))
    plt.xticks(rotation=90)
    plt.title(f"Top {top_k} words")
    plt.show()


def wordcloud_from_counter(counter: Counter):
    wc = WordCloud(width=800, height=400)
    wc.generate_from_frequencies(counter)
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def analyze_novel(
    novel_path: str,
    keep_apostrophe_inside_word: bool = True,
    top_words=40,
    top_bigrams=20,
    top_trigrams=20,
) -> dict:
    """
    Runs the full Q2 pipeline on a novel text file.
    Returns a dict of computed objects and shows plots.
    """
    with open(novel_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    cleaned_text, tokens, before, after = preprocess_text(
        raw, keep_apostrophe_inside_word
    )
    print(f"Tokens before preprocessing (split raw): {before:,}")
    print(f"Tokens after cleaning & tokenization: {after:,}")

    # Stopword removal
    tokens_nostop, removed_count = remove_stopwords(tokens, STOPWORDS)
    print(
        f"Stopwords removed: {removed_count:,}; tokens after stopword removal: {len(tokens_nostop):,}"
    )

    # Letter frequencies
    letter_cnt, total_letters = letter_frequency(cleaned_text)
    print(f"Total letters counted: {total_letters:,}")
    plot_letter_freq(letter_cnt, total_letters)

    # Word frequencies
    word_cnt = Counter(tokens_nostop)
    print(f"Unique words after stopword removal: {len(word_cnt):,}")
    plot_top_words(word_cnt, top_words)
    wordcloud_from_counter(word_cnt)

    # Bigrams & Trigrams
    bigrams = ngram_counts(tokens_nostop, 2)
    trigrams = ngram_counts(tokens_nostop, 3)
    print("Top Bigrams:")
    for b, c in bigrams.most_common(top_bigrams):
        print(f"{b} -> {c}")
    print("\nTop Trigrams:")
    for t, c in trigrams.most_common(top_trigrams):
        print(f"{t} -> {c}")

    # Visualize bigrams/trigrams (bars)
    plot_top_words(bigrams, top_bigrams)
    plot_top_words(trigrams, top_trigrams)

    # Complexity notes (returned for inclusion in report)
    complexity = {
        "preprocessing": "O(N) where N is number of characters/tokens (single pass to clean & tokenize)",
        "counts": "O(T) where T is number of tokens for unigram counts; O(T) for n-gram generation for fixed small n",
    }

    return {
        "raw_text": raw,
        "cleaned_text": cleaned_text,
        "tokens_before": before,
        "tokens_after": after,
        "tokens_nostop": tokens_nostop,
        "letter_counter": letter_cnt,
        "total_letters": total_letters,
        "word_counter": word_cnt,
        "bigrams": bigrams,
        "trigrams": trigrams,
        "complexity": complexity,
    }


# src for extra challenge
def sentence_metrics(raw_text: str) -> dict:
    """
    Basic sentence metrics:
      - average words per sentence
      - most common sentence starters (first word after sentence split)
      - sentence length distribution
    Note: sentence splitting by [.!?] is simplistic but permitted here (no NLP libs).
    """
    # Split sentences by ., !, ? — keep simple
    sentences = re.split(r"[.!?]+", raw_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    word_counts = []
    starters = Counter()
    for s in sentences:
        # tokenize similarly: lowercase, remove extra punctuation
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
