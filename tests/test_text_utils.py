import pytest
from book_analysis.Q2_Modules import preprocess_text, remove_stopwords, letter_frequency, ngram_counts, STOPWORDS

def test_tu():
    sample = "Hello, world! Don't stop. The data's great; it's 2025."
    cleaned, tokens, b, a = preprocess_text(sample)
    assert 'hello' in tokens
    assert "don't" in tokens or "dont" in tokens  # depending on apostrophe handling
    kept, removed = remove_stopwords(tokens, STOPWORDS)
    assert isinstance(kept, list)
    lc, total = letter_frequency(sample)
    assert total > 0
    n2 = ngram_counts(['a','b','c','d'], 2)
    assert n2['a b'] == 1
    print("Text utils tests passed.")
