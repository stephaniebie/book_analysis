import pytest

from book_analysis.nlp import *


def test_preprocess_text():
    input_text = "PyTHon's simple example! With punctuation."
    expected = ["python", "simple", "example", "punctuation"]
    result = preprocess_text(input_text)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_letter_frequency():
    text = "aabbccAABBCC!!"
    freq = letter_frequency(text)
    expected = {"a": 4, "b": 4, "c": 4}
    assert freq == expected


def test_word_frequency():
    filtered_text = ["test", "word", "test", "example"]
    freq = word_frequency(filtered_text)
    expected = {"test": 2, "word": 1, "example": 1}
    assert freq == expected


def test_bigram():
    filtered_text = ["this", "is", "a", "test", "this", "is"]
    freq = bigram_frequency(filtered_text)
    expected = {
        ("this", "is"): 2,
        ("is", "a"): 1,
        ("a", "test"): 1,
        ("test", "this"): 1,
    }
    assert freq == expected


def test_trigram():
    filtered_text = ["this", "is", "a", "test", "this", "is", "a"]
    freq = trigram_frequency(filtered_text)
    expected = {
        ("this", "is", "a"): 2,
        ("is", "a", "test"): 1,
        ("a", "test", "this"): 1,
        ("test", "this", "is"): 1,
    }
    assert freq == expected
