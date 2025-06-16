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
        encoding = chardet.detect(raw)["encoding"]

    # 파일 로딩
    df = pd.read_csv("CARD_SUBWAY_MONTH_202505.csv", encoding=encoding)

    # 날짜 처리 및 총승하차 계산
    df['사용일자'] = pd.to_datetime(df['사용일자'], errors='coerce')
    df['요일'] = df['사용일자'].dt.day_name()
    df['총승하차'] = df['승차총승객수'] + df['하차총승객수']
    return df

# 데이터 불러오기
df = load_data()

# 섹션: 원본 데이터 보기
st.subheader("📄 원본 데이터 (상위 10개)")
st.dataframe(df.head(10))

# 섹션: 역별 이용량
st.subheader("📍 역별 총 승하차 인원수")
station_group = df.groupby('역명')['총승하차'].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(12, 6))
station_group.plot(kind='bar', ax=ax1)
ax1.set_title("역별 총 승하차 인원수")
ax1.set_ylabel("인원수")
ax1.set_xlabel("역명")
st.pyplot(fig1)

# 섹션: 요일별 이용량
st.subheader("🗓️ 요일별 총 승하차 인원수")
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_group = df.groupby('요일')['총승하차'].sum().reindex(weekday_order)

fig2, ax2 = plt.subplots(figsize=(10, 5))
weekday_group.plot(kind='bar', color='orange', ax=ax2)
ax2.set_title("요일별 총 승하차 인원수")
ax2.set_ylabel("인원수")
ax2.set_xlabel("요일")
st.pyplot(fig2)

# 출처
st.markdown("---")
st.caption("데이터 출처: 서울 열린데이터광장")
