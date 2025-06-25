import pandas as pd
import yfinance as yf
import pytest

from app import get_price_data


def test_get_price_data_flattens_and_returns(monkeypatch):
    def fake_download(ticker, period="6mo", progress=False, group_by="column"):
        idx = pd.date_range("2023-01-01", periods=3)
        cols = pd.MultiIndex.from_product([[ticker], ["Open", "Close"]])
        return pd.DataFrame([[1, 2], [2, 3], [3, 4]], index=idx, columns=cols)

    monkeypatch.setattr(yf, "download", fake_download)
    data = get_price_data("AAPL")

    assert not isinstance(data.columns, pd.MultiIndex)
    assert "Return" in data.columns
    expected = (3 - 2) / 2
    assert data["Return"].iloc[1] == pytest.approx(expected)
