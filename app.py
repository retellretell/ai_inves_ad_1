"""Improved AI Investor Advisor app with dynamic stock analysis."""

from typing import Optional, List, Dict

import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="HyperCLOVA X 기반 AI 투자 어드바이저", layout="wide")

# Increase base font sizes for better readability on desktop and mobile
st.markdown(
    """
    <style>
        .stApp {
            font-size: 16px;
        }
        @media (max-width: 768px) {
            .stApp {
                font-size: 18px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Mapping of Korean/English company names to ticker symbols
TICKER_MAP = {
    "테슬라": "TSLA",
    "tesla": "TSLA",
    "애플": "AAPL",
    "apple": "AAPL",
    "삼성전자": "005930.KS",
    "카카오": "035720.KS",
}


def detect_ticker(text: str) -> Optional[str]:
    """Return ticker symbol if company name or ticker is in text."""
    if not text:
        return None
    text_low = text.lower()
    for key, tkr in TICKER_MAP.items():
        if key in text_low or tkr.lower() in text_low:
            return tkr
    return None


def get_price_data(ticker: str) -> Optional[pd.DataFrame]:
    """Download recent price data using yfinance."""
    try:
        data = yf.download(ticker, period="6mo", progress=False)
    except Exception:
        return None

    if data is None or data.empty:
        return data

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if "Close" in data.columns:
        data["Return"] = data["Close"].pct_change()

    return data


def get_sample_news(ticker: str) -> List[Dict[str, str]]:
    """Provide sample news for the given ticker."""
    sample_news = {
        "TSLA": [
            {"title": "Tesla launches new model", "summary": "The new EV is expected to expand market share."},
            {"title": "Analysts positive on Tesla", "summary": "Wall Street sees potential growth in energy business."},
        ],
        "AAPL": [
            {"title": "Apple reveals new iPhone", "summary": "The device includes a faster chip and better camera."},
            {"title": "Apple services revenue rises", "summary": "Subscription business continues to grow."},
        ],
    }
    return sample_news.get(ticker, [{"title": "관련 뉴스 없음", "summary": "표시할 뉴스가 없습니다."}])


def get_sample_financials(ticker: str) -> Dict[str, str]:
    """Return sample quarterly financial data."""
    data = {
        "TSLA": {"EPS": "0.85", "매출": "243억 달러", "의견": "매수 우세"},
        "AAPL": {"EPS": "1.20", "매출": "830억 달러", "의견": "보유"},
    }
    return data.get(ticker, {"EPS": "-", "매출": "-", "의견": "정보 없음"})


def get_sample_esg(ticker: str) -> Dict[str, str]:
    """Return sample ESG score and issues."""
    esg = {
        "TSLA": {"score": "BBB", "issue": "자원 조달 과정 투명성 논란"},
        "AAPL": {"score": "AA", "issue": "공급망 노동 환경 이슈"},
    }
    return esg.get(ticker, {"score": "-", "issue": "정보 없음"})


def get_sample_filing_summary(ticker: str) -> str:
    """Return a short summary of a sample SEC filing."""
    filings = {
        "TSLA": "Tesla의 최근 10-K 보고서에서는 전기차 수요 증가와 배터리 사업 확대 계획이 강조되었습니다.",
        "AAPL": "Apple의 10-K 보고서는 서비스 부문 성장과 자사주 매입 계획을 주요 내용으로 포함하고 있습니다.",
    }
    return filings.get(ticker, "관련 공시 요약이 없습니다.")


def get_recommended_questions() -> List[str]:
    """Return a few example questions based on recent market trends."""
    today = pd.Timestamp("today").strftime("%Y-%m-%d")
    return [
        f"{today} 기준 미국 증시 전망은?",
        "미국 금리 인상 가능성이 주가에 미칠 영향은?",
        "테슬라 실적 발표 후 전망은?",
    ]


# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame({"종목": ["TSLA", "AAPL"], "비중(%)": [60, 40]})

if "auto_submit" not in st.session_state:
    st.session_state.auto_submit = False

if "user_query" not in st.session_state:
    st.session_state.user_query = ""

st.title("HyperCLOVA X 기반 AI 투자 어드바이저")

# User query and recommended questions
query = st.text_input("금융 관련 질문을 입력하세요", key="user_query")

cols = st.columns(len(get_recommended_questions()))
for i, rq in enumerate(get_recommended_questions()):
    if cols[i].button(rq, key=f"rec_{i}"):
        st.session_state.user_query = rq
        st.session_state.auto_submit = True

query = st.session_state.user_query
ticker = detect_ticker(query) if query else None

# Define UI tabs
tabs = st.tabs(["질문 요약", "주가", "뉴스", "실적", "ESG", "공시", "포트폴리오"])

# Tab 0: summary
with tabs[0]:
    auto = st.session_state.auto_submit
    if st.button("분석 요청", key="summary") or auto:
        st.session_state.auto_submit = False
        if query:
            answer = f"'{query}'에 대한 요약 답변 예시입니다. 시장 상황을 종합 분석했습니다."
            st.write(answer)
            st.session_state.history.append((query, answer))
            if ticker:
                st.info(f"인식된 종목: {ticker}")
            else:
                st.warning("질문에서 특정 종목을 찾을 수 없습니다.")
        else:
            st.warning("질문을 입력해 주세요.")

# Tab 1: price
with tabs[1]:
    st.subheader("최근 주가 추이")
    if ticker:
        data = get_price_data(ticker)
        if data is None or data.empty or "Close" not in data.columns:
            st.info("주가 데이터를 가져올 수 없습니다. (데이터 없음/컬럼 문제)")
        else:
            try:
                fig_price = px.line(data, y="Close", title=f"{ticker} 최근 6개월 주가")
                st.plotly_chart(fig_price, use_container_width=True)
            except Exception as e:
                st.warning(f"주가 차트 생성 중 오류가 발생했습니다: {e}")

            if "Return" in data.columns:
                try:
                    fig_ret = px.line(data, y="Return", title=f"{ticker} 일간 수익률")
                    st.plotly_chart(fig_ret, use_container_width=True)
                except Exception as e:
                    st.warning(f"수익률 차트 생성 중 오류가 발생했습니다: {e}")
    else:
        st.info("종목이 인식되지 않았습니다.")

# Tab 2: news
with tabs[2]:
    st.subheader("관련 뉴스")
    if ticker:
        for art in get_sample_news(ticker):
            st.write(f"**{art['title']}** - {art['summary']}")
    else:
        st.info("종목이 인식되지 않았습니다.")

# Tab 3: financials
with tabs[3]:
    st.subheader("최근 분기 실적")
    if ticker:
        fin = get_sample_financials(ticker)
        st.write(f"EPS: {fin['EPS']}")
        st.write(f"매출: {fin['매출']}")
        st.write(f"애널리스트 의견: {fin['의견']}")
    else:
        st.info("종목이 인식되지 않았습니다.")

# Tab 4: ESG
with tabs[4]:
    st.subheader("ESG 정보")
    if ticker:
        esg = get_sample_esg(ticker)
        st.write(f"ESG 점수: {esg['score']}")
        st.write(f"주요 논란: {esg['issue']}")
    else:
        st.info("종목이 인식되지 않았습니다.")

# Tab 5: filings
with tabs[5]:
    st.subheader("SEC 공시 요약")
    if ticker:
        st.write(get_sample_filing_summary(ticker))
    else:
        st.info("종목이 인식되지 않았습니다.")

# Tab 6: portfolio
with tabs[6]:
    st.subheader("보유 종목과 비중 입력")

    def edit_portfolio(df: pd.DataFrame) -> pd.DataFrame:
        """Display an editable table with fallback for older Streamlit versions."""
        if hasattr(st, "data_editor"):
            return st.data_editor(df, num_rows="dynamic", key="portfolio_editor")
        if hasattr(st, "experimental_data_editor"):
            return st.experimental_data_editor(
                df, num_rows="dynamic", key="portfolio_editor"
            )
        st.write("현재 Streamlit 버전에서 데이터 편집 기능을 사용할 수 없습니다.")
        st.dataframe(df)
        return df

    st.session_state.portfolio = edit_portfolio(st.session_state.portfolio)
    st.subheader("포트폴리오 비중 차트")
    if not st.session_state.portfolio.empty:
        fig_port = px.pie(
            st.session_state.portfolio,
            names="종목",
            values="비중(%)",
            hole=0.3,
        )
        st.plotly_chart(fig_port, use_container_width=True)

        weights = (
            pd.to_numeric(st.session_state.portfolio["비중(%)"], errors="coerce")
            .fillna(0)
            / 100
        )
        risk = (weights ** 2).sum() ** 0.5
        st.write(f"단순 위험 지표(예시): {risk:.2f}")
        if "TSLA" in st.session_state.portfolio["종목"].values:
            tsla_weight = st.session_state.portfolio.loc[
                st.session_state.portfolio["종목"] == "TSLA", "비중(%)"
            ].astype(float).values[0]
            st.write(f"테슬라 비중: {tsla_weight}%")
            if tsla_weight > 30:
                st.warning("테슬라 비중이 높습니다. 분산 투자를 고려해 보세요.")

# Sidebar history
st.sidebar.header("질문/답변 히스토리")
for idx, (q, a) in enumerate(reversed(st.session_state.history), 1):
    with st.sidebar.expander(f"대화 {idx}"):
        st.write(f"**Q:** {q}")
        st.write(f"**A:** {a}")

