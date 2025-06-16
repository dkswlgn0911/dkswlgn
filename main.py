import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import chardet
import os

st.set_page_config(page_title="서울 지하철 이용 분석", layout="wide")
st.title("📊 서울 지하철 이용 분석 앱 (2025년 5월)")

@st.cache_data
def load_data():
    filename = "CARD_SUBWAY_MONTH_202505.csv"
    if not os.path.exists(filename):
        st.error(f"⚠️ 파일이 존재하지 않습니다: {filename}")
        return None

    # 인코딩 감지
    with open(filename, "rb") as f:
        raw = f.read()
        encoding = chardet.detect(raw)["encoding"]

    try:
        df = pd.read_csv(filename, encoding=encoding)
    except Exception as e:
        st.error(f"❌ CSV 읽기 오류: {e}")
        return None

    # 사용일자 컬럼 제거
    if '사용일자' in df.columns:
        df.drop(columns=['사용일자'], inplace=True)

    # 총승하차 컬럼 추가
    if '승차총승객수' in df.columns and '하차총승객수' in df.columns:
        df['총승하차'] = df['승차총승객수'] + df['하차총승객수']
    else:
        st.error("⚠️ 필요한 컬럼이 없습니다. ('승차총승객수', '하차총승객수')")
        return None

    return df

df = load_data()
if df is not None:
    st.subheader("📄 상위 데이터 미리보기")
    st.dataframe(df.head(10))

    st.subheader("📍 역별 총 승하차 인원수")
    station_group = df.groupby('역명')['총승하차'].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    station_group.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    st.subheader("🚇 노선별 총 승하차 인원수")
    line_group = df.groupby('노선명')['총승하차'].sum().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    line_group.plot(kind='bar', ax=ax2, color='green')
    st.pyplot(fig2)

    st.caption("데이터 출처: 서울 열린데이터광장")
