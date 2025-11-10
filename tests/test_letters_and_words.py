from book_analysis.letters_and_words import (
    preprocess_text,
    remove_stopwords,
    letter_frequency,
    ngram_counts,
    STOPWORDS,
)

sample = "Hello, world! Don't stop. The data's great; it's 2025."
cleaned, tokens, b, a = preprocess_text(sample)


def test_preprocess_text():
    assert "hello" in tokens
    assert "don't" in tokens or "dont" in tokens  # depending on apostrophe handling


def test_remove_stopwords():
    kept, removed = remove_stopwords(tokens, STOPWORDS)
    assert isinstance(kept, list)


def test_letter_frequencey():
    lc, total = letter_frequency(sample)
    assert total > 0


def test_ngram_counts():
    n2 = ngram_counts(["a", "b", "c", "d"], 2)
    assert n2["a b"] == 1
