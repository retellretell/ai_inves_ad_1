import pandas as pd
import math

from app import extract_ticker_weight


def test_extract_numeric():
    df = pd.DataFrame({"종목": ["TSLA"], "비중(%)": ["25"]})
    weight = extract_ticker_weight(df, "TSLA")
    assert weight == 25


def test_extract_non_numeric():
    df = pd.DataFrame({"종목": ["TSLA"], "비중(%)": ["abc"]})
    weight = extract_ticker_weight(df, "TSLA")
    assert math.isnan(weight)
