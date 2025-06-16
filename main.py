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

    # CSV 파일 읽기
    df = pd.read_csv("CARD_SUBWAY_MONTH_202505.csv", encoding=encoding)

    # 사용일자 컬럼 제거
    if '사용일자' in df.columns:
        df = df.drop(columns=['사용일자'])

    # 총승하차 계산
    df['총승하차'] = df['승차총승객수'] + df['하차총승객수']
    
    return df

# 데이터 불러오기
df = load_data()

# 컬럼 순서 정리 (노선명부터 앞으로)
columns_order = ['노선명', '역ID', '역명', '승차총승객수', '하차총승객수', '총승하차']
df = df[columns_order]

# 원본 데이터 미리보기
st.subheader("📄 원본 데이터 (상위 10개)")
st.dataframe(df.head(10))

# 역별 총 승하차 시각화
st.subheader("📍 역별 총 승하차 인원수")
station_group = df.groupby('역명')['총승하차'].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(12, 6))
station_group.plot(kind='bar', ax=ax1)
ax1.set_title("역별 총 승하차 인원수")
ax1.set_ylabel("인원수")
ax1.set_xlabel("역명")
st.pyplot(fig1)

# 노선별 총 승하차 시각화
st.subheader("🚇 노선별 총 승하차 인원수")
line_group = df.groupby('노선명')['총승하차'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(10, 5))
line_group.plot(kind='bar', color='green', ax=ax2)
ax2.set_title("노선별 총 승하차 인원수")
ax2.set_ylabel("인원수")
ax2.set_xlabel("노선명")
st.pyplot(fig2)

st.markdown("---")
st.caption("데이터 출처: 서울 열린데이터광장")
