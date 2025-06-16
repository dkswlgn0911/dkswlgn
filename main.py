import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import chardet

st.set_page_config(page_title="서울 지하철 이용 분석", layout="wide")

st.title("📊 서울 지하철 이용 분석 앱 (2025년 5월)")
st.markdown("업로드된 CSV 데이터를 기반으로 역별, 노선별, 요일별 이용량을 분석합니다.")

@st.cache_data
def load_data():
    # 파일 인코딩 자동 감지
    with open("CARD_SUBWAY_MONTH_202505.csv", "rb") as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    # 파일 읽기
    df = pd.read_csv("CARD_SUBWAY_MONTH_202505.csv", encoding=encoding)

    # 날짜 처리 (format 지정 없이 유연하게)
    df['사용일자'] = pd.to_datetime(df['사용일자'], errors='coerce')
    df['요일'] = df['사용일자'].dt.day_name()
    df['총승하차'] = df['승차총승객수'] + df['하차총승객수']

    return df

df = load_data()

st.subheader("📄 원본 데이터 미리보기")
st.dataframe(df.head())

# 사이드바 필터
st.sidebar.header("🔍 필터")
selected_line = st.sidebar.multiselect("노선 선택", sorted(df['노선명'].unique()), default=df['노선명'].unique())
selected_station = st.sidebar.multiselect("역 선택", sorted(df['역명'].unique()), default=df['역명'].unique())
selected_day = st.sidebar.multiselect("요일 선택", sorted(df['요일'].dropna().unique()), default=df['요일'].dropna().unique())

filtered_df = df[
    (df['노선명'].isin(selected_line)) &
    (df['역명'].isin(selected_station)) &
    (df['요일'].isin(selected_day))
]

st.subheader("🔎 필터링된 데이터")
st.dataframe(filtered_df.head(10))

# 역별 총 이용량 시각화
st.subheader("📍 역별 총 승하차 인원수")
station_group = filtered_df.groupby('역명')['총승하차'].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(12, 6))
station_group.plot(kind='bar', ax=ax1)
ax1.set_title("역별 총 승하차 인원수")
ax1.set_ylabel("인원수")
ax1.set_xlabel("역명")
st.pyplot(fig1)

# 요일별 이용량 시각화
st.subheader("🗓️ 요일별 승하차 인원수")
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_group = filtered_df.groupby('요일')['총승하차'].sum().reindex(weekday_order)

fig2, ax2 = plt.subplots(figsize=(10, 5))
weekday_group.plot(kind='bar', color='orange', ax=ax2)
ax2.set_title("요일별 승하차 인원수")
ax2.set_ylabel("인원수")
ax2.set_xlabel("요일")
st.pyplot(fig2)

st.markdown("---")
st.caption("데이터 출처: 서울 열린데이터광장")
