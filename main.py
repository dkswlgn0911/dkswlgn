import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 경로
file_path = "CARD_SUBWAY_MONTH_202505.csv"

# CSV 파일 읽기 (인코딩 문제로 cp949 사용)
df = pd.read_csv(file_path, encoding='cp949')

# 사용하지 않을 열 제거
df = df.drop(columns=['사용일자', '등록일자', '역명'])

# 노선별 승하차 인원 합계 계산
df_grouped = df.groupby('노선명')[['승차총승객수', '하차총승객수']].sum().reset_index()

# 시각화 스타일 설정
plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")

# 막대그래프 그리기
df_grouped = df_grouped.sort_values(by='승차총승객수', ascending=False)
bar_plot = sns.barplot(x='노선명', y='승차총승객수', data=df_grouped, label='승차', color='skyblue')
sns.barplot(x='노선명', y='하차총승객수', data=df_grouped, label='하차', color='orange')

# 그래프 꾸미기
plt.title('2025년 5월 지하철 노선별 총 승하차 인원')
plt.ylabel('총 승객 수')
plt.xlabel('노선명')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# 출력
plt.show()
