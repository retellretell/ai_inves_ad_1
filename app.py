import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HyperCLOVA X 기반 AI 투자 어드바이저")

if "history" not in st.session_state:
    st.session_state.history = []
if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame({
        "종목": ["삼성전자", "카카오"],
        "비중(%)": [50, 50],
    })

st.title("HyperCLOVA X 기반 AI 투자 어드바이저")
st.caption("예시: 미국 금리 전망, 삼성전자 ESG 리스크, 내 포트폴리오 영향")

query = st.text_input("금융 관련 질문을 입력하세요")

tabs = st.tabs(["질문 결과", "포트폴리오 분석"])

with tabs[0]:
    if st.button("분석 요청"):
        if query:
            # HyperCLOVA X API 호출 예시 (주석 처리)
            # response = requests.post(
            #     "https://clova.api.naver.com/HyperCLOVAX",
            #     headers={"Authorization": "Bearer YOUR_TOKEN"},
            #     json={"prompt": query}
            # )
            # answer = response.json().get("result")
            answer = (
                f"'{query}' 에 대한 요약 답변 예시입니다. 시장 상황을 종합적으로 분석한 내용이 여기에 표시됩니다."
            )
            st.session_state.history.append((query, answer))

            st.subheader("요약 답변")
            st.write(answer)

            st.subheader("환율/주가 추이")
            df = pd.DataFrame({
                "날짜": pd.date_range(end=pd.Timestamp.today(), periods=7),
                "USD/KRW": [1310, 1320, 1315, 1325, 1330, 1322, 1328],
            })
            fig = px.line(df, x="날짜", y="USD/KRW", title="최근 원달러 환율 추이")
            st.plotly_chart(fig, use_container_width=True)

            esg_tab, news_tab, impact_tab = st.tabs(
                ["ESG 분석", "최신 금융 뉴스 요약", "시장 영향 분석"]
            )
            with esg_tab:
                st.write(
                    "삼성전자는 친환경 경영을 강화하고 있으나 공급망 투명성은 추가 개선이 필요하다는 평가를 받고 있습니다."
                )
            with news_tab:
                try:
                    resp = requests.get("https://example.com/api/news")
                    news_data = resp.json()
                except Exception:
                    news_data = {
                        "articles": [
                            {"title": "금융 뉴스 1", "summary": "금융 뉴스 1 요약입니다."},
                            {"title": "금융 뉴스 2", "summary": "금융 뉴스 2 요약입니다."},
                            {"title": "금융 뉴스 3", "summary": "금융 뉴스 3 요약입니다."},
                        ]
                    }
                for art in news_data["articles"][:3]:
                    st.write(f"**{art['title']}** - {art['summary']}")
            with impact_tab:
                st.write(
                    "금리와 환율 변동이 포트폴리오에 미치는 영향에 대한 예시 분석 내용입니다."
                )
        else:
            st.warning("질문을 입력해 주세요")

with tabs[1]:
    st.subheader("보유 종목과 비중 입력")
    st.session_state.portfolio = st.data_editor(
        st.session_state.portfolio, num_rows="dynamic", key="portfolio_editor"
    )
    st.subheader("포트폴리오 비중 차트")
    if not st.session_state.portfolio.empty:
        fig_port = px.pie(
            st.session_state.portfolio,
            names="종목",
            values="비중(%)",
            hole=0.3,
        )
        st.plotly_chart(fig_port, use_container_width=True)

st.sidebar.header("질문/답변 히스토리")
for idx, (q, a) in enumerate(reversed(st.session_state.history), 1):
    with st.sidebar.expander(f"대화 {idx}"):
        st.write(f"**Q:** {q}")
        st.write(f"**A:** {a}")
