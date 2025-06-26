"""Minimal yfinance stub so tests can monkeypatch download."""

def download(*args, **kwargs):
    raise NotImplementedError("yfinance is not available in this environment")
