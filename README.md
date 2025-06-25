# ai_inves_ad_1

AI investor advisor is a Streamlit application that analyzes stock information and provides example investment insights.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Disclaimer

This app provides sample data for demonstration purposes only and is **not** financial advice. Actual market information may be delayed or inaccurate, so use the insights with caution.

The function that retrieves price data uses `st.cache_data` so repeated requests
for the same ticker and time period do not trigger additional network calls.

