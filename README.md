# ai_inves_ad_1

AI investor advisor is a Streamlit application that analyzes stock information and provides example investment insights.

## Features

- **Daily recommended questions** appear as buttons for quick access.
- Clicking a recommendation automatically runs the analysis and fills the query field.
- **Responsive font sizes** are tuned for desktop and mobile viewing.

## Installation

```bash
pip install -r requirements.txt
```

The key dependencies are pinned for reproducible installs:

- `streamlit==1.35.0`
- `pandas==2.2.2`
- `plotly==5.21.0`
- `yfinance==0.2.37`

## Usage

```bash
streamlit run app.py
```

## Running Tests

Execute the test suite with [pytest](https://pytest.org/):

```bash
pytest
```

## Additional Usage Notes

Price charts rely on live market data from Yahoo Finance. Ensure the app has
network access so that `yfinance` can download the latest prices.

## Disclaimer

This app provides sample data for demonstration purposes only and is **not** financial advice. Actual market information may be delayed or inaccurate, so use the insights with caution.

The function that retrieves price data uses `st.cache_data` so repeated requests
for the same ticker and time period do not trigger additional network calls.

