import pytest

from app import detect_ticker


def test_detect_korean_name():
    assert detect_ticker("테슬라 전망은?") == "TSLA"


def test_detect_english_name():
    assert detect_ticker("Apple outlook") == "AAPL"
