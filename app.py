import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import yfinance as yf

st.set_page_config(page_title="HyperCLOVA X 기반 AI 투자 어드바이저")

# 초기 세션 상태 설정
if "history" not in st.session_state:
    st.session_state.history = []
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame({
        "종목": ["삼성전자", "테슬라"],
        "비중(%)": [60, 40],
    })

st.title("HyperCLOVA X 기반 AI 투자 어드바이저")
st.caption(
    "예시: 카카오에 투자해도 될까?, 반도체 산업 전망은?, 미국 금리 인상 영향이 클까?, 내 포트폴리오(삼성전자 60%, 테슬라 40%) 괜찮은가?"
)

query = st.text_input("질문을 입력하세요")

# 키워드 판별 함수
def identify_query(q: str):
    stocks = {
        "삼성전자": "005930.KS",
        "카카오": "035720.KS",
        "애플": "AAPL",
        "테슬라": "TSLA",
    }
    for name, tic in stocks.items():
        if name in q:
            return {"type": "stock", "keyword": name, "ticker": tic}

    industries = ["반도체", "전기차"]
    for ind in industries:
        if ind in q:
            return {"type": "industry", "keyword": ind}

    issues = ["금리", "환율", "ESG"]
    for iss in issues:
        if iss in q:
            return {"type": "issue", "keyword": iss}

    if "포트폴리오" in q or "자산배분" in q:
        return {"type": "portfolio"}

    return {"type": "general"}

# 데이터 수집 예시 함수들
def get_stock_price(ticker: str):
    try:
        data = yf.Ticker(ticker).history(period="1mo").reset_index()[["Date", "Close"]]
    except Exception:
        data = pd.DataFrame({
            "Date": pd.date_range(end=pd.Timestamp.today(), periods=5),
            "Close": [100, 102, 101, 103, 104],
        })
    return data


def get_news(keyword: str):
    try:
        resp = requests.get(f"https://example.com/api/news?q={keyword}")
        articles = resp.json().get("articles", [])[:3]
    except Exception:
        articles = [
            {"title": f"{keyword} 뉴스 1", "summary": f"{keyword} 뉴스 1 요약"},
            {"title": f"{keyword} 뉴스 2", "summary": f"{keyword} 뉴스 2 요약"},
            {"title": f"{keyword} 뉴스 3", "summary": f"{keyword} 뉴스 3 요약"},
        ]
    return articles


def get_financials(keyword: str):
    df = pd.DataFrame({
        "항목": ["매출", "영업이익"],
        "2024": [100, 10],
        "2023": [90, 8],
    })
    return df


def analyze_query(q: str):
    info = identify_query(q)
    summary = f"'{q}'에 대한 HyperCLOVA X 요약 답변 예시입니다."
    result = {
        "type": info.get("type"),
        "summary": summary,
        "financials": None,
        "esg": None,
        "filing": None,
        "price_data": None,
        "news": None,
        "analysis": None,
    }

    if info["type"] == "stock":
        result["price_data"] = get_stock_price(info["ticker"])
        result["news"] = get_news(info["keyword"])
        result["financials"] = get_financials(info["keyword"])
        result["esg"] = f"{info['keyword']}의 ESG 요약 예시입니다."
        result["filing"] = f"{info['keyword']} 관련 최근 공시 요약 예시입니다."
    elif info["type"] == "industry":
        result["news"] = get_news(info["keyword"])
        result["financials"] = f"{info['keyword']} 산업 지표와 전망 요약 예시입니다."
        result["esg"] = f"{info['keyword']} 산업의 ESG 리스크 요약 예시입니다."
        result["filing"] = f"{info['keyword']} 산업 관련 공시 예시입니다."
    elif info["type"] == "issue":
        result["news"] = get_news(info["keyword"])
        result["financials"] = f"{info['keyword']} 관련 지표 분석 예시입니다."
        result["esg"] = f"{info['keyword']} 이슈에 대한 ESG 관점 해설 예시입니다."
        result["filing"] = f"{info['keyword']} 관련 보고서 요약 예시입니다."
    elif info["type"] == "portfolio":
        result["analysis"] = "입력된 포트폴리오에 대한 분석 예시입니다. 종목 비중 조정이 필요할 수 있습니다."
    else:
        result["news"] = get_news(q)
        result["financials"] = "일반 금융 정보 예시입니다."
    return result


if st.button("분석 요청"):
    if query:
        analysis = analyze_query(query)
        st.session_state.history.append((query, analysis["summary"]))

        tabs = st.tabs(["요약", "주가/뉴스", "실적", "ESG", "공시", "포트폴리오 분석"])
        with tabs[0]:
            st.write(analysis["summary"])
        with tabs[1]:
            if analysis["price_data"] is not None:
                fig = px.line(analysis["price_data"], x="Date", y="Close", title="주가 추이")
                st.plotly_chart(fig, use_container_width=True)
            if analysis["news"]:
                for art in analysis["news"]:
                    st.write(f"**{art['title']}** - {art['summary']}")
        with tabs[2]:
            if isinstance(analysis["financials"], pd.DataFrame):
                st.dataframe(analysis["financials"], use_container_width=True)
            else:
                st.write(analysis["financials"])
        with tabs[3]:
            if analysis["esg"]:
                st.write(analysis["esg"])
        with tabs[4]:
            if analysis["filing"]:
                st.write(analysis["filing"])
        with tabs[5]:
            st.subheader("포트폴리오 입력")
            st.session_state.portfolio = st.data_editor(
                st.session_state.portfolio, num_rows="dynamic", key="portfolio_editor"
            )
            if analysis["analysis"]:
                st.write(analysis["analysis"])
            if not st.session_state.portfolio.empty:
                fig_port = px.pie(
                    st.session_state.portfolio,
                    names="종목",
                    values="비중(%)",
                    hole=0.3,
                )
                st.plotly_chart(fig_port, use_container_width=True)
    else:
        st.warning("질문을 입력해 주세요")

st.sidebar.header("질문/답변 히스토리")
for idx, (q, a) in enumerate(reversed(st.session_state.history), 1):
    with st.sidebar.expander(f"대화 {idx}"):
        st.write(f"**Q:** {q}")
        st.write(f"**A:** {a}")

