"""
HyperCLOVA X 기반 AI 투자 어드바이저 샘플 앱
주요 기능:
 - 대화형 질의응답
 - 한국어 초장문 요약
 - 금융 리포트 자동 생성
 - 공시 번역/해설
 - 이미지(멀티모달) 분석
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from PIL import Image

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

tabs = st.tabs([
    "질문 결과",
    "초장문 요약",
    "리포트 작성",
    "공시 번역/해설",
    "이미지 분석",
    "포트폴리오 분석",
])

with tabs[0]:
    if st.button("분석 요청", key="qna"):
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
    st.subheader("긴 한국어 기사/공시 입력")
    long_text = st.text_area("5천자 이상의 텍스트도 요약 가능합니다.", height=200)
    if st.button("HyperCLOVA X 요약", key="long_summary"):
        if long_text:
            # HyperCLOVA X 초장문 요약 API 예시
            # response = requests.post(
            #     "https://clova.api.naver.com/hyperclovax/summary",
            #     headers={"Authorization": "Bearer YOUR_TOKEN"},
            #     json={"document": long_text},
            # )
            # summary = response.json()["summary"]
            summary = "입력된 장문의 한국어 텍스트를 요약한 예시 결과입니다."
            st.session_state.history.append(("장문 요약", summary))
            st.write(summary)
        else:
            st.warning("텍스트를 입력해 주세요")

with tabs[2]:
    company = st.text_input("기업명을 입력하세요", value="삼성전자")
    if st.button("리포트 생성", key="report"):
        # HyperCLOVA X 리포트 생성 API 예시
        # response = requests.post(
        #     "https://clova.api.naver.com/hyperclovax/report",
        #     headers={"Authorization": "Bearer YOUR_TOKEN"},
        #     json={"company": company},
        # )
        # report = response.json()["result"]
        report = (
            f"{company} 투자분석 리포트 예시입니다. 핵심 포인트와 리스크가 정리되어 있습니다."
        )
        st.session_state.history.append((f"{company} 리포트", report))
        st.write(report)

with tabs[3]:
    notice = st.text_area("영문 공시 또는 외신 입력", height=150)
    if st.button("번역 및 해설", key="notice"):
        if notice:
            # HyperCLOVA X 번역/해설 API 예시
            # response = requests.post(
            #     "https://clova.api.naver.com/hyperclovax/translate",
            #     headers={"Authorization": "Bearer YOUR_TOKEN"},
            #     json={"text": notice},
            # )
            # translation = response.json()["translation"]
            translation = "공시 번역본 예시"
            commentary = "투자자 관점 해설 예시입니다."
            st.session_state.history.append(("공시 해설", translation + commentary))
            st.write("**번역 결과**")
            st.write(translation)
            st.write("**해설**")
            st.write(commentary)
        else:
            st.warning("영문 텍스트를 입력해 주세요")

with tabs[4]:
    uploaded = st.file_uploader("IR 슬라이드 이미지 업로드", type=["png", "jpg", "jpeg"])
    if st.button("이미지 분석", key="image"):
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="업로드한 이미지")
            # HyperCLOVA X 멀티모달 분석 API 예시
            # response = requests.post(
            #     "https://clova.api.naver.com/hyperclovax/image-summary",
            #     headers={"Authorization": "Bearer YOUR_TOKEN"},
            #     files={"image": uploaded.getvalue()},
            # )
            # analysis = response.json()["summary"]
            analysis = "이미지 속 핵심 텍스트와 내용을 요약한 예시입니다."
            st.session_state.history.append(("이미지 분석", analysis))
            st.write(analysis)
        else:
            st.warning("이미지를 업로드해 주세요")

with tabs[5]:
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
