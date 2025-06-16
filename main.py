import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import chardet

st.set_page_config(page_title="서울 지하철 이용 분석", layout="wide")
st.title("📊 서울 지하철 이용 분석 앱 (2025년 5월)")

@st.cache_data
def load_data():
    # 인코딩 자동 감지
    with open("CARD_SUBWAY_MONTH_202505.csv", "rb") as f:
        raw = f.read()
        encoding = chardet.detect(raw)['encoding']

    df = pd.read_csv("CARD_SUBWAY_MONTH_202505.csv", encoding=encoding)

    # 날짜 처리
    df['사용일자'] = pd.to_datetime(df['사용일자'], errors='coerce')
    df['요일'] = df['사용일자'].dt.day_name()
    df['총승하차'] = df['승차총승객수'] + df['하차총승객수']
    return df

df = load_data()

# 필터 설정
st.sidebar.header("필터")
노선 = st.sidebar.multiselect("노선명", df['노선명'].unique(), default=df['노선명'].unique())
역 = st.sidebar.multiselect("역명", df['역명'].unique(), default=df['역명'].unique())

filtered = df[(df['노선명'].isin(노선)) & (df['역명'].isin(역))]

# 역별 이용량 시각화
st.subheader("역별 총 승하차 인원")
grouped = filtered.groupby('역명')['총승하차'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
grouped.plot(kind='bar', ax=ax)
st.pyplot(fig)

# 요일별 이용량 시각화
st.subheader("요일별 총 승하차 인원")
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_grouped = filtered.groupby('요일')['총승하차'].sum().reindex(weekday_order)

fig2, ax2 = plt.subplots(figsize=(10, 5))
weekday_grouped.plot(kind='bar', color='green', ax=ax2)
st.pyplot(fig2)

st.markdown("데이터 출처: 서울열린데이터광장")
