"""HyperCLOVA X 기반 AI 투자 어드바이저 웹앱

사용자 질문에서 종목, 산업, 경제 이슈를 추출해 맞춤 정보를 보여준다.
종목이면 주가와 실적, 뉴스, ESG 데이터를, 산업이나 이슈면 관련 지수와
전망을, 포트폴리오 질문이면 자산 배분 분석을 제공한다.
HyperCLOVA X API 연동 부분은 예시 주석 형태로 남겨 두었다.
"""

from __future__ import annotations

import re
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

try:  # yfinance는 선택 사항
    import yfinance as yf

    HAS_YF = True
except Exception:  # pragma: no cover - 네트워크 없을 때 샘플 데이터 사용
    HAS_YF = False


def detect_query(text: str) -> dict:
    """질문 내용에서 종목/산업/이슈/포트폴리오 여부를 간단히 탐지."""

    stocks = {
        "삼성전자": "005930.KS",
        "카카오": "035720.KS",
        "애플": "AAPL",
        "테슬라": "TSLA",
    }
    industries = ["반도체", "전기차"]
    issues = ["금리", "환율", "ESG"]

    if "포트폴리오" in text or "자산배분" in text:
        return {"type": "portfolio", "portfolio": parse_portfolio(text)}

    for name, symbol in stocks.items():
        if name in text:
            return {"type": "stock", "name": name, "symbol": symbol}

    for ind in industries:
        if ind in text:
            return {"type": "industry", "name": ind}

    for iss in issues:
        if iss in text:
            return {"type": "issue", "name": iss}

    return {"type": "general"}


def parse_portfolio(text: str) -> pd.DataFrame:
    """문장에서 종목과 비중을 추출해 DataFrame을 만든다."""

    pairs = re.findall(r"([A-Za-z가-힣]+)\s*(\d+)%", text)
    if pairs:
        return pd.DataFrame(
            {"종목": [p[0] for p in pairs], "비중(%)": [int(p[1]) for p in pairs]}
        )
    return st.session_state.portfolio.copy()


def get_stock_price(symbol: str) -> pd.DataFrame:
    """종목 가격 데이터를 yfinance에서 받아오고, 실패 시 예시 데이터를 제공."""

    if HAS_YF:
        try:
            data = yf.download(symbol, period="1mo")
            if not data.empty:
                df = data["Close"].reset_index()
                df.columns = ["날짜", "종가"]
                return df
        except Exception:
            pass

    dates = pd.date_range(end=datetime.today(), periods=5)
    return pd.DataFrame({"날짜": dates, "종가": [100, 110, 105, 115, 120]})


st.set_page_config(page_title="HyperCLOVA X 기반 AI 투자 어드바이저")

if "history" not in st.session_state:
    st.session_state.history = []
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(
        {"종목": ["삼성전자", "테슬라"], "비중(%)": [60, 40]}
    )

st.title("HyperCLOVA X 기반 AI 투자 어드바이저")
st.caption(
    "예시: 카카오에 투자해도 될까?, 반도체 산업 전망은?, "
    "내 포트폴리오(삼성전자 60%, 테슬라 40%) 괜찮은가?"
)

query = st.text_input("금융 관련 질문을 입력하세요")
run = st.button("분석 시작")

if run and query:
    result = detect_query(query)
    st.session_state.history.append((query, result["type"]))

    tabs = st.tabs([
        "요약",
        "주가/뉴스",
        "실적/지표",
        "ESG/리스크",
        "포트폴리오 분석",
    ])

    with tabs[0]:
        summary = f"'{query}' 에 대한 HyperCLOVA X 요약 예시입니다."
        # response = requests.post("https://clova.api.naver.com/hyperclova", ...)
        st.write(summary)

    if result["type"] == "stock":
        symbol = result["symbol"]
        price_df = get_stock_price(symbol)

        with tabs[1]:
            st.subheader(f"{result['name']} 주가 추이")
            fig = px.line(price_df, x="날짜", y="종가")
            st.plotly_chart(fig, use_container_width=True)
            st.write("관련 뉴스 예시: 주요 기사 요약")

        with tabs[2]:
            st.write(f"{result['name']} 실적 요약 예시")

        with tabs[3]:
            st.write(f"{result['name']} ESG 이슈 요약 예시")

        with tabs[4]:
            st.write("현재 포트폴리오와의 연관성 분석 예시")

    elif result["type"] in {"industry", "issue"}:
        with tabs[1]:
            st.write(f"{result['name']} 관련 지수와 뉴스 예시")

        with tabs[2]:
            st.write(f"{result['name']} 전망 및 주요 지표 예시")

        with tabs[3]:
            st.write(f"{result['name']} 리스크 요약 예시")

        with tabs[4]:
            st.write("포트폴리오 영향 분석 예시")

    elif result["type"] == "portfolio":
        portfolio_df = result["portfolio"]

        with tabs[1]:
            st.write("포트폴리오 관련 뉴스 예시")

        with tabs[2]:
            st.write("보유 종목 실적 요약 예시")

        with tabs[3]:
            st.write("포트폴리오 ESG 분석 예시")

        with tabs[4]:
            fig = px.pie(portfolio_df, names="종목", values="비중(%)", hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
            st.write("자산배분 조언 예시")

    else:
        with tabs[1]:
            st.write("일반적인 시장 뉴스 예시")

        with tabs[2]:
            st.write("주요 지표 요약 예시")

        with tabs[3]:
            st.write("리스크 요약 예시")

        with tabs[4]:
            st.write("질문에 대한 포트폴리오 영향 분석 예시")

else:
    st.info("질문을 입력하고 '분석 시작' 버튼을 눌러 주세요.")


st.sidebar.header("질문/분석 히스토리")
for idx, (q, t) in enumerate(reversed(st.session_state.history), 1):
    st.sidebar.write(f"{idx}. {q} -> {t}")

st.sidebar.subheader("포트폴리오 편집")
st.session_state.portfolio = st.sidebar.data_editor(
    st.session_state.portfolio, num_rows="dynamic", key="portfolio_editor"
)

